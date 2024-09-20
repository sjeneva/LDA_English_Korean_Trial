import os
import re

def extract_keywords_context(text, keywords, context_range=2):
    lines = text.split('\n')
    keyword_contexts = []

    for i, line in enumerate(lines):
        for keyword in keywords:
            if keyword in line:
                start = max(0, i - context_range)
                end = min(len(lines), i + context_range + 1)
                context = lines[start:end]
                keyword_contexts.append({
                    'keyword': keyword,
                    'context': context
                })
                print(f"Found keyword '{keyword}' in line {i}: {line}")  # Debugging print
    return keyword_contexts

# Directory containing the text files
directory = r'C:\Users\1234\OneDrive - 인하대학교\바탕 화면\ESGL_Korean\LDA_English_Korean\Extracted_Articles'  # Replace with the actual path

# Ensure the directory exists
if not os.path.exists(directory):
    raise FileNotFoundError(f"The directory {directory} does not exist")

# Keywords to search for
keywords = ['ESG', 'environmental', 'sustainability', 'greenwashing']

# Process each text file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"Reading file: {filename}")  # Debugging print

            # Extract contexts for the current article
            contexts = extract_keywords_context(content, keywords)
            if not contexts:
                print(f"No keywords found in the article: {filename}")  # Debugging print

            # Write the results to a text file named after the input file
            output_filename = os.path.splitext(filename)[0] + '_keyword_contexts.txt'
            output_filepath = os.path.join(directory, output_filename)
            with open(output_filepath, 'w', encoding='utf-8') as f:
                for context in contexts:
                    f.write(f"Keyword: {context['keyword']}\n")
                    f.write("Context:\n")
                    f.write("\n".join(context['context']) + "\n")
                    f.write("\n" + "=" * 80 + "\n")
                f.flush()
                os.fsync(f.fileno())

            print(f"Results for {filename} have been written to {output_filepath}")

            # Verify if the file was created
            if os.path.isfile(output_filepath):
                print(f"File {output_filepath} created successfully.")
            else:
                print(f"File {output_filepath} was not created.")
