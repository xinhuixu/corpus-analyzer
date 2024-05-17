import os, re
from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db, cache
from models import *
from utils import *
# from utils import parse_transcript, get_list_of_speakers, filter_by_speaker, calculate_airtimes, generate_pie_chart, calculate_total_words, invalidate_cache, get_or_set_cache

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Configurations
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Default cache timeout 5 minutes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transcripts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with the app
db.init_app(app)
cache.init_app(app)

# Route for the home page
@app.route('/')  
def index():
    transcripts = Transcript.query.all()
    total_words = get_or_set_cache('total_words', calculate_total_words)
   
    return render_template('index.html', 
                           transcripts=transcripts,
                           total_words=total_words)  

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
    invalidate_cache()

    if not processed_files:
        # If no files were processed successfully, redirect to upload page
        print('No files processed')
    else:
        print(f'Successfully processed files: {", ".join(processed_files)}')
    
    return redirect(url_for('index'))
    '''
        # Assuming we've saved each transcript and have their IDs
        transcripts = Transcript.query.all() 
        total_words = get_or_set_cache('total_words', calculate_total_words)
        # Re-render index page with updated list of transcripts
        return render_template('index.html', 
                               transcripts=transcripts,
                               total_words=total_words)
    '''
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
    invalidate_cache()
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
    invalidate_cache()
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

from flask import flash, redirect, url_for

@app.route('/aggregate_airtime_analysis', methods=['POST'])
def aggregate_airtime_analysis_route():
    aggregated_airtimes = aggregate_airtimes()
    generate_pie_chart(aggregated_airtimes, "aggregate")

    pie_chart_url = url_for('static', filename="airtimes_chart_aggregate.png")
 
    transcripts = Transcript.query.all()
    total_words = get_or_set_cache('total_words', calculate_total_words)
    
    sorted_airtimes = {k: v for k, v in sorted(aggregated_airtimes.items(), key=lambda item: item[1], reverse=True)}

    return render_template('index.html', 
                           transcripts=transcripts,
                           total_words=total_words,
                           pie_chart_url=pie_chart_url,
                           aggregated_airtimes=sorted_airtimes)

@app.route('/search_all', methods=['GET'])
def search_all_route():
    search_query = request.args.get('search_query')
    search_mode = request.args.get('search_mode')
    
    if search_mode == 'whole_word': # EX: "are" returns "Are you..." but not "grandparents"
        matching_transcripts = Transcript.query.all()
    elif search_mode == 'partial_match': # Every transcript that has partial match
        matching_transcripts = Transcript.query.filter(
            Transcript.transcript_data.contains(search_query)).all()
    
    # Extract matching speeches from the transcripts
    search_results = []
    for transcript in matching_transcripts:
        for entry in transcript.transcript_data:
            # Check the speech for the search query based on the search mode
            if search_mode == 'whole_word':
                if re.search(r'\b{}\b'.format(re.escape(search_query)), entry['speech'], re.IGNORECASE):
                    search_results.append({
                        'filename': transcript.filename,
                        'speaker': entry['speaker'],
                        'timestamp': entry['timestamp'],
                        'speech': highlight_search_term(entry['speech'], search_query, search_mode)
                    })
            elif search_mode == 'partial_match':
                if search_query.lower() in entry['speech'].lower():
                    search_results.append({
                        'filename': transcript.filename,
                        'speaker': entry['speaker'],
                        'timestamp': entry['timestamp'],
                        'speech': highlight_search_term(entry['speech'], search_query, search_mode)
                    })
    
    return render_template('search_results.html', 
                           search_results=search_results, 
                           search_query=search_query,
                           search_mode=search_mode)

def main():
    print("Running...")
    with app.app_context():
        db.create_all()  # This creates the database tables

if __name__ == '__main__':
    main()
    app.run(debug=True)  # Run the Flask app in debug mode if executed directly
