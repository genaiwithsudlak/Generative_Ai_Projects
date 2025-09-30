from pydub import AudioSegment

def combine_mp3_files(mp3_paths, output_path):
    """Merge multiple mp3 chunks into one final file."""
    combined = AudioSegment.empty()
    for p in mp3_paths:
        seg = AudioSegment.from_file(p)
        combined += seg
    combined.export(output_path, format="mp3")
    return output_path
