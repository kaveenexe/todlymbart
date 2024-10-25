import re
from utils.custom_lexicon import apply_custom_lexicon, custom_lexicon
from utils.translation import translate_text_with_fallback

# NOT USING CURRENTLY
def detect_and_translate_untranslated_segments(text, source_lang, target_lang):
    english_pattern = r'\b[A-Za-z]+\b'
    untranslated_segments = re.findall(english_pattern, text)

    for segment in untranslated_segments:
        if segment not in custom_lexicon:
            translated_segment = translate_text_with_fallback(segment, source_lang, target_lang)
            text = text.replace(segment, translated_segment)

    return apply_custom_lexicon(text)
