"""Exercise routing without launching Computer Use, audio, or network requests."""
import json
import sys
import types
import unittest
from unittest.mock import Mock, patch

import codex_notify


class NotifyTests(unittest.TestCase):
    def run_event(self, payload, voice_on=True, forward_error=None, speech_error=None):
        order = []

        def forward(*args):
            order.append("forward")
            if forward_error:
                raise forward_error

        def speech(*args):
            order.append("speak")
            if speech_error:
                raise speech_error

        speaker = Mock(side_effect=speech)
        with patch.object(sys, "argv", ["codex_notify.py", payload]), \
                patch.object(codex_notify, "SWITCH") as switch, \
                patch.object(codex_notify.Path, "is_file", return_value=True), \
                patch.object(codex_notify.subprocess, "Popen", side_effect=forward) as popen, \
                patch.dict(sys.modules, {"speak": types.SimpleNamespace(speak=speaker)}), \
                patch.object(sys, "stderr"):
            switch.exists.return_value = voice_on
            if speech_error:
                with self.assertRaises(type(speech_error)):
                    codex_notify.main()
            else:
                codex_notify.main()
            popen.assert_called_once_with([codex_notify.SKY, "turn-ended", payload])
        return speaker, order

    def event(self, reply):
        return json.dumps({"type": "agent-turn-complete", "last-assistant-message": reply})

    def test_forwards_before_speaking_only_final_summary(self):
        speaker, order = self.run_event(self.event(
            "Spoken summary: earlier\nFull reply.\nSpoken summary: **All done.**"))
        speaker.assert_called_once_with("All done.")
        self.assertEqual(order, ["forward", "speak"])

    def test_voice_off_still_forwards(self):
        speaker, order = self.run_event(self.event("Spoken summary: Done."), voice_on=False)
        speaker.assert_not_called()
        self.assertEqual(order, ["forward"])

    def test_invalid_or_irrelevant_input_is_silent(self):
        for payload in ["not json", "[]", "null", "{}", '{"type":"other"}',
                        self.event(None), self.event(17), self.event("No summary"),
                        self.event("Spoken summary: ** **")]:
            with self.subTest(payload=payload):
                speaker, _ = self.run_event(payload)
                speaker.assert_not_called()

    def test_speech_failure_does_not_prevent_forwarding(self):
        _, order = self.run_event(self.event("Spoken summary: Done."),
                                  speech_error=RuntimeError("speech unavailable"))
        self.assertEqual(order, ["forward", "speak"])

    def test_notifier_launch_failure_does_not_prevent_speech(self):
        speaker, _ = self.run_event(self.event("Spoken summary: Done."),
                                    forward_error=FileNotFoundError())
        speaker.assert_called_once_with("Done.")

    def test_no_argument_does_nothing(self):
        with patch.object(sys, "argv", ["codex_notify.py"]), \
                patch.object(codex_notify.subprocess, "Popen") as popen:
            codex_notify.main()
            popen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
