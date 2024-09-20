import spacy
import os

# Load spaCy's English model for efficient NLP tasks including tokenization.
# This pre-trained model handles various NLP tasks with a single call.
nlp = spacy.load("en_core_web_sm")

def tokenize_file(file_path):
    """
    Tokenize the content of a file into sentences using spaCy.

    Args:
    file_path: The path to the text file to be processed.

    Returns:
    A list of sentences extracted from the file.

    This function opens the specified text file, reads its content,
    and uses the spaCy NLP model to tokenize the text into sentences.
    If an error occurs, it catches and prints the error message.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]
        return sentences
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return []

def sanitize_filename(filename):
    """
    Sanitize the filename to avoid issues with long paths and special characters.

    Args:
    filename: The original filename to be sanitized.

    Returns:
    A sanitized version of the filename.
    """
    max_length = 100
    sanitized = filename.replace('/', '_').replace('\\', '_')
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized

def main(source_directory_path, result_directory_path):
    """
    Process all text files in the specified source directory for sentence segmentation,
    and save the tokenized results in the result directory.

    This function iterates through each text file in the source directory,
    tokenizes its content into sentences using the tokenize_file function,
    and writes the tokenized sentences to a new file in the result directory.
    It ensures that the result directory exists before processing files.

    Args:
    source_directory_path: Directory containing the original text files.
    result_directory_path: Directory where tokenized files will be saved.
    """
    if not os.path.exists(result_directory_path):
        os.makedirs(result_directory_path)

    for filename in os.listdir(source_directory_path):
        if filename.endswith('.txt'):
            source_file_path = os.path.join(source_directory_path, filename)
            sentences = tokenize_file(source_file_path)
            sanitized_filename = sanitize_filename(filename)
            result_file_path = os.path.join(result_directory_path, f"tokenized_{sanitized_filename}.txt")

            try:
                with open(result_file_path, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(sentences))
                print(f"Sentences for {filename} saved to {result_file_path}")
            except Exception as e:
                print(f"Error saving file {result_file_path}: {e}")

if __name__ == "__main__":
    # Define the source directory containing input text files and the
    # result directory where tokenized files will be saved.
    source_directory_path = r'Extracted_Articles_kr'
    result_directory_path = r'2.1_Extracted_Articles_kr'

    # Execute the main function to start the sentence tokenization process.
    main(source_directory_path, result_directory_path)
