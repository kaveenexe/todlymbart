import re
from google.cloud import translate_v2 as translate
import os

from utils.translation import translate_text_with_fallback


# NOT USING CURRENTLY
# Initialize the Google Translate client
# Set up Google Cloud credentials

def detect_and_translate_untranslated_segments_batch(text, source_lang, target_lang):
    # Find all English words in the text
    english_words = re.findall(r'\b[a-zA-Z]+\b', text)
    if not english_words:
        return text

    print(f"Detected untranslated segments: {set(english_words)}")

    # Remove duplicates while preserving order
    english_words_unique = list(dict.fromkeys(english_words))

    # Translate all detected English words in one go
    translations = translate_text_with_fallback(" ".join(english_words_unique), source_lang, target_lang)
    translated_words = translations.split()

    # Ensure the number of translations matches the number of words
    if len(translated_words) != len(english_words_unique):
        print("Mismatch in number of words and translations. Individual translation will be used.")
        # Translate words individually
        translation_map = {}
        for word in english_words_unique:
            translation = translate_text_with_fallback(word, source_lang, target_lang)
            translation_map[word] = translation
    else:
        # Map the English words to their translations
        translation_map = {word: trans for word, trans in zip(english_words_unique, translated_words)}

    # Replace English words with their Sinhala translations
    def replace_match(match):
        word = match.group(0)
        return translation_map.get(word, word)

    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in translation_map.keys()) + r')\b', flags=re.IGNORECASE)
    text = pattern.sub(replace_match, text)

    return text
