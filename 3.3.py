import os
import re
from konlpy.tag import Okt  # Using Okt tokenizer from konlpy
from gensim import corpora, models


# Function to read text from a file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Function to sanitize filenames
def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)[:100]


# Path to the input and output directories
input_dir = r'2.6_Extracted_Articles_ENG'
output_dir = r'3.3_Extracted_Articles_ENG'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set up Korean tokenizer and stopwords
tokenizer = Okt()
stop_words = set()

# Process each file
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        try:
            file_path = os.path.join(input_dir, filename)
            text = read_text_file(file_path)

            # Check if the text is empty
            if not text.strip():
                print(f"Skipping empty file: {filename}")
                continue

            processed_text = tokenizer.morphs(text)
            filtered_text = [word for word in processed_text if word not in stop_words]

            # Check if the filtering results in an empty list
            if not filtered_text:
                print(f"No tokens after processing for file: {filename}")
                continue

            dictionary = corpora.Dictionary([filtered_text])
            corpus = [dictionary.doc2bow(filtered_text)]

            if not corpus:
                print(f"Empty corpus for file: {filename}")
                continue

            lda_model = models.LdaModel(
                corpus=corpus,
                id2word=dictionary,
                num_topics=2,
                random_state=100,
                update_every=1,
                chunksize=1000,
                passes=1000,
                alpha='auto',
                per_word_topics=True
            )

            sanitized_filename = sanitize_filename(filename)
            output_filepath = os.path.join(output_dir, f'topics_{sanitized_filename}')

            # Ensure the output directory exists
            output_file_dir = os.path.dirname(output_filepath)
            if not os.path.exists(output_file_dir):
                os.makedirs(output_file_dir)

            with open(output_filepath, 'w', encoding='utf-8') as f:
                for idx in range(lda_model.num_topics):
                    words_and_probs = lda_model.show_topic(idx, topn=5)
                    formatted_topic = ", ".join([f"{word} ({prob:.2f})" for word, prob in words_and_probs])
                    f.write(f"Topic {idx}: {formatted_topic}\n")

            print(f"Processed and saved: {filename}")
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")

print(f"Topics saved to the directory: {output_dir}")
