from preprocess_text import preprocess, lemmatize, make_word_cloud, visualize_dependency
from download_text_files import download_text_files
from build_corpus import build_corpus

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
def preprocess_text_route():
    if request.method == 'POST':  
        # Get the text from the submitted form
        text = preprocess(request.form['text'])
        print("Route text:", text)
        lemmatized_text = lemmatize(text)
        wordcloud_img = make_word_cloud(lemmatized_text)
        dependency = visualize_dependency(text)

        # return render_template('index.html', original_text=text, stemmed_text=stemmed, lemmatized_text=lemmatized, wordcloud_img=img_data)
        return render_template('index.html', original_text=text, lemmatized_text=lemmatized_text, wordcloud_img=wordcloud_img, dependency=dependency)

# Define a route for downloading text files when user submits url
@app.route('/download_text_files', methods=['POST'])
def download_text_files_route():
    if request.method == 'POST':
        user_url = request.form['url']

        download_folder = 'downloaded_text_files'

        download_text_files(user_url, download_folder)
        success_message = f"Download completed successfully for URL: {user_url}. " \
            f"Files saved in folder: {download_folder}" \
        
       # This was bad because I didn't re-render the template, so msg did not show up! 
       # return redirect(url_for('index', success_message=success_message))
        return render_template('index.html', success_message=success_message)

    # If the request is not a POST, redirect to the index page
    return redirect(url_for('index'))


# Builds a corpus from .txt documents in a folder
@app.route('/build_corpus', methods=['POST'])
def build_corpus_route():
    try:
        folder_path = request.form['folder_path']
    except KeyError:
        return render_template('index.html', build_corpus_msg="KeyError: 'folder_path' not found in form data.")

    # Call build_corpus with the provided folder_path
    corpus, build_corpus_msg = build_corpus(folder_path)

    return render_template('index.html', corpus=corpus, build_corpus_msg=build_corpus_msg)
    
def main():
    print("Running...")


if __name__ == '__main__':
    main()

    app.run(debug=True)  # Run the Flask app in debug mode if executed directly
