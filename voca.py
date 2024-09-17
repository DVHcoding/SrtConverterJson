import json
import nltk
from googletrans import Translator

def extract_single_words(json_file, output_file):
    """Extract single words and their translations from a JSON file."""
    # Download required NLTK data
    nltk.download('punkt')
    nltk.download('stopwords')
    
    translator = Translator()
    
    with open(json_file, 'r', encoding='utf-8') as f:
        subtitles = json.load(f)

    text = ""
    
    # Combine all subtitle text into a single string
    for subtitle in subtitles:
        text += subtitle['text'] + " "
    
    # Tokenize and clean text
    tokens = nltk.word_tokenize(text)
    stopwords = set(nltk.corpus.stopwords.words('english'))
    words = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords]

    # Remove duplicates by converting to a set
    unique_words = set(words)
    terms_definitions = []

    # Fetch translations for each unique word
    for word in unique_words:
        try:
            translation = translator.translate(word, src='en', dest='vi').text
            terms_definitions.append({
                'term': word,
                'definition': translation
            })
        except Exception as e:
            print(f"Error translating word '{word}': {e}")
            terms_definitions.append({
                'term': word,
                'definition': "Definition not found."
            })

    # Write terms and definitions to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(terms_definitions, f, ensure_ascii=False, indent=4)

# Example usage
extract_single_words('./BabyChickJump.json', './single_words.json')
