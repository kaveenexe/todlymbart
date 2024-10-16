from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch
import requests
import re

app = Flask(__name__)

# Load the mBART-50 model and tokenizer
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

def translate_text(text, source_lang, target_lang):
    # Set the source language
    tokenizer.src_lang = source_lang

    # Encode the text
    encoded_text = tokenizer(text, return_tensors="pt")

    # Generate translation
    generated_tokens = model.generate(
        **encoded_text,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
        max_length=512,
        num_beams=10,
        temperature=0.7,
        repetition_penalty=1.5,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    # Decode the generated tokens
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_text

def clean_text(text):
    # Remove any non-printable characters
    text = ''.join(filter(lambda x: x.isprintable(), text))
    # Remove any extra whitespace
    text = ' '.join(text.split())
    # Remove any special tokens or placeholders
    text = re.sub(r'<.*?>', '', text)
    # Remove any unwanted characters (e.g., characters from other scripts)
    # For Sinhala, Unicode range is U+0D80 to U+0DFF
    # Keep Sinhala characters, English letters, and common punctuation
    text = re.sub(r'[^\u0D80-\u0DFFa-zA-Z0-9\s\.\,\?\!\-]', '', text)
    return text

def translate_text_with_fallback(text, source_lang, target_lang):
    translated_text = translate_text(text, source_lang, target_lang)
    # Simple heuristic: if the translation is significantly shorter or contains unwanted characters
    if len(translated_text) < 0.7 * len(text) or any(char in translated_text for char in ['{', '\\', '}']):
        print("Translation may be incomplete or contains unwanted characters.")
        # Implement fallback here if needed
    return translated_text

@app.route('/')
def home():
    return "Welcome to the Toddler App API! Use the /process endpoint to interact with the service."

@app.route('/process', methods=['POST'])
def process_request():
    data = request.json
    question = data.get("question")
    source_lang = data.get("source_lang", "si_LK")
    target_lang = data.get("target_lang", "en_XX")

    # Translate the question from Sinhala to English
    translated_question = translate_text_with_fallback(question, source_lang, target_lang)
    print("Translated Question (Sinhala to English):", translated_question)

    # Modify the prompt sent to the LLM
    prompt = f"""
You are an expert in child nutrition and development. Please provide a concise, plain-text short answer to the following question without any special characters, numbering, bullets or formatting:

Question: {translated_question}
"""

    # Send the prompt to Ollama
    llm_response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        headers={"Content-Type": "application/json"},
        json={
            "model": "blackalpha/todlymist",
            "prompt": prompt,
            "max_tokens": 256,  # Adjust as needed
            "stream": False
        }
    )

    if llm_response.status_code == 200:
        english_answer = llm_response.json().get("response")
        print("LLM's Response (in English):", english_answer)
    else:
        return jsonify({"error": "Failed to get a response from LLM"}), 500

    # Clean the LLM's response
    english_answer = clean_text(english_answer)
    print("Cleaned LLM's Response (in English):", english_answer)

    # Translate the LLM's answer back to Sinhala
    final_answer = translate_text_with_fallback(english_answer, "en_XX", "si_LK")
    print("Final Answer (English to Sinhala):", final_answer)

    return jsonify({"answer": final_answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)