# corpus-analyzer (under construction)
Analyze language classroom transcripts. Built for the [Language & Tech Research Group](https://sites.google.com/tc.columbia.edu/al-tesol-language-technology/projects/altec-learner-corpus?authuser=0) @ Teachers College.

## Installation guide (2/15/24)
![Installing-GIF](/static/corpus-analyzer-install-1-021524.gif)
![Running-GIF](/static/corpus-analyzer-install-2-021524.gif)
Prerequisites: [Python](https://www.python.org/) & [Git](https://github.com/git-guides/install-git) installed on your computer.

### Step 1: Clone the project
Open a terminal on your computer, then copy and paste the following commands:
   ```bash
   git clone https://github.com/xinhuixu/corpus-analyzer.git
   ```
### Step 2: Install libraries
After cloning, navigate to the project directory in your terminal, then install required Python libraries:
```bash
cd corpus-analyzer
```
   ```bash
   pip install -r requirements.txt
   ```
### Step 3: Run the application
   ```bash
   python app.py
   ```
 Then, open a web browser and go to http://127.0.0.1:5000/. 


## Transcripts database schema (3/2/24)

**Description:** Stores information about audio transcript files, including metadata and parsed content.

| Column Name           | Data Type | Description                                                                 | Example                                                                                                                                                                      | Constraints                |
|-----------------------|-----------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| `id`                  | Integer   | Automatically generated numerical identifier of the transcript.            |                                                                                                                                                                              | Primary Key, Auto-increment|
| `filename`            | String    | The name of the transcript file as uploaded.                                | `sample_transcript.txt`                                                                                                                                                      | NOT NULL, UNIQUE, 255 chars|
| `text`                | Text      | Raw text content of the transcript as uploaded.                             |                                                                                                                                                                              | NOT NULL                   |
| `transcript_data`     | JSON      | Structured representation of the parsed transcript content.                 | `[{"speaker": "Student 1", "timestamp": "00:00:10.500 - 00:00:12.300", "speech": "So, it's like saying 'brother' in English?"}, {"speaker": "Teacher 1", "timestamp": "00:00:12.310 - 00:00:16.789", "speech": "Exactly, but in our target language, the word carries more cultural significance."}]` | Nullable                   |
| `speakers`            | JSON      | List of unique speakers identified in the transcript.                       | `["Student 2", "Student 4", "Student 1", "Student 3", "Teacher 1"]`                                                                                                           | Nullable                   |
| `airtimes`            | JSON      | Summary of speaking times for each speaker.                                 | `{"Student 1": 5.1, "Teacher 1": 49.5, "Student 2": 4.0, "Student 3": 4.8, "Student 4": 5.5}`                                                                                 | Nullable                   |
| `airtimes_chart_path` | String    | File path to the generated pie chart visualizing speaker airtimes.          | `airtimes_chart_sample_transcript_2.txt.png`                                                                                                                                  | Nullable, 255 chars        |

