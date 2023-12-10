# nlp-playground
Analyze text files from the internet or on your computer.

## Usable features
- Download all text files (*.txt) from a specified webpage to a user-defined folder.
- Transform text from user input to dictionary-like data.

## Target features
- Transform text files in a folder to dictionary-like data.
- Download visible text data from specified webpage.
- More analysis and visualization options.
## Folder structure
```
NLP-playground/
│
├── downloaded_text_files/    
├── templates/        # HTML templates
├── app.py            # Main application file 
├── build_corpus.py   
├── download_text_files.py  
├── part_of_speech.py 
├── preprocess_text.py
├── requirements.txt  # Python dependencies
└── devlog.md         # Development log
```

## Installation

   ```bash
   git clone https://github.com/xinhuixu/nlp-playground.git
   pip install -r requirements.txt
   python app.py
   # Open your web browser and go to http://127.0.0.1:5000/.
```
Alternatively, follow these steps to run this web app on your computer.

### Prerequisites

1. **Python Installed:**
    - You can download it from [python.org](https://www.python.org/downloads/).

### Step 1: Download the Code

1. Click on the <b>green "Code" button</b> on GitHub and select "Download ZIP."
2. Extract the downloaded ZIP file to a location on your computer.

### Step 2: Open a Terminal

1. **Windows:**
    - Press `Win + R`, type `cmd`, and press Enter.
2. **Mac:**
   - Press `Cmd + Space`, type `Terminal`, and press Enter.

### Step 3: Navigate to the App Directory

1. Use the `cd` command to navigate to the directory where you extracted the ZIP file.
   ```bash
   cd /Users/yourusername/Downloads/nlp-playground #in Mac

### Step 4: Install Dependencies
1. Install the additional tools this app needs to run.
    ```bash
    pip install -r requirements.txt


### Step 5: Run the App
1. Run the following command to start the app.
    ```bash
    python app.py
2. <b>Open your web browser and go to http://127.0.0.1:5000/. You should now see the web app in your browser!

