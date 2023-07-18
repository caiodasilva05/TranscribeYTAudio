import time
import re
import os
import json
import librosa
import whisper
from pytube import YouTube
import os
from pathlib import Path, PureWindowsPath



MODEL = whisper.load_model("base.en")


def download_and_transcribe(youtube_url):

    print("Downloading..." + youtube_url)

    video_details = ""
    youtube_content = YouTube(youtube_url)
    
    print("Video Downloaded")

    channel_id = youtube_content.channel_id
    channel_url = youtube_content.channel_url
    video_title = youtube_content.title
    video_view_count = youtube_content.views
    video_upload_date = youtube_content.publish_date

    audio_streams = youtube_content.streams.filter(only_audio = True, subtype="mp4")
    file_path = audio_streams[0].download()
    file_name = os.path.basename(file_path)
    duration = youtube_content.length
    print("Transcribing...")

    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    print("Video transcribed")
    print("Video length:", duration, "seconds")
    print("result="+result)

    # Split result["text"]  on !,? and . , but save the punctuation
    sentences = re.split("([!?.])", result["text"])

    # Join the punctuation back to the sentences
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    transcription = "\n".join(sentences)

    data = {
        "channel_id": channel_id,
        "channel_url": channel_url,
        #"video_id": video_id,
        "video_url": youtube_url,
        "video_title": video_title,
        "video_view_count": video_view_count,
        "video_upload_date": video_upload_date,
        "transcription": transcription
    }

    transcriptions_file_path = "".join(file_path) + ".txt"
    transcriptions_file_path = "\"" + "transcriptions/" + transcriptions_file_path + "\""
    print(transcriptions_file_path)
    json_file_path = "json/" + file_path + ".json"
    print(json_file_path)

    with open(transcriptions_file_path, "w") as output_transcription_file:
        output_transcription_file.write(transcription)

    with open(json_file_path, "w") as out_json_file:
        json.dump(data, out_json_file, indent=4)


    print("\n\n", "-"*100, "\nYour transcript is here:", transcriptions_file_path)
    os.remove(file_path)

#test
download_and_transcribe("https://www.youtube.com/watch?v=CnT-Na1IeVI")

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
