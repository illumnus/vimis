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
        elif text_file_paths[0][1] == "ПЦР_ВИМИС.txt":
            return text_file_paths[0][0], "ПЦР_ВИМИС"
        elif text_file_paths[0][1] == "ТМС_ВИМИС.txt":
            return text_file_paths[0][0], "ТМС_ВИМИС"
    else:
        return None, None

def get_unsuccess(Laboratory_CODE):

    if Laboratory_CODE == "ТМС_ВИМИС":
        file_path = "Files/TMC_unsuccess.txt"
    elif Laboratory_CODE == "ПЦР_ВИМИС":
        file_path = "Files/MGI_unsuccess.txt"

    with open(file_path, "r") as f:
        text = f.read().split("\n")
        for i in range(len(text)):
            text[i] = text[i].split("\t")
        return text