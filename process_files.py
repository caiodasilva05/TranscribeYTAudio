import os
import glob
import json

# Directory to list files from
input_directory = "transcriptions/"

# Directory to save json files
output_directory = "json/"

def parse_file_and_create_json(file_name, outfile):

    # Extract text before the first underscore

    file_name_without_path = file_name.replace("transcriptions\\", "")
    channel_title = file_name_without_path.split("_")[0]
    channel_url = "https://www.youtube.com/@" + channel_title.replace(" ", "")

    # Extract text between the first underscore and ".mp3"
    video_title = file_name.split("_", 1)[1].split(".mp3")[0]

    # Open the file and read its contents
    with open(file_name, "r") as f:
        transcription = f.read()

    # Save the title and videoTitle in a JSON file
    data = {"channel_title": channel_title, "channel_url" : channel_url,  "video_title": video_title, "transcription": transcription}
    with open(outfile, "w") as f:
        json.dump(data, f, indent=4)




# Get all files with the .txt extension
txt_files = glob.glob(os.path.join(input_directory, "*.txt"))

# Print the list of files
i=1
for txt_file in txt_files:
    print(txt_file)
    parse_file_and_create_json(txt_file, output_directory + f"{i}.json")
    i += 1
