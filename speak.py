#!/usr/bin/env python3
"""Speak text out loud through ElevenLabs. Usage: speak.py "some text" """
import getpass, json, subprocess, sys, tempfile

VOICE_ID = "SAz9YHcvj6GT2YYXdXww"  # River; choose an available voice from your ElevenLabs account.
MODEL_ID = "eleven_flash_v2_5"     # Eleven Flash v2.5

def api_key():
    # Reads the key from Keychain. It is never written to a file.
    return subprocess.run(
        ["security", "find-generic-password", "-a", getpass.getuser(),
         "-s", "elevenlabs-api-key", "-w"],
        capture_output=True, text=True, check=True).stdout.strip()

def speak(text):
    try:
        # curl, not Python's urllib: python.org Python lacks the Mac's trusted certificates.
        with tempfile.NamedTemporaryFile(suffix=".mp3") as audio:
            subprocess.run(
                ["curl", "-sSf", "--max-time", "30",
                 f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_64",
                 "--config", "-", "-o", audio.name],
                input="\n".join([
                    "header = " + json.dumps("xi-api-key: " + api_key()),
                    'header = "Content-Type: application/json"',
                    "data = " + json.dumps(json.dumps({"text": text, "model_id": MODEL_ID})),
                ]),
                text=True, check=True)
            subprocess.run(["afplay", audio.name])   # afplay is the Mac's built-in player
    except subprocess.CalledProcessError:
        # ElevenLabs said no (credits gone, offline, key issue): use the Mac's own voice.
        subprocess.run(["say", text])

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or sys.stdin.read()
    if text.strip():
        speak(text.strip())
