#!/usr/bin/env python3
"""Runs when the user sends a message. "voice on" / "voice off" flips the switch;
while on, it asks Claude to end the reply with a spoken summary."""
import json, sys
from pathlib import Path

SWITCH = Path(__file__).with_name("VOICE_ON")  # if this file exists, the voice is on

prompt = json.load(sys.stdin).get("prompt", "").strip().lower().rstrip(".!")
if prompt == "voice on":
    SWITCH.touch()
elif prompt == "voice off":
    SWITCH.unlink(missing_ok=True)

if SWITCH.exists():
    print("Voice is on. End your reply with a final section starting 'Spoken summary:' "
          "that explains each main point in plain spoken sentences, with the reasoning "
          "behind it, without reading the reply out. Match the length to the reply: "
          "one or two sentences for a short reply, about 100 words for a normal one, "
          "longer only when the reply carries real depth such as calculations. "
          "No links, tables, code, file names or markdown.")
