from flask import Blueprint, request, jsonify

from utils.custom_lexicon import apply_custom_lexicon
from utils.translation import translate_text_with_fallback
from templates import prompt, ollama_model
from utils.text_cleaner import clean_text, correct_grammar, filter_unwanted_characters
from bleu import calculate_bleu_score
from utils.untranslate_detection import detect_and_translate_untranslated_segments

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
    if translated_question is None:
        return jsonify({"error": "Translation failed. Please try again."}), 500

    print("Translated Question (Sinhala to English):", translated_question)

    # Step 2: Get the answer from the model
    response = (prompt | ollama_model).invoke({"question": translated_question})
    print("LLM's Response (in English):", response)

    # Step 3: Clean and correct the LLM's response
    cleaned_english_answer = clean_text(response)
    corrected_answer = correct_grammar(cleaned_english_answer)
    print("Corrected LLM's Response (in English):", corrected_answer)

    # Step 4: Translate the corrected response back to Sinhala
    intermediate_answer = translate_text_with_fallback(corrected_answer, "en_XX", "si_LK")
    if intermediate_answer is None:
        return jsonify({"error": "Final translation failed. Please try again."}), 500

    # Step 5: Apply targeted re-translation for untranslated segments
    # final_answer = detect_and_translate_untranslated_segments(intermediate_answer, "en_XX", "si_LK")

    # Step 5:
    lexicon_answer = apply_custom_lexicon(intermediate_answer)

    # Step 6:
    final_answer = filter_unwanted_characters(lexicon_answer)

    print("Final Answer (English to Sinhala):", final_answer)
    return jsonify({"answer": final_answer})
