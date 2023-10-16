import os
import unittest
from pydub import AudioSegment
from audio_extractor import clip_audio

class TestYTAlarmMaker(unittest.TestCase):

    def setUp(self):
        """Create a sample audio file for testing."""
        # Generate a 10-second silent audio segment
        self.test_audio = AudioSegment.silent(duration=10000)  # duration in milliseconds
        # Export the silent audio segment to a file
        self.test_audio.export("test_audio.mp3", format="mp3")

    def test_clip_audio(self):
        """Test the audio clipping function."""
        # Define the start and end times for clipping (3 seconds to 8 seconds)
        start_time = "00:03:000"
        end_time = "00:08:000"

        # Clip the audio segment
        clip_audio("test_audio.mp3", start_time, end_time, "test_output.mp3")

        # Check if the output file was created
        self.assertTrue(os.path.exists("test_output.mp3"))

        # Load the clipped audio and check its duration
        clipped_audio = AudioSegment.from_file("test_output.mp3")
        # The expected duration should be 5000 milliseconds (5 seconds)
        self.assertEqual(len(clipped_audio), 5000)

    def tearDown(self):
        """Clean up the created audio files after testing."""
        os.remove("test_audio.mp3")
        os.remove("test_output.mp3")

if __name__ == "__main__":
    unittest.main()
