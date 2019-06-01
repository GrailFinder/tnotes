#!/usr/bin/env python

import subprocess
import unittest
import os


homepath = os.environ["HOME"]
TNOTES = os.path.join(homepath, "projects/tnotes/tnotes")
CONFIG = os.path.join(homepath, ".config/tnotes")

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

    3) search in note
    4) search in all notes

    writing:
    0) new note creation through arguments
    1) addition to existing note
    2) (maybe) replacing note
    3) (maybe) replacing n line in the note

    deleting:
    0) delete note
    1) delete line in a note
    """

    def setUp(self):
        self.file = "functest.tsv"
        self.path = os.path.join(CONFIG, self.file)
        # tnotes creates test tsv file itself
        self.args = [TNOTES, "-f", self.file]

    def tearDown(self):
        os.remove(self.path)

    def test_get_all_titles(self):
        self.args.extend(
                ["test_note", "-w", "Hello. I am the test note"])
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)

        self.args[-3:] = ["-l"]
        out, err = run_cmd(self.args)
        # err should be empty
        self.assertEqual(b"", err)
        # tnotes should return something, even without any notes
        self.assertNotEqual(b"", out)

    def test_write_new(self):
        self.args.extend(
                ["test_note", "-w", "Hello. I am the test note"])
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)
        self.assertEqual(b"", out)

        # read written note
        out, err = run_cmd(self.args[:-2])
        self.assertEqual(b"", err)
        self.assertNotEqual(b"", out)


    def test_read_note(self):
        self.args.extend(
                ["test_note", "-w", "Hello. I am the test note"])
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)

        # create test_note first
        self.args[-2:] = []
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)
        self.assertIn(b"Hello. I am the test note", out)

    def test_read_specific_note(self):
        # first need to write a few specific notes
        self.args.extend(
                ["test_specific", "-w", "hallo, I am a specific note;"])
        w_results = [run_cmd(self.args) for i in range(10)]
        [self.assertEqual(b"", err) for _, err in w_results]

        # time to read second one (indexes from 0)
        self.args[-3:] = ["test_specific", "1"]
        out, err = run_cmd(self.args)
        self.assertNotEqual(b"", out)
        self.assertEqual(b"", err)
        #only one note-line
        self.assertEqual(str(out).count(";"), 1)

        # time to read from third to seventh (2-6)
        self.args[-1] = "2:6"
        out, err = run_cmd(self.args)
        self.assertNotEqual(b"", out)
        self.assertEqual(b"", err)

    def test_title_not_found(self):
        # user tries to read from title that does not exists
        self.args.append("not_existing_title")
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)
        self.assertIn("title not found", str(out))

    def test_replace_note(self):
        #user wants to replace a note
        # user creates wrong note
        self.args.extend(["note to replace", "-w",
                "bad note, replace later"])
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)

        #user replaces that note using -wr flag
        # returns updated note
        self.args[-2:] = ["-wr", "good replacement material"]
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)

        # read new note
        self.args[-2:] = []
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)
        self.assertIn("good", str(out))

    def test_replace_n_line(self):
        # user creates a note with 3 lines
        title = "multiline note to replace"
        self.args.extend([title, "-w", "old text"])
        results = [run_cmd(self.args) for _ in range (3)]
        for res in results:
            out, err = res
            self.assertEqual(b"", err)

        # user changes second line
        self.args[-2:] = ["1", "-wr", "new text"]
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)

        # user reads new note
        self.args = self.args[:-3]
        out, err  = run_cmd(self.args)
        self.assertIn("new", str(out))

        # user deletes that note alltogether
        self.args.append("-d")
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)

    def test_delete_note(self):
        # user creates bad note
        self.args.extend(["bad note to delete", "-w",
                "pls delete me"])
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)

        # user wants to delete that note
        self.args[-2:] = ["-d"]
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)

        # user checks titles
        self.args[-2:] = ["-l"]
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)
        self.assertNotIn("bad note to delete", str(out))

    def test_delete_n_line(self):
        # user creates multiline bad note
        self.args.extend(["multibad", "-w", "I am the worst"])
        results = [run_cmd(self.args) for _ in range(3)]
        for res in results:
            self.assertEqual(b"", res[1])

        # user checks that 3 lines created
        self.args[-2:] = []
        out, err = run_cmd(self.args)
        self.assertEqual(3, str(out).count("worst"))

        # user deleted n line
        self.args.extend(["1", "-d"])
        _, err = run_cmd(self.args)
        self.assertEqual(b"", err)

        # user checks that only two lines left
        out, _ = run_cmd(self.args[:-2])
        self.assertEqual(2, str(out).count("worst"))

        # user deletes all multibad notes
        self.args.pop(-2)
        _, err = run_cmd(self.args)
        self.assertEqual(b"", err)

    def test_search_in_all_notes(self):
        # user creates two notes containing some common text
        self.args.extend(["find some note", "-w", "this is searchable line"])
        run_cmd(self.args)
        self.args[-1] = "other line, cant be found"
        run_cmd(self.args)
        self.args[-1] = "it should be searchable, I hope"
        run_cmd(self.args)

        # user runs search on common text
        self.args[-3:] = ["-s", "searchable"]
        out, err = run_cmd(self.args)
        self.assertEqual(b"", err)
        self.assertEqual(2, str(out).count("searchable"))

        # user deletes these notes
        self.args[-2:] = ["find some note", "-d"]
        run_cmd(self.args)

        self.args[-2] = "find other note"
        run_cmd(self.args)


    def test_search_in_note(self):
        # user creates note with n lines
        self.args.extend(["find some note", "-w", "this is searchable line"])
        run_cmd(self.args)
        self.args[-1] = "other line, cant be found"
        run_cmd(self.args)

        # user runs search in that note
        self.args[-2:] = ["-s", "searchable"]
        out, err = run_cmd(self.args)

        self.assertEqual(b"", err)
        self.assertEqual(1, str(out).count("searchable"))

        # user deletes these notes
        self.args[-2:] = ["-d"]
        run_cmd(self.args)


if __name__ == "__main__":
    unittest.main()
