import re
import spacy
from spacy import displacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

  # Load spaCy English model
nlp = spacy.load('en_core_web_sm')

def preprocess(text):
        cleaned = re.sub('[\n\t]+', ' ', text)
        doc = nlp(cleaned)
        return doc
      
def lemmatize(doc):
    # Extract lemmatized tokens excluding punctuations and whitespace
    lemmatized = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    return lemmatized

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
       # return displacy.render(doc, style="dep", options={'distance': 120}, jupyter=False)
        sentence_visualizations = []
        for sent in doc.sents:
                 # Process each sentence separately
                print("Processing Sentence:", sent.text)
                sent_doc = nlp(sent.text)
                
                visualize_data = displacy.render(sent_doc, style="dep", options={'distance': 120}, jupyter=False)
                sentence_visualizations.append(visualize_data)
        
        return sentence_visualizations

# Parse transcript text
def parse_transcript(text):
    pattern = re.compile(r"^(Student \d+|Teacher \d+)\s+(.*?)\n\s+(\d{2}:\d{2}:\d{2}\.\d{3}\s*-\s*\d{2}:\d{2}:\d{2}\.\d{3})", re.MULTILINE | re.DOTALL)
    transcript_data = []
    for match in pattern.finditer(text):
        speaker, speech, timestamp = match.groups()
        transcript_data.append({
            "speaker": speaker.strip(),
            "timestamp": timestamp.strip(),
            "speech": speech.strip().replace('\n', ' ')
        })
    return transcript_data