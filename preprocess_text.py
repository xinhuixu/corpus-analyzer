# regex for removing punctuation!
import re
# nltk preprocessing magic
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from part_of_speech import get_part_of_speech


def preprocess_text(text):
 
        
        # Preprocess the text
        cleaned = re.sub('\W+', ' ', text)
        tokenized = word_tokenize(cleaned)

        stemmer = PorterStemmer()
        stemmed = [stemmer.stem(token) for token in tokenized]

        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized]

        return stemmed, lemmatized
       
# From Codecademy free course