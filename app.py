from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

app = Flask(__name__)

# Load the mBART-50 model and tokenizer for translations
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

# Function to handle translation using mBART-50
def translate_text(text, source_lang, target_lang):
    tokenizer.src_lang = source_lang
    encoded_text = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded_text,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
        max_length=512,
        num_beams=10,
        repetition_penalty=1.5,
        no_repeat_ngram_size=3,
        early_stopping=True,
        do_sample=True
    )
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_text

# Function to clean the response text
def clean_text(text):
    text = ''.join(filter(lambda x: x.isprintable(), text))
    text = ' '.join(text.split())
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\u0D80-\u0DFFa-zA-Z0-9\s\.\,\?\!\-]', '', text)
    return text

# Function to translate with fallback if needed
def translate_text_with_fallback(text, source_lang, target_lang):
    translated_text = translate_text(text, source_lang, target_lang)
    if len(translated_text) < 0.7 * len(text) or any(char in translated_text for char in ['{', '\\', '}']):
        print("Translation may be incomplete or contains unwanted characters.")
    return translated_text

# Define the ChatPromptTemplate
template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

# Set up the OllamaLLM model
ollama_model = OllamaLLM(model="blackalpha/todlymist")

@app.route('/')
def home():
    return "Welcome to the Toddler App API! Use the /process endpoint to interact with the service."

@app.route('/process', methods=['POST'])
def process_request():
    data = request.json
    question = data.get("question")
    source_lang = data.get("source_lang", "si_LK")
    target_lang = data.get("target_lang", "en_XX")

    # Step 1: Translate the question from Sinhala to English
    translated_question = translate_text_with_fallback(question, source_lang, target_lang)
    print("Translated Question (Sinhala to English):", translated_question)

    # Step 2: Use the ChatPromptTemplate and the Ollama model to get the answer
    response = (prompt | ollama_model).invoke({"question": translated_question})
    print("LLM's Response (in English):", response)

    # Step 3: Clean the LLM's response
    cleaned_english_answer = clean_text(response)
    print("Cleaned LLM's Response (in English):", cleaned_english_answer)

    # Step 4: Translate the LLM's answer back to Sinhala
    final_answer = translate_text_with_fallback(cleaned_english_answer, "en_XX", "si_LK")
    print("Final Answer (English to Sinhala):", final_answer)

    return jsonify({"answer": final_answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
