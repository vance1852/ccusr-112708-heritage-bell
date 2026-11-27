"""核对本地记录在装载时完整保留了协议字段与输入顺序。"""
import json
import subprocess
import sys
import unittest

from device_replay import ROOT, load_profile, read_frames


class DeviceArchiveTest(unittest.TestCase):
    def test_envelopes_and_payload_widths(self):
        profile = load_profile()
        frames = list(read_frames())
        self.assertEqual(len(frames), 18)
        self.assertEqual(set(profile["wire_fields"]), {f["type"] for f in frames})
        self.assertEqual([f["arrival"] for f in frames], list(range(1, len(frames) + 1)))
        self.assertEqual([f["received"] for f in frames], sorted(f["received"] for f in frames))
        for frame in frames:
            with self.subTest(arrival=frame["arrival"]):
                self.assertIsInstance(frame["captured"], int)
                self.assertTrue(frame["source"])
                self.assertEqual(len(profile["wire_fields"][frame["type"]].split()), len(frame["args"]))

    def test_cli_matches_raw_archive(self):
        run = subprocess.run(
            [sys.executable, "device_replay.py"],
            cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual([json.loads(line) for line in run.stdout.splitlines()], list(read_frames()))

    def test_related_device_evidence_is_present_in_reception_order(self):
        frames = list(read_frames())
        indices = [4, 5, 6, 8]
        self.assertEqual([
            (frames[i]["source"], frames[i]["type"], frames[i]["args"][0]) for i in indices
        ], [('n1', 'queued', 'show1'), ('n2', 'queued', 'show1'), ('n2', 'clock', 'c22'), ('n2', 'link', 'offline')])
        indices = [9, 10, 11, 14, 15]
        self.assertEqual([
            (frames[i]["source"], frames[i]["type"], frames[i]["args"][0]) for i in indices
        ], [('n1', 'playing', 'show1'), ('ops', 'quiet', 'homes'), ('n1', 'stop_seen', 'show1'), ('n1', 'stopped', 'show1'), ('n2', 'playing', 'show1')])
        indices = [12, 13, 16, 17]
        self.assertEqual([
            (frames[i]["source"], frames[i]["type"], frames[i]["args"][0]) for i in indices
        ], [('desk', 'book', 'show3'), ('n3', 'playing', 'show3'), ('n3', 'stopped', 'show3'), ('desk', 'ask', 'show1')])
