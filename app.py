from utils import parse_transcript
import os

# Web app
from flask import Flask, render_template, request, redirect, url_for, flash 
app = Flask(__name__) 

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

    # Parse uploaded transcript into a Python dictionary
        transcript_data = parse_transcript(text)
        return render_template('transcript_display.html', filename=request.files['file'].filename, transcript_data=transcript_data)

    except Exception as e:
         flash('Error processing file: {e}', 'error')
         return redirect(url_for('index'))

def main():
    print("Running...")

if __name__ == '__main__':
    main()
    app.run(debug=True)  # Run the Flask app in debug mode if executed directly
