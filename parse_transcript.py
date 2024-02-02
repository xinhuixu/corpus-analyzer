import re

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