#!/usr/bin/env python

import csv
import os
import argparse
import datetime as dt

DEFAULT_COLUMNS=("date", "title", "note")

def init_flags():
    parser = argparse.ArgumentParser(description="notes in tsv format")
    parser.add_argument(
        "-f",
        dest="notes_file",
        default="default.tsv",
        help="tsv file to store your notes; consider difference in column titles",
    )
    parser.add_argument(
        "title",
        nargs="*",
        help="title to write your notes; book->date->subject->title->chapter->note"
    )
    parser.add_argument(
        "-w",
        dest="write_mode",
        help="when given writes to file, if given existing title - adds a note"
    )
    parser.add_argument(
        "-wr",
        dest="replace_mode",
        help="replaces note text"
    )
    parser.add_argument(
        "-i",
        dest="interactive_mode",
        action="store_true",
        help="when given uses promt to get input from user to add a note"
    )
    parser.add_argument(
        "-d",
        dest="delete_mode",
        action="store_true",
        help="deletes note with given title"
    )
    parser.add_argument(
        "-l",
        dest="list_titles",
        action="store_true",
        help="lists all titles"
    )

    if len(os.sys.argv)==1:
        parser.print_help(os.sys.stderr)
        os.sys.exit(1)

    args = parser.parse_args()
    return args

class TNotes:
    def __init__(self, notes_file="default.tsv",
        columns=DEFAULT_COLUMNS, **kwargs):
        self.notes_file = notes_file
        self.columns = columns
        self.index_to_return = None

        # hardcode
        self.create_notes_file()

        arg_di = {**kwargs}
        nav_di = arg_di.copy()
        for key in arg_di:
            if key not in self.columns:
                nav_di.pop(key)

        # read mode
        if "list_titles" in arg_di and arg_di["list_titles"]:
            self.get_all_titles()
            return

        # extract string from list
        if "title" in nav_di and type(nav_di["title"]) is list:
            if len(nav_di["title"]) > 1:
                self.index_to_return = nav_di["title"][1]
            nav_di["title"] = nav_di["title"][0]


        # write mode
        if "write_mode" in arg_di and arg_di["write_mode"]:
            note_text = arg_di["write_mode"]

            if "date" in self.columns:
                nav_di["date"] = dt.datetime.now().isoformat()
            self.write_note(note_text=note_text, **nav_di)
            print(note_text)
            return

        elif "replace_mode" in arg_di and arg_di["replace_mode"]:
            note_text = arg_di["replace_mode"]
            nav_di["note"] = note_text
            self.replace_note(**nav_di)
            return

        elif "delete_mode" in arg_di and arg_di["delete_mode"]:
            self.replace_note(**nav_di)
            return

        else:
            # read
            self.read_notes(**nav_di)

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

    def get_all_titles(self):
        """returns list of titles"""
        # read/update data
        self.get_tsv_data()
        print({row["title"] for row in self.data_tsv})
        return {row["title"] for row in self.data_tsv}


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

    def replace_note(self, **kwargs):
        """deletes all the lines of the note with given title"""
        row_dict = {**kwargs}
        # read all notes
        self.get_tsv_data()
        if "title" not in row_dict:
            print("error: no title given")
        filtered = [row for row in self.data_tsv
                    if row["title"] != row_dict["title"]]
        # add new note to cleared notes
        if "note" in row_dict:
            if "date" in self.columns:
                row_dict["date"] = dt.datetime.now().isoformat()
            filtered.append(row_dict)
        # write it
        headers = filtered[0].keys()
        with open(self.notes_file, "w", newline="") as tf:
            writer = csv.DictWriter(tf, headers, delimiter="\t")
            writer.writeheader()
            writer.writerows(filtered)


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

    def read_notes(self, **kwargs):
        nav_di = {**kwargs}
        self.get_tsv_data()
        by_title = [row["note"] for row in self.data_tsv 
                if row["title"] == nav_di["title"]]

        # if no such notes with that title
        if not by_title:
            print("title not found:", nav_di["title"])
            return by_title

        # index parsing
        start_index = None
        if self.index_to_return:
            if ":" in self.index_to_return:
                start_index, end_index = self.index_to_return.split(":")
                start_index = int(start_index)
                end_index = int(end_index)
            else:
                start_index = end_index = int(self.index_to_return)

        print(nav_di["title"])
        if start_index:
            [print(index, '\t', row)
                for index, row in enumerate(by_title)
                if index >= start_index and index <= end_index]
        else:
            [print(index, '\t', row)
                for index, row in enumerate(by_title)]

        return by_title


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


if __name__ == "__main__":
    args = init_flags()
    flags = vars(args) # vars?

    tnotes = TNotes(**flags)
