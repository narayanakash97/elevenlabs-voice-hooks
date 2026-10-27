#!/usr/bin/env python3
"""Forward Codex notifications to Computer Use, then speak while voice is on."""
import json
import subprocess
import sys
from pathlib import Path

SKY = str(Path.home() / ".codex/computer-use/Codex Computer Use.app/Contents/"
          "SharedSupport/SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient")
SWITCH = Path(__file__).with_name("VOICE_ON")


def main():
    if len(sys.argv) < 2:
        return
    payload = sys.argv[-1]
    # Forward the original payload before loading any speech code.
    try:
        if Path(SKY).is_file():
            subprocess.Popen([SKY, "turn-ended", payload])
    except OSError:
        print("Codex voice relay: could not start Computer Use notifier.", file=sys.stderr)

    if not SWITCH.exists():
        return
    try:
        event = json.loads(payload)
    except (ValueError, TypeError):
        return
    if not isinstance(event, dict) or event.get("type") != "agent-turn-complete":
        return
    reply = event.get("last-assistant-message")
    marker = "Spoken summary:"
    if not isinstance(reply, str) or marker not in reply:
        return
    summary = reply.rsplit(marker, 1)[1].strip().strip("*_ ").strip()
    if summary:
        from speak import speak
        speak(summary)


if __name__ == "__main__":
    main()
