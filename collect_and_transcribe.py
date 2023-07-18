import time
import re
import os
import json
import librosa
import whisper
import youtube_dl



MODEL = whisper.load_model("base.en")


def download_and_transcribe(youtube_url):

    print("Downloading..." + youtube_url)

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'view_count': True,
        'upload_date': True,
        'channel': True,
        'title': True,
        'channel_id': True,
        'id': True
    }

    video_details = ""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_details = ydl.extract_info(youtube_url, download=True)

    print("Video Downloaded")

    channel_id = video_details['channel_id']
    channel_name = video_details['channel']
    channel_url = "https://www.youtube.com/@" + channel_name.replace(" ", "")
    video_id = video_details['id']
    video_title = video_details['title']
    video_view_count = video_details['view_count']
    video_upload_date = video_details['upload_date']

    file_path = ydl.prepare_filename(video_details)
    file_path = file_path.replace('.webm', '.mp3')
    file_path = file_path.replace('.m4a', '.mp3')

    print("Transcribing...")

    duration = librosa.get_duration(filename=file_path)
    start = time.time()
    result = MODEL.transcribe(file_path)
    end = time.time()
    seconds = end - start

    print("Video length:", duration, "seconds")
    print("Transcription time:", seconds)

    # Split result["text"]  on !,? and . , but save the punctuation
    sentences = re.split("([!?.])", result["text"])

    # Join the punctuation back to the sentences
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    transcription = "\n".join(sentences)

    data = {
        "channel_id": channel_id,
        "channel_name": channel_name,
        "channel_url": channel_url,
        "video_id": video_id,
        "video_url": youtube_url,
        "video_title": video_title,
        "video_view_count": video_view_count,
        "video_upload_date": video_upload_date,
        "transcription": transcription
    }

    transcriptions_file_path = "".join(file_path) + ".txt"
    transcriptions_file_path = "transcriptions/" + transcriptions_file_path
    json_file_path = "json/" + file_path + ".json"

    with open(transcriptions_file_path, "w") as output_transcription_file:
        output_transcription_file.write(transcription)

    with open(json_file_path, "w") as out_json_file:
        json.dump(data, out_json_file, indent=4)


    print("\n\n", "-"*100, "\nYour transcript is here:", transcriptions_file_path)
    os.remove(file_path)

#download_and_transcribe("https://www.youtube.com/watch?v=CnT-Na1IeVI")

with open('cooking_recipe_youtube_videos.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    print("["+line+"]")
    try:
        download_and_transcribe(line)
    except Exception as exception:
        print("An unknown error occurred")
        print("Retry the download and transcribe process for this video later " + line)
        print(exception)
