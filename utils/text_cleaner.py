import re


# Function to clean the response text
def clean_text(text):
    # Remove non-printable characters
    text = ''.join(filter(lambda x: x.isprintable(), text))

    # Normalize the text by collapsing multiple spaces into a single space
    text = ' '.join(text.split())

    # Remove HTML tags or content enclosed within '<' and '>'
    text = re.sub(r'<.*?>', '', text)

    # Remove any characters that are not Sinhala, English, or allowed punctuation
    text = re.sub(r'[^\u0D80-\u0DFFa-zA-Z0-9\s\.\,\?\!\-]', '', text)

    return text
