 #!/usr/bin/env python

import csv
import os

DEFAULT_COLUMNS=("theme", "date", "subtheme", "title", "chapter", "note")

class TNotes:
    def __init__(self, notes_file="default.tsv",
        columns=DEFAULT_COLUMNS):
        self.notes_file = notes_file
        self.columns = columns

        self.create_notes_file()

    def create_notes_file(self):
        """
        if notes_file does not exists
        create it with given column headers/titles
        """
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, "w", newline="") as tsv_file:
                title_writer = csv.writer(tsv_file, delimiter="\t")
                title_writer.writerow(self.columns)

    def get_tsv_data(self):
        with open(self.notes_file) as tsvf:
            # might be really unefficient
            self.data_tsv = list(csv.DictReader(tsvf, delimiter="\t"))

    def get_all_notes(self):
        """returns list of notes"""
        # read/update data
        self.get_tsv_data()
        return [row["note"] for row in self.data_tsv]


    def write_note(self, note_text, **kwargs):
        row_dict = {**kwargs}
        row_dict["note"] = note_text
        key = self.check_keys(row_dict, self.columns)
        if key:
            raise f"""bad argument {key},
            given arguments should be {self.columns}"""
        with open(self.notes_file, "a", newline="") as tf:
            writer = csv.DictWriter(tf, fieldnames=self.columns,
                    delimiter="\t")
            writer.writerow(row_dict)

    def get_input(self):
        lines = list()
        print(f"""you're writing in {self.notes_file},
enter empty line to end input""")
        while True:
            line = input(">")
            if line:
                lines.append(line)
            else:
                break
        self.note_text = """\n""".join(lines)
        return self.note_text

    @staticmethod
    def check_keys(di, keys):
        """
        checks if all dict keys are in keys
        if not returns key that not in keys
        """
        for key in di:
            if key not in keys:
                return key
        return None
