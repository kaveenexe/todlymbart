import torch
from config import tokenizer, model

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

# Function to translate with fallback if needed
def translate_text_with_fallback(text, source_lang, target_lang):
    translated_text = translate_text(text, source_lang, target_lang)
    if len(translated_text) < 0.7 * len(text) or any(char in translated_text for char in ['{', '\\', '}']):
        print("Translation may be incomplete or contains unwanted characters.")
    return translated_text
