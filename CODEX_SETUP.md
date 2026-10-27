# Optional Codex notification relay

This path is experimental. Offline tests pass; desktop playback must be checked in your actual client.

1. Complete the Keychain and direct speech setup in the README.
2. In Terminal, run `command -v python3` and `pwd` from the cloned repository. Keep those paths.
3. Open `~/.codex/config.toml` in your editor and save a backup. Add the following at the top level, before any `[section]`, replacing both example paths:

```toml
notify = ["/ABSOLUTE/PATH/python3", "/ABSOLUTE/PATH/elevenlabs-voice-hooks/codex_notify.py"]
```

Use your user-level configuration. Project-level configuration cannot override `notify`. If you already have a `notify` command, preserve its behavior before replacing it. The supplied relay only forwards the specific macOS Computer Use notifier at `~/.codex/computer-use/Codex Computer Use.app/Contents/SharedSupport/SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient` when that executable exists. It does not preserve arbitrary custom notifiers.

4. In `~/.codex/AGENTS.md`, append this instruction without removing existing instructions:

> End each final reply with a line beginning Spoken summary: followed by a brief plain-language account of the main points. Keep it to roughly 100 words or less. Exclude links, tables, code, filenames, and Markdown.

5. In Terminal, from the cloned folder, enable speech:

```sh
touch VOICE_ON
```

6. Quit and reopen Codex. Ask for a short greeting. Verify both the written summary and audible speech. A direct script test does not establish that the desktop client emits notifications.
7. Disable speech from Terminal with:

```sh
rm -f VOICE_ON
```

Send another prompt and confirm silence. Codex has no `voice on` prompt handler in this repository. If Claude Code uses this same checkout, its voice commands control the shared switch too.

To roll back, restore your previous `notify` setting, remove only the summary instruction you added, and restart Codex. Preserve later edits to either file.
