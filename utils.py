import os
from moviepy.editor import VideoFileClip
import click


@click.command()
@click.option("--path", "-p", prompt="Enter the path to the MP4 file")
def mp4_to_mp3(path):
    try:
        # Check if the input file exists
        if not os.path.isfile(path):
            raise FileNotFoundError(f"The file '{path}' does not exist.")

        # Get the file's base name without extension
        base_name = os.path.splitext(os.path.basename(path))[0]

        # Set the output MP3 file path
        output_path = os.path.join(
            os.path.dirname(path), f"{base_name}.mp3")

        # Convert the MP4 file to MP3
        video_clip = VideoFileClip(path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_path)

        # Close the clips
        audio_clip.close()
        video_clip.close()

        print(f"Conversion successful. MP3 file saved as '{output_path}'")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    mp4_to_mp3()
