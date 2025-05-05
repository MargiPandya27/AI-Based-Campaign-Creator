import argparse
from llm_utils import generate_ad_content
from mock_api import create_campaign_flow

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Ad Campaign Creator")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--budget", required=True)
    parser.add_argument("--duration", required=True)
    parser.add_argument("--ad_prompt", required=True)

    args = parser.parse_args()

    print("\n🤖 Generating ad content using LLM...")
    ad_data = generate_ad_content(args.ad_prompt)

    print("\n🚀 Creating campaign (mock)...")
    create_campaign_flow(args, ad_data)

if __name__ == "__main__":
    main()
