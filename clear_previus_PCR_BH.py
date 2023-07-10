import os


def get_text_file_paths(directory):
    # Get all files in the directory
    files = os.listdir(directory)

    # Filter out only the text files and get their full paths
    text_file_paths = [[os.path.join(directory, file), file] for file in files if file.endswith('.txt')]
    for i in range(len(text_file_paths)):
        if text_file_paths[i][1] == "ПЦР.txt":
            os.remove(text_file_paths[i][0])
            print("will delete ПЦР.txt")
        elif text_file_paths[i][1] == "БХ.txt":
            os.remove(text_file_paths[i][0])
            print("will delete БХ.txt")


directory = "C:/результат/"
get_text_file_paths(directory)
