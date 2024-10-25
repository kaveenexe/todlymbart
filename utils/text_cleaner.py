import re
import language_tool_python

# Initialize the LanguageTool object
tool = language_tool_python.LanguageTool('en-US')

# Pre Processing
# Function to clean the response text
def clean_text(text):
    # Remove non-printable characters
    text = ''.join(filter(lambda x: x.isprintable(), text))

    # Normalize the text by collapsing multiple spaces into a single space
    text = ' '.join(text.split())

    # Remove HTML tags or content enclosed within '<' and '>'
    text = re.sub(r'<.*?>', '', text)

    # Remove any characters that are not Sinhala, English, or allowed punctuation
    text = re.sub(r'[^\u0D80-\u0DFFa-zA-Z0-9\s\.\,\?\!\-\–]', '', text)

    return text

def correct_grammar(text):
    """
    Uses LanguageTool to perform spelling and grammar correction on the text.
    """
    matches = tool.check(text)
    corrected_text = tool.correct(text)
    return corrected_text


# Post Processing
def filter_unwanted_characters(text):
    # Allow Sinhala, English, spaces, basic punctuation, and both hyphen types
    return re.sub(r'[^\u0D80-\u0DFFa-zA-Z0-9\s\.\,\?\!\-\–]', '', text)
