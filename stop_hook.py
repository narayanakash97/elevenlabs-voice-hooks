#!/usr/bin/env python3
"""Runs when Claude finishes a reply. While the voice is on, speaks the
'Spoken summary:' line and nothing else."""
import json, sys
from pathlib import Path
from speak import speak

if Path(__file__).with_name("VOICE_ON").exists():
    reply = json.load(sys.stdin).get("last_assistant_message") or ""
    marker = "Spoken summary:"
    if marker in reply:
        speak(reply.rsplit(marker, 1)[1].strip().strip("*_ "))
