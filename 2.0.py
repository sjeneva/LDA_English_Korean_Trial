import os

def process_files(input_directory, output_directory):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Define patterns to filter out
    patterns_to_filter = [
        '_', '[', '*', '*[', '* [', '"  * [', '"', '-', '## [', '![](', '](', '![', '##### ', '- ', '](', '# **[![',
        'Copyright ⓒ', '보기](/', '검색어를 입력해주세요. 검색하기', '검색', '닫기', 'URL복사', '(', '![](', '###', '##',
        '#  [ ![', '스크롤', '기사보내기', '이 ', '저작권자', '라이브리', '기사검색 _검색_', '개최]'
    ]

    # Loop through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            input_filepath = os.path.join(input_directory, filename)
            output_filepath = os.path.join(output_directory, filename)

            # Handle long paths on Windows
            if os.name == 'nt':
                input_filepath = r'\\?\\' + os.path.abspath(input_filepath)
                output_filepath = r'\\?\\' + os.path.abspath(output_filepath)

            try:
                with open(input_filepath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                print(f"Skipping file due to encoding error: {filename}")
                continue

            # Remove first 25 and last 100 lines
            if len(lines) > 125:
                lines = lines[25:-100]
            else:
                print(f"Skipping file due to insufficient lines after removal: {filename}")
                continue

            # Filter out lines that start with specified patterns
            filtered_lines = []
            for line in lines:
                if not any(line.strip().startswith(pattern) for pattern in patterns_to_filter):
                    filtered_lines.append(line)

            # Ensure the directory for the output file exists
            output_dir = os.path.dirname(output_filepath)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            # Write the filtered lines to the new file in the output directory
            with open(output_filepath, 'w', encoding='utf-8') as file:
                file.writelines(filtered_lines)

            print(f"Processed file: {filename} -> {output_directory}")

# Replace 'source_directory_path' and 'result_directory_path' with the actual paths to your directories
source_directory_path = r'2.0_Extracted_Articles_kr'
result_directory_path = r'2.1_Extracted_Articles_kr'
process_files(source_directory_path, result_directory_path)
