#!/usr/bin/env python

import unittest
from tnotes import TNotes
import os

class TestTsvNotes(unittest.TestCase):

    """
    need to test writing to tsv notes
    reading from it
    shall be main tsv file created: like default.tsv
    creation of custom tsv files
    """

    test_file = "test.tsv"
    columns=("theme", "date", "subtheme", "title", "chapter", "note")

    def setUp(self):
        self.tnotes = TNotes(notes_file=self.test_file,
                columns=self.columns)

    def tearDown(self):
        os.remove(self.test_file)

    def test_minimal_write(self):
        """
        write minimal note to empty tsv
        test that it got 1 note entry
        """
        self.tnotes.write_note("this is a test note")
        notes = self.tnotes.get_all_notes()
        self.assertEqual(len(notes), 1)

        # read back as dict
        row_dict = self.tnotes.read_rows(index=0)

        # type dict
        self.assertEqual(type(row_dict), "dict")

        # keys from row dict are the same that we gave it
        for key in row_dict:
            self.assertIn(self.columns)




if __name__ == "__main__":
    unittest.main()
