# 🧠 AI-Powered Campaign Creator 


## 📑 Table of Contents

- [Objective](#-objective)
- [Architecture Overview](#️-architecture-overview)
  - [🔹 Inputs](#-inputs)
  - [🔹 Core Modules](#-core-modules)
- [LLM Model Selection](#-llm-model-selection)
- [Repository Structure](#-repository-structure)
- [Deliverables](#-deliverables)
- [ Getting Started & Running the Code](#-getting-started-&-running-the-code)
- [Future Scope](#-future-scope)
- [Contact](#-contact)

---


## Objective

This project demonstrates a minimal viable product (MVP) for automating the creation of digital ad campaigns using a Large Language Model (LLM) and deploying them on platforms like Meta, TikTok, or LinkedIn. The tool takes a structured campaign brief and optionally a PDF input, and generates ad copy and targeting suggestions using prompt-engineered LLM responses.

---

## Architecture Overview

<img src="https://github.com/user-attachments/assets/4a9f6aec-db35-4745-9f1c-b57c9f75023e" alt="image" width="500"/>


### Core Modules

1. **PDF Text Extraction**  
   Utilizes `PyMuPDF` for multi-page PDF parsing and conversion to usable plain text.

2. **LLM-Powered Ad Generator**  
   Uses Google's Gemini 1.5 Flash via the Generative AI API to generate structured campaign content with tailored prompt engineering for LinkedIn.

3. **Campaign Deployment (Prototype)**  
   Placeholder logic that simulates campaign submission. Modularized to integrate Meta, LinkedIn, and TikTok Ads APIs in production.

---

## LLM Model Selection

| Model         | Pros                                             | Cons                                 | Reason for Not Choosing          |
|---------------|--------------------------------------------------|--------------------------------------|----------------------------------|
| **Gemini 1.5 Flash** | Fast, structured output, stable formatting | API limits, Easy to deploy          | ✅ Chosen for MVP                 |
| LLaMA 2        | Open-source, local control                      | Requires GPU, setup-heavy            | Not practical for quick MVP      |
| Mistral        | Lightweight, open license                       | Lower instruction-following ability  | Less robust for prompt structure |
| Claude         | Strong reasoning and summarization              | Inconsistent formatting, slower      | Good alternative, not ideal here |
| GPT-4          | Powerful and accurate                           | Expensive, slow                      | Overkill for MVP, high latency   |

**Gemini 1.5 Flash** was chosen for its optimal trade-off between inference speed, formatting reliability, and ease of integration for a structured prompt environment.

---

## Repository Structure

├── main.py # CLI runner
├── llm_generator.py # LLM interaction and prompt construction
├── campaign_runner.py # Execution pipeline for end-to-end flow
├── extractor.py # PDF handling logic
├── config.env # API keys (excluded in repo)
├── README.md # Project overview and instructions
└── screenshots/ # Sample output snapshots

---

## Getting Started & Running the Code

### 1. Setup Environment

Clone the repository and install the required Python packages:

```bash
git clone https://github.com/your-username/atomicads-ai-engineer-assignment-margi.git
cd atomicads-ai-engineer-assignment-margi
pip install -r requirements.txt
```

### 2. Configure API Access
Create a .env file in the root directory and add your Google Generative AI API key:

```bash
GOOGLE_API_KEY=your_google_genai_api_key_here
```

⚠️ You need access to Google’s Gemini Generative AI API for this to work.

### 3. How to Set Up the Workflow in Zapier

1. Go to the [Zapier Dashboard](https://zapier.com/app/dashboard)
2. Click on **"Create Zap"**

#### Step 1: Set Up Trigger

- **App**: Webhooks by Zapier  
- **Trigger Event**: `Catch Hook`  
- Zapier will generate a custom webhook URL. Use it in your Python script to POST the generated LinkedIn ad content.


### 4. Run the Application
Run the python app.py to generate an ad campaign:

```bash
python app.py
```
---

## Deliverables

- [x] Python scripts (`main.py`, `llm_generator.py`, etc.)
- [x] Environment config (`.env`)
- [x] README documentation
- [x] Prompt examples
- [x] Simulated ad output and screenshots


---

## Future Scope

- ✅ Add frontend via Streamlit or Flask
- ✅ Real-time deployment via Ads API (Meta, LinkedIn, TikTok)
- ✅ Feedback loop and A/B testing capabilities
- ✅ Cost optimization via local open-source models
- ✅ Prompt tuning and output validation logic

---

## 🙋‍♀️ Contact

Feel free to reach out on [LinkedIn](https://www.linkedin.com/in/margi-pandya/) or [Email](mapandya@ucsd.edu) for any questions or feedback.

