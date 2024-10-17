from flask import Blueprint, request, jsonify
from utils.translation import translate_text_with_fallback
from utils.text_cleaner import clean_text
from templates import prompt, ollama_model

# Initialize Blueprint for routing
api_routes = Blueprint('api', __name__)

@api_routes.route('/')
def home():
    return "Welcome to the Toddler App API! Use the /process endpoint to interact with the service."

@api_routes.route('/process', methods=['POST'])
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
