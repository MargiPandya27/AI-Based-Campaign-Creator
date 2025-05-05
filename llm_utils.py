from transformers import pipeline

# Load LLM pipeline
generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", device_map="auto")

def generate_ad_content(prompt: str) -> str:
    full_prompt = f"""<s>[INST] Write a catchy ad copy for the following product/service: {prompt} 
Return format:
Headline:
Text:
CTA:
[/INST]"""
    
    result = generator(full_prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    return result[0]["generated_text"].split('[/INST]')[-1].strip()
