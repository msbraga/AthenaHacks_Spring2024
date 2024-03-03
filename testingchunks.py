import pydub


audio_file = "sup-bro.mp3"

def cut_audio_into_chunks(audio_file,chunk_length_seconds):
    audio_file = pydub.AudioSegment.from_file(audio_file)
    duration = int(audio_file.duration_seconds * 1000)
    chunks = []
    for i in range(0, duration, chunk_length_seconds * 1000):
        chunks.append(audio_file[i:i + chunk_length_seconds * 1000])
    return chunks
    

chunk_length_seconds = 10

chunks = cut_audio_into_chunks(audio_file, chunk_length_seconds)

for i, chunk in enumerate(chunks):
    chunk.export("chunk_{}.mp3".format(i), format="mp3")
print("Try programiz.pro")