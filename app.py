from flask import Flask, render_template, request, redirect, session
from markupsafe import Markup
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
from main import process_campaign

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-123')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["5 per minute"])

ZAPIER_WEBHOOK_URL = "zapier_webhook_link"
LINKEDIN_ACCESS_TOKEN = 'add_your_access_token'  # Replace with your LinkedIn access token

request_cache = {}

def check_duplicates(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.form.copy()
        if 'pdf_file' in request.files:
            request_data['pdf_filename'] = secure_filename(request.files['pdf_file'].filename)
        signature = f"{get_remote_address()}-{str(sorted(request_data.items()))}"
        if signature in request_cache:
            return "Duplicate request blocked", 429
        request_cache[signature] = datetime.now().timestamp()
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET'])
def campaign_form():
    return render_template('campaign_form.html')

@app.route('/', methods=['POST'])
@limiter.limit("5/minute")
@check_duplicates
def handle_campaign():
    try:
        campaign_details = {
            'product': request.form['product'],
            'goal': request.form['goal'],
            'audience': request.form['audience'],
            'budget': float(request.form['budget']),
            'platform': request.form['platform'],
            'website': request.form['website']
        }

        pdf_path = None
        if 'pdf_file' in request.files:
            pdf_file = request.files['pdf_file']
            if pdf_file.filename != '':
                filename = secure_filename(pdf_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                pdf_file.save(filepath)
                pdf_path = filepath

        result = process_campaign(campaign_details, pdf_path)

        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)

        if isinstance(result, tuple):
            headline, body = result
        else:
            headline, body = "Ad Headline Not Found", str(result) if result else "Ad Body Not Found"

        idempotency_key = str(uuid.uuid4())
        content_hash = hash(f"{campaign_details}{headline}{body}")
        unique_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{content_hash}"

        plain_message = f"{headline}\n\n{body}{campaign_details['website']}"

        zapier_payload = {
            "idempotency_key": idempotency_key,
            "client_tracking_id": unique_id,
            "message": plain_message,
            **campaign_details,
            "result": body,
            "pdf_excerpt": "",
            "linkedin_params": {
                "client_tracking_id": unique_id,
                "visibility": "PUBLIC",
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": []
                }
            }
        }

        requests.post(ZAPIER_WEBHOOK_URL, json=zapier_payload, timeout=10)

        post_to_linkedin(campaign_details, body, unique_id)

        # Return the result as an inline HTML response
        return f"""
            <div style="padding: 2em; font-family: Arial, sans-serif;">
                <h2 style="color: #2c3e50;">{campaign_details['product']} — Campaign Result</h2>
                <h3 style="color: #2980b9;">{headline}</h3>
                <p>{body}</p>
                <br><a href="/" style="text-decoration:none;color:#3498db;">← Back to form</a>
            </div>
        """

    except Exception as e:
        app.logger.error(f"Error processing campaign: {str(e)}")
        return f"<h3>Error occurred:</h3><pre>{str(e)}</pre>", 500

def post_to_linkedin(details, content, tracking_id):
    print(f"[LinkedIn Post] ID: {tracking_id}, Platform: {details['platform']}, Content: {content[:150]}...")

if __name__ == "__main__":
    app.run(debug=True)
