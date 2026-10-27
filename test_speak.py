"""Verify speech routing without secrets, network requests, or audio playback."""
import json
import subprocess
import unittest
from unittest.mock import patch

import speak


class SpeechTests(unittest.TestCase):
    def test_key_and_text_are_stdin_only_and_audio_is_temporary(self):
        from pathlib import Path
        with patch.object(speak, "api_key", return_value="fixture-key"), \
                patch.object(speak.subprocess, "run") as run:
            speak.speak('A "quoted" summary.\nSecond line.')
        request, playback = run.call_args_list
        args = request.args[0]
        self.assertNotIn("fixture-key", " ".join(args))
        self.assertNotIn("quoted", " ".join(args))
        config = request.kwargs["input"].splitlines()
        self.assertEqual(json.loads(config[0].split(" = ", 1)[1]), "xi-api-key: fixture-key")
        payload = json.loads(json.loads(config[2].split(" = ", 1)[1]))
        self.assertEqual(payload["text"], 'A "quoted" summary.\nSecond line.')
        self.assertEqual(playback.args[0][0], "afplay")
        self.assertFalse(Path(playback.args[0][1]).exists())

    def test_api_failure_uses_system_voice(self):
        with patch.object(speak, "api_key", return_value="fixture-key"), \
                patch.object(speak.subprocess, "run", side_effect=[
                    subprocess.CalledProcessError(22, "curl"), None]) as run:
            speak.speak("Hello")
        self.assertEqual(run.call_args.args[0], ["say", "Hello"])

    def test_missing_key_uses_system_voice(self):
        with patch.object(speak, "api_key", side_effect=subprocess.CalledProcessError(44, "security")), \
                patch.object(speak.subprocess, "run") as run:
            speak.speak("Hello")
        run.assert_called_once_with(["say", "Hello"])


if __name__ == "__main__":
    unittest.main()
