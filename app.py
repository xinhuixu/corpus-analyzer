from utils import parse_transcript, get_list_of_speakers, filter_by_speaker
import os

# Web app
from flask import Flask, render_template, request, redirect, url_for, flash, session 
app = Flask(__name__)
app.secret_key = os.urandom(16)

# Route for the home page
@app.route('/')  
def index():
    return render_template('index.html')  

# For transcript file upload
@app.route('/process_transcript_upload', methods=['POST'])
def process_transcript_upload_route():
    if 'file' not in request.files or request.files['file'].filename =='':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if not file.filename.endswith('.txt'):
            flash('Invalid file type. Please upload a .txt file', 'error')
            return redirect(url_for('index'))
    
    try:
        text = file.read().decode('utf-8')
        print("Text file uploaded:", text)

    # Parse uploaded transcript into a Python dictionary and store in session
        transcript_data = parse_transcript(text)
        session['transcript_data'] = transcript_data

        speakers = get_list_of_speakers(transcript_data)
        session['speakers'] = speakers

        filename = request.files['file'].filename
        session['filename'] = filename

        return render_template('transcript_display.html', filename=filename, transcript_data=transcript_data, speakers=speakers)

    except Exception as e:
         flash('Error processing file: {e}', 'error')
         return redirect(url_for('index'))

@app.route('/filter_by_speaker', methods=['GET'])
def filter_by_speaker_route():
    selected_speaker = request.args.get('speaker')
    print("SELECTED SPEAKER: ", selected_speaker)
    transcript_data = session.get('transcript_data', [])
    speakers = session.get('speakers', [])
    filename = session.get('filename')

    # No filtering
    if selected_speaker == 'Default':
        return render_template('transcript_display.html', filename=filename, transcript_data=transcript_data, speakers=speakers)
    
    # With filtering
    if selected_speaker:
        filtered_transcript = filter_by_speaker(transcript_data, selected_speaker)
        print("Filtered transcript:", filtered_transcript)
        return render_template('transcript_display.html', filename=filename, transcript_data=filtered_transcript, speakers=speakers)

def main():
    print("Running...")

if __name__ == '__main__':
    main()
    app.run(debug=True)  # Run the Flask app in debug mode if executed directly
