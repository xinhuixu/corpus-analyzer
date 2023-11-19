# regex for removing punctuation!
import re
# nltk preprocessing magic
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from part_of_speech import get_part_of_speech
from download_text_files import download_text_files

import os

# web app
from flask import Flask, render_template, request, redirect, url_for 
app = Flask(__name__) 

# Define a route for the home page
@app.route('/')  
def index():
    return render_template('index.html')  

 # Define a route for processing text when the form is submitted
@app.route('/preprocess_text', methods=['POST']) 
def preprocess_text():
    if request.method == 'POST':  
        # Get the text from the submitted form
        text = request.form['text']  
        
        # Preprocess the text
        cleaned = re.sub('\W+', ' ', text)
        tokenized = word_tokenize(cleaned)

        stemmer = PorterStemmer()
        stemmed = [stemmer.stem(token) for token in tokenized]

        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized]

        # Render the HTML template with the original text, stemmed text, and lemmatized text
        return render_template('index.html', original_text=text, stemmed_text=stemmed, lemmatized_text=lemmatized)

# Define a route for downloading text files when user submits url
@app.route('/download_text_files_main', methods=['POST'])
def download_text_files_main():
    if request.method == 'POST':
        user_url = request.form['url']

        download_folder = 'downloaded_text_files'

        download_text_files(user_url, download_folder)
        success_message = f"Download completed successfully for URL: {user_url}. " \
            f"Files saved in folder: {download_folder}"
        
       # This was bad because I didn't re-render the template, so msg did not show up! 
       # return redirect(url_for('index', success_message=success_message))
        return render_template('index.html', success_message=success_message)

    # If the request is not a POST, redirect to the index page
    return redirect(url_for('index'))



# Builds a corpus from .txt documents in a folder
def build_corpus(folder_path):
    # Initialize an empty list to store the text content of each document
    corpus = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
             # Construct the full path to the file
            file_path = os.path.join(folder_path, filename)

            # Open the file in read mode with utf-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

                #Append the text content to the corpus list
                corpus.append(text)

    return corpus

    
def main():
    folder_path = 'source_text_1'

    corpus = build_corpus(folder_path)

    # Print the first 10 characters of each document in the corpus
    for i, document in enumerate(corpus):
        print(f"Document {i + 1}: {document[:10]}...")



if __name__ == '__main__':
    main()

    app.run(debug=True)  # Run the Flask app in debug mode if executed directly


'''
text = "So many squids are jumping out of suitcases these days that you can barely go anywhere without seeing one burst forth from a tightly packed valise. I went to the dentist the other day, and sure enough I saw an angry one jump out of my dentist's bag within minutes of arriving. She hardly even noticed."

cleaned = re.sub('\W+', ' ', text)
tokenized = word_tokenize(cleaned)

stemmer = PorterStemmer()
stemmed = [stemmer.stem(token) for token in tokenized]

## -- CHANGE these -- ##
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized]

print("Stemmed text:")
print(stemmed)
print("\nLemmatized text:")
print(lemmatized)
'''