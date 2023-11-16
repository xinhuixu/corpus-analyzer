# regex for removing punctuation!
import re
# nltk preprocessing magic
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
# grabbing a part of speech function:
from part_of_speech import get_part_of_speech

# web app
from flask import Flask, render_template, request 
app = Flask(__name__) 

@app.route('/')  # Define a route for the home page
def index():
    return render_template('index.html')  # Render the HTML template for the home page

@app.route('/preprocess_text', methods=['POST'])  # Define a route for processing text when the form is submitted
def preprocess_text():
    if request.method == 'POST':  
        text = request.form['text']  # Get the text from the submitted form
        # Preprocess the text
        cleaned = re.sub('\W+', ' ', text)
        tokenized = word_tokenize(cleaned)

        stemmer = PorterStemmer()
        stemmed = [stemmer.stem(token) for token in tokenized]

        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized]

        # Render the HTML template with the original text, stemmed text, and lemmatized text
        return render_template('index.html', original_text=text, stemmed_text=stemmed, lemmatized_text=lemmatized)

if __name__ == '__main__':
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