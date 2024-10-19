import random

def insert_multiple_random_media_lines(file_path):
    # Step 1: Generate the media lines and duplicate each 3 times
    media_lines = [f"media:./media/med{i}.mp4\n" for i in range(31, 55)] * 3
    
    # Step 2: Shuffle the lines randomly
    random.shuffle(media_lines)

    # Step 3: Read the existing lines in the file
    with open(file_path, 'r') as file:
        existing_lines = file.readlines()

    # Step 4: Merge the existing lines with the shuffled media lines
    combined_content = existing_lines + media_lines

    # Shuffle the entire content to randomly distribute the media lines
    random.shuffle(combined_content)

    # Step 5: Write the new content back to the file
    with open(file_path, 'w') as file:
        file.writelines(combined_content)

# Replace 'your_file.txt' with the path to your text file
insert_multiple_random_media_lines('msg.txt')
