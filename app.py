from utils import parse_transcript, get_list_of_speakers, filter_by_speaker, calculate_airtimes, generate_pie_chart
import os

# Web app
from flask import Flask, render_template, request, redirect, url_for, flash, session 
app = Flask(__name__)
app.secret_key = os.urandom(16)

# Database
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transcripts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    transcript_data = db.Column(db.JSON, nullable=True)
    speakers = db.Column(db.JSON, nullable=True)  # Store list of unique speakers
    airtimes = db.Column(db.JSON, nullable=True)  # Store airtime data
    airtimes_chart_path = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Transcript {self.filename}>'

# Route for the home page
@app.route('/')  
def index():
    transcripts = Transcript.query.all() 
    return render_template('index.html', transcripts=transcripts)  

@app.route('/process_transcript_upload', methods=['POST'])
def process_transcript_upload_route():
    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        flash('No files selected', 'error')
        return redirect(url_for('index'))
    
    # debugging
    print("Files received:", len(files))
    for file in files:
        print("File name:", file.filename)

    processed_files = []
    for file in files:
        if not file.filename.endswith('.txt'):
            print(f'Invalid file type for {file.filename}. Please upload .txt files', 'error')
            continue  # Skip to the next file

        try:
            text = file.read().decode('utf-8')

             # Check if file already exists in the database
            existing_transcript = Transcript.query.filter_by(filename=file.filename).first()
            if existing_transcript:
                print(f'File {file.filename} already exists. Deleting and re-adding...')
                # If it exists, delete the existing record
                db.session.delete(existing_transcript)
                db.session.commit()  # Commit the delete before adding a new record
            
            # Save new transcript to database
            transcript_data = parse_transcript(text)
            speakers = get_list_of_speakers(transcript_data)
            airtimes = calculate_airtimes(transcript_data)
            airtimes_chart_path = generate_pie_chart(airtimes, file.filename)

            new_transcript = Transcript(
                filename=file.filename,
                text=text,
                transcript_data=transcript_data,
                speakers=speakers,
                airtimes=airtimes,
                airtimes_chart_path=airtimes_chart_path
                )
            db.session.add(new_transcript)
            '''
            print(transcript_data)
            print(speakers)
            print(airtimes)
            print(airtimes_chart_path)
            '''
            processed_files.append(file.filename)  # Keep track of successfully processed files
        except Exception as e:
            print(f'Error processing file {file.filename}: {e}', 'error')
    
    db.session.commit()  # Commit once after processing all files
    
    if not processed_files:
        # If no files were processed successfully, redirect to upload page
        print('No files processed')
        return redirect(url_for('index'))
    else:
        print(f'Successfully processed files: {", ".join(processed_files)}')

     # Assuming we've saved each transcript and have their IDs
        transcripts = Transcript.query.all() 

        # Re-render index page with updated list of transcripts
        return render_template('index.html', transcripts=transcripts)

# Display a single transcript
@app.route('/transcript/<int:transcript_id>')
def transcript_display_route(transcript_id):
    transcript = Transcript.query.get_or_404(transcript_id)
    transcript_data = transcript.transcript_data
    speakers = transcript.speakers

    return render_template('transcript_display.html', transcript_id=transcript_id, filename=transcript.filename, transcript=transcript, transcript_data=transcript_data, speakers=speakers)

@app.route('/delete_transcript/<int:transcript_id>', methods=['POST'])
def delete_transcript_route(transcript_id):
    transcript_to_delete = Transcript.query.get_or_404(transcript_id)

    airtimes_chart_path = os.path.join(app.static_folder, transcript_to_delete.airtimes_chart_path)
    if os.path.exists(airtimes_chart_path):
        os.remove(airtimes_chart_path) 
        print("Airtimes pie chart image deleted:", airtimes_chart_path)

    db.session.delete(transcript_to_delete)
    db.session.commit()
    print('Transcript deleted successfully')
    return redirect(url_for('index'))

@app.route('/delete_all_transcripts', methods=['POST'])
def delete_all_transcripts_route():
    try:
        transcripts = Transcript.query.all()
        for transcript in transcripts:
            airtimes_chart_path = os.path.join(app.static_folder, transcript.airtimes_chart_path)
            if os.path.exists(airtimes_chart_path):
                os.remove(airtimes_chart_path) 
                print("Airtimes pie chart image deleted:", airtimes_chart_path)

        # Deletes all transcripts from the database
        Transcript.query.delete()
        db.session.commit()
        print('All transcripts have been deleted successfully')
    except Exception as e:
        db.session.rollback()
        print(f'Error deleting transcripts: {e}')
    return redirect(url_for('index'))


@app.route('/filter_by_speaker/<int:transcript_id>', methods=['GET'])
def filter_by_speaker_route(transcript_id):
    selected_speaker = request.args.get('speaker')

    transcript = Transcript.query.get_or_404(transcript_id)
    transcript_data = transcript.transcript_data
    speakers = transcript.speakers
    filename = transcript.filename
    # No filtering
    if selected_speaker == 'Default':
        return render_template('transcript_display.html', transcript_id=transcript_id, filename=filename, transcript_data=transcript_data, speakers=speakers)
    
    # With filtering
    if selected_speaker:
        filtered_transcript = filter_by_speaker(transcript_data, selected_speaker)
        return render_template('transcript_display.html', transcript_id=transcript_id, filename=filename, transcript_data=filtered_transcript, speakers=speakers)

@app.route('/analyze_airtime/<int:transcript_id>', methods=['GET'])
def analyze_airtime_route(transcript_id):    
    transcript = Transcript.query.get_or_404(transcript_id)
    transcript_data = transcript.transcript_data
    speakers = transcript.speakers
    filename = transcript.filename
    airtimes = transcript.airtimes
    airtimes_chart_path = transcript.airtimes_chart_path
    total_airtime = sum(airtimes.values())

    # Sort airtimes in descending order
    sorted_airtimes = {k: v for k, v in sorted(airtimes.items(), key=lambda item: item[1], reverse=True)}

    return render_template('transcript_display.html', transcript_id=transcript_id, filename=filename, transcript_data=transcript_data, speakers=speakers, airtimes=sorted_airtimes, total_airtime=total_airtime, airtimes_chart_path=airtimes_chart_path)

@app.route('/search_all', methods=['GET'])
def search_all_route():
    search_query = request.args.get('search_query')

    matching_transcripts = Transcript.query.filter(
        Transcript.transcript_data.contains(search_query)).all()
    
    # Extract matching speeches from the transcripts
    search_results = []
    for transcript in matching_transcripts:
        for entry in transcript.transcript_data:
            if search_query.lower() in entry['speech'].lower():
                search_results.append({
                    'filename': transcript.filename,
                    'speaker': entry['speaker'],
                    'timestamp': entry['timestamp'],
                    'speech': entry['speech']
                })
    return render_template('search_results.html', 
                           search_results=search_results, 
                           search_query=search_query)

def main():
    print("Running...")
    with app.app_context():
        db.create_all()  # This creates the database tables

if __name__ == '__main__':
    main()
    app.run(debug=True)  # Run the Flask app in debug mode if executed directly
