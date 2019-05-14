#!/usr/bin/env python

import subprocess
import unittest

TNOTES = "/home/grail/projects/tnotes/tnotes.py"

def run_cmd(args):
    proc = subprocess.Popen(args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out, err

class TestTnotes(unittest.TestCase):

    """
    reading:
    0) all the titles
    1) specific note
    2) (maybe) specific line in note

    writing:
    0) new note creation through arguments
    1) addition to existing note
    2) (maybe) replacing note
    3) (maybe) replacing n line in the note

    deleting:
    0) delete note
    1) delete line in a note
    """

    def test_get_all_titles(self):
        args = [TNOTES, "-l"]
        out, err = run_cmd(args)
        # err should be empty
        self.assertEqual(b"", err)
        # tnotes should return something, even without any notes
        self.assertNotEqual(b"", out)

    def test_write_new(self):
        args = [TNOTES,
                "test_note", "-w", "Hello. I am the test note"]
        out, err = run_cmd(args)
        self.assertEqual(b"", err)
        self.assertNotEqual(b"", out)

    def test_read_note(self):
        # create test_note first
        args = [TNOTES, "test_note"]
        out, err = run_cmd(args)
        self.assertEqual(b"", err)
        self.assertIn(b"Hello. I am the test note", out)

    def test_read_specific_note(self):
        # first need to write a few specific notes
        wargs = [TNOTES, "test_specific", "-w", "hallo, I am a specific note;"]
        w_results = [run_cmd(wargs) for i in range(10)]
        [self.assertEqual(b"", err) for _, err in w_results]

        # time to read second one (indexes from 0)
        rargs = [TNOTES, "test_specific", "1"]
        out, err = run_cmd(rargs)
        self.assertNotEqual(b"", out)
        self.assertEqual(b"", err)
        #only one note-line
        self.assertEqual(str(out).count(";"), 1)

        # time to read from third to seventh (2-6)
        rargs = [TNOTES, "test_specific", "2:6"]
        out, err = run_cmd(rargs)
        self.assertNotEqual(b"", out)
        self.assertEqual(b"", err)

    def test_title_not_found(self):
        # user tries to read from title that does not exists
        args = [TNOTES, "not_existing_title"]
        out, err = run_cmd(args)
        self.assertEqual(b"", err)
        self.assertIn("title not found", str(out))

    def test_replace_note(self):
        #user wants to replace a note
        # user creates wrong note
        args = [TNOTES, "note to replace", "-w",
                "bad note, replace later"]
        out, err = run_cmd(args)
        self.assertNotEqual(b"", out)
        self.assertEqual(b"", err)
        self.assertIn("bad note", str(out))

        #user replaces that note using -wr flag
        # returns updated note
        args = [TNOTES, "note to replace", "-wr",
                "good replacement material"]
        out, err = run_cmd(args)
        self.assertEqual(b"", err)

        # read new note
        args = [TNOTES, "note to replace"]
        out, err = run_cmd(args)
        self.assertEqual(b"", err)
        self.assertIn("good", str(out))

    def test_delete_note(self):
        # user creates bad note
        args = [TNOTES, "bad note to delete", "-w",
                "pls delete me"]
        out, err = run_cmd(args)
        self.assertNotEqual(b"", out)
        self.assertEqual(b"", err)
        
        # user wants to delete that note
        args = [TNOTES, "bad note to delete", "-d"]
        out, err = run_cmd(args)
        self.assertEqual(b"", err)

        # user checks titles
        args = [TNOTES, "-l"]
        out, err = run_cmd(args)
        self.assertEqual(b"", err)
        self.assertNotIn("bad note to delete", str(out))



if __name__ == "__main__":
    unittest.main()
