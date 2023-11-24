import os

def build_corpus(folder_path):
    # Initialize an empty list to store the text content of each document
    corpus = []

    # Check if the folder exists
    if not os.path.exists(folder_path):
        return [], f"The folder '{folder_path}' does not exist."

    # Check if the folder is empty
    if not os.listdir(folder_path):
        return [], f"The folder '{folder_path}' is empty."

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # Construct the full path to the file
            file_path = os.path.join(folder_path, filename)

            # Open the file in read mode with utf-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

                # Append the text content to the corpus list
                corpus.append(text)

    # Check if corpus is empty
    if not corpus:
        return [], "Corpus is empty; no .txt files in folder."
    else:
        return corpus, "Corpus built."