# YouTube Alarm Maker

This command-line utility allows you to download audio from a YouTube video, clip a specified segment, and save it for use as an alarm tone on devices that support MP3 or similar audio formats.

## Requirements

- Python 3.x
- `yt-dlp`
- `pydub`
- `ffmpeg`

You can install the required Python packages using pip:

```sh
pip install yt-dlp pydub
```

Ensure you also have `ffmpeg` installed on your system. Refer to the [official FFmpeg download page](https://ffmpeg.org/download.html) for installation instructions.

## Usage

The utility requires three positional arguments:

- `url`: The full URL of the YouTube video you want to download the audio from.
- `start_time`: The start time for the audio clip in the format 'mm:ss:SSS' (minutes:seconds:milliseconds).
- `end_time`: The end time for the audio clip in the same format as the start time.

Here's the command-line syntax:

```sh
python yt_alarm_maker.py <url> <start_time> <end_time>
```

### Example

```sh
python yt_alarm_maker.py https://www.youtube.com/watch?v=V2KU5HracvI 02:40:000 03:30:000
```

This will create an MP3 file named `alarm_clip.mp3` with the audio from 2 minutes, 40 seconds to 3 minutes, 30 seconds from the provided YouTube video.

## Notes

- This script is for educational purposes. Ensure you have the right to access and modify the content you download.
- The quality and format of the downloaded audio are set to 192kbps MP3, but these can be changed within the script.
- The script does minimal error checking, so ensure your inputs are correct.