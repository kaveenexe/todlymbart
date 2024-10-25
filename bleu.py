# bleu.py
import pandas as pd
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from utils.translation import translate_text_with_fallback
from utils.text_cleaner import correct_grammar
from tqdm import tqdm  # Import progress bar

# Ensure necessary NLTK components are available
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Function to calculate BLEU score for a single sentence pair (reference vs. generated)

def calculate_bleu_score(reference, candidate):
    # Tokenize the reference and candidate sentences with explicit language specification
    reference_tokens = [nltk.word_tokenize(reference, language='english')]
    candidate_tokens = nltk.word_tokenize(candidate, language='english')

    # Apply smoothing and calculate BLEU with a lower n-gram order (up to 2-grams)
    smoothing_function = SmoothingFunction().method4  # method4 applies moderate smoothing
    bleu_score = sentence_bleu(
        reference_tokens,
        candidate_tokens,
        weights=(0.5, 0.5),  # Up to bigrams only, with equal weights
        smoothing_function=smoothing_function
    )
    return bleu_score

def load_sentences_from_csv(file_path):
    """
    Load sentences from a CSV file where:
    - Source column contains English sentences
    - Target column contains Sinhala sentences (your translations)
    :param file_path: Path to the CSV file
    :return: A list of dictionaries with 'source' and 'reference' keys
    """
    df = pd.read_csv(file_path)
    sentences = []

    # Assuming the CSV has 'source' and 'target' columns for English and Sinhala sentences
    for _, row in df.iterrows():
        sentences.append({
            'source': row['target'],  # Sinhala sentence is the "source" for translation
            'reference': row['source']  # English sentence is the reference translation
        })

    return sentences

def evaluate_bleu_score_directly(file_path):
    """
    Evaluates BLEU score by loading sentences from the CSV and calculating the BLEU score for each pair
    :param file_path: Path to the CSV file
    """
    # Load the sentences from the CSV file
    sentences = load_sentences_from_csv(file_path)

    total_bleu_score = 0
    count = len(sentences)

    # Use tqdm to display progress bar
    for sentence_pair in tqdm(sentences, desc="Evaluating BLEU Score", unit="sentence"):
        source_sentence = sentence_pair['source']  # Sinhala sentence (machine-generated)
        reference_translation = sentence_pair['reference']  # English sentence (human translation)

        # Translate the Sinhala sentence to English using your model
        generated_translation = translate_text_with_fallback(source_sentence, 'si_LK', 'en_XX')

        # Apply spelling and grammar correction to the generated translation
        corrected_translation = correct_grammar(generated_translation)

        # Calculate BLEU score for the current sentence pair
        bleu_score = calculate_bleu_score(reference_translation, corrected_translation)

        # Print BLEU score for each sentence
        print(f"Source (Sinhala): {source_sentence}")
        print(f"Reference (English): {reference_translation}")
        print(f"Generated (English): {generated_translation}")
        print(f"Corrected (English): {corrected_translation}")
        print(f"BLEU score: {bleu_score}\n")

        total_bleu_score += bleu_score

    # Calculate the average BLEU score across all sentences
    average_bleu_score = total_bleu_score / count
    print(f"\nAverage BLEU Score: {average_bleu_score}")

# Run the BLEU score evaluation directly using your CSV file
if __name__ == "__main__":
    # Set the path to your CSV file
    file_path = r"D:\SLIIT\Year 04\Research\Implementation\Helsinki\TodlyDataset.csv"

    # Call the function to evaluate BLEU score
    evaluate_bleu_score_directly(file_path)
