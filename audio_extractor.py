import argparse
import yt_dlp as youtube_dl
from pydub import AudioSegment

def download_audio(url, output_format='mp3', quality='192'):
    """Download audio from YouTube URL and extract audio in the specified format."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': quality,
        }],
        'outtmpl': 'downloaded_audio.' + output_format,  # set filename
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return 'downloaded_audio.' + output_format


def clip_audio(file_path, start_time, end_time, output_file):
    """Clip the audio file based on start and end times, and save it to the output file."""
    audio = AudioSegment.from_file(file_path)
    
    # convert start and end times to milliseconds
    start_time = sum(x * int(t) for x, t in zip([60000, 1000, 1], start_time.split(':')))
    end_time = sum(x * int(t) for x, t in zip([60000, 1000, 1], end_time.split(':')))

    # extract audio segment
    clipped_audio = audio[start_time:end_time]

    # save the clipped audio
    clipped_audio.export(output_file, format=file_path.split('.')[-1])


def main():
    """The main function handling argument parsing and initiating processing."""
    parser = argparse.ArgumentParser(description='Download audio from a YouTube video and clip a specified segment.')
    parser.add_argument('url', help='The URL of the YouTube video')
    parser.add_argument('start_time', help="The start time of the clip in the format 'mm:ss:SSS'")
    parser.add_argument('end_time', help="The end time of the clip in the format 'mm:ss:SSS'")

    args = parser.parse_args()

    try:
        # Download the audio
        downloaded_file = download_audio(args.url)

        # Clip the audio segment
        clip_audio(downloaded_file, args.start_time, args.end_time, 'alarm_clip.mp3')

        print("The clip has been successfully saved as 'alarm_clip.mp3'")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()