from konlpy.tag import Okt
import os

# Initialize the Okt tokenizer
okt = Okt()

def preprocess_file(file_path):
    """
    Preprocess the content of a file by filtering out specific parts of speech.
    Retains only nouns, verbs, adjectives, and adverbs.

    Args:
    file_path: Path to the file to be processed.

    Returns:
    A list of cleaned and preprocessed lines from the file.
    """
    cleaned_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = okt.pos(text, stem=True)
            # Filter tokens based on POS tags and exclude URLs
            tokens = [word for word, pos in tokens if pos in ['Noun', 'Verb', 'Adjective', 'Adverb'] and 'http' not in word]
            cleaned_line = " ".join(tokens)
            if cleaned_line:  # Ensure the cleaned line is not empty
                cleaned_lines.append(cleaned_line)
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
    return cleaned_lines

def process_directory(source_directory, result_directory):
    """
    Process all text files in the source directory and save the results in the result directory.
    """
    # Ensure the result directory exists
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    for filename in os.listdir(source_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(source_directory, filename)
            result_file_path = os.path.join(result_directory, filename)

            print(f"Processing file: {file_path}")  # Debugging line

            cleaned_lines = preprocess_file(file_path)

            if cleaned_lines:
                # Write the preprocessed text to a new file
                with open(result_file_path, 'w', encoding='utf-8') as result_file:
                    result_file.write("\n".join(cleaned_lines))
                print(f"Processed and saved: {filename}")
            else:
                print(f"No content to save for: {filename}")

if __name__ == "__main__":
    source_directory = r'2.0_Extracted_Articles_ENG'
    result_directory = r'2.6_Extracted_Articles_ENG'
    process_directory(source_directory, result_directory)
