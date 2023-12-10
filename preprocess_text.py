# regex for removing punctuation!
import re
# nltk preprocessing magic
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import spacy
from spacy import displacy

from part_of_speech import get_part_of_speech

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def preprocess(text):
        cleaned = re.sub('\W+', ' ', text)

        # Load spaCy English model
        nlp = spacy.load('en_core_web_sm')
    
        # Process the cleaned text with spaCy
        doc = nlp(cleaned)

        return doc
      
def lemmatize(doc):
    # Extract lemmatized tokens
    lemmatized = [token.lemma_ for token in doc]
    return lemmatized

'''def preprocess_text(text):
        
        # Preprocess the text
        cleaned = re.sub('\W+', ' ', text)
        tokenized = word_tokenize(cleaned)

        stemmer = PorterStemmer()
        stemmed = [stemmer.stem(token) for token in tokenized]

        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized]

        return stemmed, lemmatized
       
# preprocess_text is from a Codecademy free course
'''

def make_word_cloud(list_of_words):
                # Generate word cloud from list of words
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(list_of_words))

        # Save the word cloud image to a BytesIO object
        img_buffer = BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        img_buffer.seek(0)

        # Encode the image as base64 to embed in the HTML
        img_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return img_data

def visualize_dependency(doc):
       return displacy.render(doc, style="dep", options={'distance': 120}, jupyter=False)