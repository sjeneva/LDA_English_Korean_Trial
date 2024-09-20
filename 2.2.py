import os
import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def read_file(file_path):
    """
    Read the content of a file and return it.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def remove_duplicates(file_content):
    """
    Remove duplicate lines from the file content.
    """
    unique_content = set(file_content)
    return list(unique_content)

def preprocess_line(line, stop_words):
    """
    Remove stop words from a line of text.
    """
    tokens = nlp(line)
    cleaned_tokens = [token.text for token in tokens if token.text.lower() not in stop_words]
    return " ".join(cleaned_tokens)

def process_files(source_directory, result_directory):
    """
    Process files to remove duplicates and stop words, then save the results.
    """
    # Ensure the result directory exists
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    stop_words = nlp.Defaults.stop_words  # Get spaCy's default English stop words

    for filename in os.listdir(source_directory):
        if filename.endswith('.txt'):
            source_file_path = os.path.join(source_directory, filename)
            result_file_path = os.path.join(result_directory, filename)

            # Read the content of the source file
            content = read_file(source_file_path)

            # Remove duplicate lines from the content
            cleaned_content = remove_duplicates(content)

            # Remove stop words from each line
            cleaned_lines = [preprocess_line(line, stop_words) for line in cleaned_content]

            # Save the cleaned content to the result file
            with open(result_file_path, 'w', encoding='utf-8') as file:
                file.writelines("\n".join(cleaned_lines))

            print(f"Processed and saved cleaned file: {filename}")

if __name__ == "__main__":
    # Directories: You have a source directory with the tokenized texts (`Tokenized_Texts`)
    # and a result directory where the cleaned (duplicate-free) texts will be saved (`Cleaned_Texts`).
    source_directory = r'Extracted_Articles_kr'
    result_directory = r'2.2_Extracted_Articles_kr'
    process_files(source_directory, result_directory)
