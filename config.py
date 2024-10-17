from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

# Load mBART-50 model and tokenizer for translations
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)
