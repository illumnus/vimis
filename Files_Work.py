import os


def get_text_file_paths(directory):
    # Get all files in the directory
    files = os.listdir(directory)

    # Filter out only the text files and get their full paths
    text_file_paths = [[os.path.join(directory, file), file] for file in files if file.endswith('.txt')]

    # Return the file paths if there are any
    if len(text_file_paths) == 1:
        if text_file_paths[0][1] == "ПЦР.txt":
            return text_file_paths[0][0], "ПЦР"
        elif text_file_paths[0][1] == "ТМС.txt":
            return text_file_paths[0][0], "ТМС"
    else:
        return None, None
