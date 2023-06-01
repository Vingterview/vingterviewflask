import subprocess
import os

AUDIO_TEMP = "temp/"


def extract_audio(input_video_path, file_name):
    output_audio_path = AUDIO_TEMP + file_name + ".mp3"
    # audio stream만 copy -acodec copy
    command = f'ffmpeg -y -i {input_video_path} {output_audio_path}'
    subprocess.call(command, shell=True)
    return output_audio_path


def merge_audio2video(output_audio_path, input_video_path, store_file_name):
    output_video_path = "merge/" + store_file_name
    command = f'ffmpeg -y -i {input_video_path} -i {output_audio_path} -c:v copy -map 0:v:0 -map 1:a:0 -shortest {output_video_path}'
    subprocess.call(command, shell=True)

    return output_video_path


def remove_tempfile(tempfiles):
    for tempfile in tempfiles:
        os.remove(tempfile)


if __name__ == "__main__":
    output_audio_path = extract_audio("assets/driving-square.mp4", "example")
    merge_audio2video(output_audio_path, "result/3cf54a04-a7a6-4681-87b2-451ff9bb1d55.mp4",
                      "merge/3cf54a04-a7a6-4681-87b2-451ff9bb1d55merged.mp4")
