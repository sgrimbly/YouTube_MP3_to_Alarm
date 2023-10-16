import argparse
import yt_dlp as youtube_dl
from pydub import AudioSegment
import re
import os 

def sanitize_filename(filename):
    """
    Sanitize the filename by removing or replacing characters that are not allowed in filenames.
    """
    # Define a set of allowed characters (alphanumeric, spaces, and hyphens)
    allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_")

    # Replace unallowed characters with an underscore
    sanitized_filename = ''.join(c if c in allowed_characters else '_' for c in filename)

    # Further sanitize filename using regex to handle edge cases
    sanitized_filename = re.sub(r'(?u)[^-\w.]', '', sanitized_filename)

    # Avoid extremely long filenames
    max_length = 255
    if len(sanitized_filename) > max_length:
        # Truncate the name, not counting the extension
        file_root, file_extension = os.path.splitext(sanitized_filename)
        file_root = file_root[:max_length - len(file_extension)]
        sanitized_filename = file_root + file_extension

    return sanitized_filename

def download_audio(url, output_format='mp3', quality='192'):
    """Download audio from YouTube URL and extract audio in the specified format."""
    
    # Temporary ydl_opts without 'outtmpl' to fetch the video's title
    temp_ydl_opts = {}
    
    with youtube_dl.YoutubeDL(temp_ydl_opts) as ydl:
        # We only want to extract the information without downloading the video
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)

    # Sanitize the filename to make it filesystem safe
    sanitized_title = sanitize_filename(video_title)
    
    # Define ydl options with 'outtmpl' using the sanitized title
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': quality,
        }],
        # Use the sanitized title as the template for the output filename
        'outtmpl': f"{sanitized_title}.%(ext)s",  
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # This time, we proceed with the actual download since we've set the correct 'outtmpl'
        ydl.download([url])

    # Construct the filename using the sanitized title and the expected extension
    filename = f"{sanitized_title}.{output_format}"

    # Verify the file exists, especially if there were special characters or length issues
    if not os.path.isfile(filename):
        raise Exception(f"Expected file '{filename}' doesn't exist. The filename might have been altered during download.")

    return filename  # return the sanitized filename

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

def convert_to_ringtone(file_path, output_file):
    """Convert the mp3 file to an iPhone-compatible ringtone format (.m4r)."""
    # Load the mp3 file
    audio = AudioSegment.from_file(file_path, format="mp3")

    # Export the audio in .m4r format
    audio.export(output_file, format="mp4")  # .m4r is a subset of the MPEG-4 format


def main():
    parser = argparse.ArgumentParser(description='Download audio from a YouTube video, clip a specified segment, and optionally convert it to iPhone ringtone format.')
    parser.add_argument('url', help='The URL of the YouTube video')
    parser.add_argument('start_time', help="The start time of the clip in the format 'mm:ss:SSS'")
    parser.add_argument('end_time', help="The end time of the clip in the format 'mm:ss:SSS'")
    parser.add_argument('--iphone', action='store_true', help='Convert the clip to iPhone ringtone format')

    args = parser.parse_args()

    try:
        # Download the audio
        downloaded_file = download_audio(args.url)

        # Define the output file name
        output_file = 'alarm_clip.m4r' if args.iphone else 'alarm_clip.mp3'

        # Clip the audio segment
        clip_audio(downloaded_file, args.start_time, args.end_time, output_file)

        # If the iPhone flag is used, convert the file to .m4r format
        if args.iphone:
            convert_to_ringtone(output_file, 'alarm_clip.m4r')
            print("The clip has been successfully saved as 'alarm_clip.m4r'")
            print("Please transfer this file to your iPhone and set it as a ringtone. Refer to the README for instructions.")
        else:
            print("The clip has been successfully saved as 'alarm_clip.mp3'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()