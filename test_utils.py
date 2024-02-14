from utils import calculate_airtimes

sample_transcript_data = [
    {'speaker': 'Speaker 1', 'timestamp': '00:00:10.000 - 00:00:15.000'},
    {'speaker': 'Speaker 2', 'timestamp': '00:00:15.500 - 00:00:20.000'},
    {'speaker': 'Speaker 1', 'timestamp': '00:00:20.500 - 00:00:24.276'}
]

def test_calculate_airtimes():
    airtimes = calculate_airtimes(sample_transcript_data)
    for speaker, duration in airtimes.items():
        print(f"{speaker}: {duration} seconds")

if __name__ == "__main__":
    test_calculate_airtimes()