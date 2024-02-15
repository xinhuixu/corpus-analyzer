import re
#import spacy
#from spacy import displacy
#from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime
from collections import defaultdict

'''
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
'''

# Parse transcript text (assumes ELAN format)
# Return [{'speaker': ____, 'speech':___, 'timestamp':____}, {...}]
def parse_transcript(text):
    # Compile a regular expression pattern to match speaker names (Student or Teacher followed by a digit),
    # followed by their speech, and then a timestamp in a specific format.
    pattern = re.compile(r"^(Student \d+|Teacher \d+)\s+(.*?)\n\s+(\d{2}:\d{2}:\d{2}\.\d{3}\s*-\s*\d{2}:\d{2}:\d{2}\.\d{3})", re.MULTILINE | re.DOTALL)
   
    transcript_data = []
   
    # Use the compiled pattern to find all matches (segments) in the text
    for match in pattern.finditer(text):
        # Extract speaker, speech, and timestamp from each match
        speaker, speech, timestamp = match.groups()

        transcript_data.append({
            "speaker": speaker.strip(),
            "timestamp": timestamp.strip(),
            "speech": speech.strip().replace('\n', ' ')
        })
    return transcript_data

def filter_by_speaker(transcript_data, speaker):
    filtered_data = [entry for entry in transcript_data if entry['speaker'] == speaker]
    return filtered_data

def get_list_of_speakers(transcript_data):
      # Set automatically enforce uniqueness
      speakers_set = {entry['speaker'] for entry in transcript_data}
      unique_speakers = list(speakers_set)
      return unique_speakers


def calculate_airtimes(transcript_data):
    airtimes = defaultdict(float)
    # When accessing or modyfing a key that doesn't exist,
    # defaultdict automatically creates an entry for that key (0) 

    for entry in transcript_data:
        speaker = entry['speaker']
        timestamp = entry['timestamp']
        start_time, end_time = timestamp.split(' - ')

        # Convert timestamps to datetime objects
        format = '%H:%M:%S.%f'
        start = datetime.strptime(start_time, format)
        end = datetime.strptime(end_time, format)

        # Calculate duration and add to speaker's total airtime
        duration = (end - start).total_seconds()
        airtimes[speaker] += duration

    # Round the durations
    rounded_airtimes = {speaker: round(duration, 1) for speaker, duration in airtimes.items()}
    return rounded_airtimes


def generate_pie_chart(airtimes):
    labels = airtimes.keys()
    sizes = airtimes.values()

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', textprops={'fontsize': 18})
    plt.title('Distribution of Airtime by Speaker', fontsize=20)

    pie_chart_filename = 'pie_chart.png'
    plt.savefig(f'static/{pie_chart_filename}')

    print("Pie chart image saved:", pie_chart_filename)
    return pie_chart_filename