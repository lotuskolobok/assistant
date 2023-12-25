from collections import UserDict
from datetime import date, datetime
import json
from pathlib import Path
import re
import copy
import os


class NoteName:

    def __init__(self, value):
        if len(value) < 30:
            self.value = value
        else:
            self.value = value[:30]

    def __repr__(self):
        return f'{self.value}'


class Status:

    def __init__(self, value="in progress"):
        self.value = "in progress"

    def __repr__(self):
        return f'{self.value}'


class Notes:

    def __init__(self, value):
        if len(value) < 250:
            self.value = value
        else:
            self.value = value[:250]


class Tags:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class RecordNote:
    def __init__(self, name, note: Notes, tag: Tags = None, status="in progress"):
        self.name = name
        self.note = note
        self.tags = []
        if tag:
            self.tags.append(tag)
        self.status = Status(status)

    def __str__(self):
        return f"Name: {self.name.value} Note: {self.note.value} Tags: {self.tags} Status: {self.status.value}"

    def __repr__(self):
        return f"Name: {self.name.value} Note: {self.note.value} Tags: {self.tags} Status: {self.status.value}"


class NoteBook(UserDict):
    def __init__(self):
        self.data = {}

    def __repr__(self):
        return f'{self.data}'

    def add_note(self, record):
        self.data[record.name.value] = record

    def change_name(self, old_name, new_name):
        self.data[new_name] = copy.deepcopy(self.data[old_name])
        self.data[new_name].name.value = new_name
        self.data.pop(old_name)

    def change_tag(self, name, tags):
        new_tag = Tags(tags)
        for k, v in self.data.items():
            if k == name:
                self.data[k].tags = []
                self.data[k].tags.append(new_tag)

    def change_note(self, name, new_note):
        new_note = Notes(new_note)
        for k in self.data:
            if k == name:
                self.data[k].note = new_note

    def change_status(self, name, new_status):
        if new_status.lower() in ["in progress", "done"]:
            self.data[name].status.value = new_status.lower()

    def show_record(self, name):
        if name in self.data.keys():
            return self.data[name]

    def show_note(self, name):
        for k in self.data:
            if k == name:
                return self.data[k]

    def delete_note(self, rec: RecordNote):
        for a, v in self.data.items():
            if v.note == rec.note:
                deleted_note = a.note
                self.data.pop(a)
                return deleted_note

    def delete_notes_by_status(self, status):
        result = {}
        for name, record in self.data.items():
            if record.status.value != status:
                result[name] = record
        self.data = result

    def delete_tag(self, name, del_tag):
        old_tags = self.data[name].tags
        new_tags = [tag for tag in old_tags if tag.value != del_tag]
        self.data[name].tags = new_tags

    def add_tag(self, name, new_tag):
        if new_tag.value not in [i.value for i in self.data[name].tags]:
            self.data[name].tags.append(new_tag)

    def find_info_by_name(self, keyword):
        result = []
        for name, record in self.data.items():
            if keyword.lower() == name.lower():
                result.append(self.data[name])
                break
        return result

    def find_info_by_tag(self, keyword):
        result = []
        for name, record in self.data.items():
            for tag in record.tags:
                if keyword.lower() == tag.value.lower():
                    result.append(self.data[name])
                    break
        return result

    def find_info_by_status(self, keyword):
        result = []
        for name, record in self.data.items():
            if keyword.lower() == record.status.value.lower():
                result.append(self.data[name])
        return result

    def get_tags(self, name):
        return self.data[name].tags

    def change_tag(self, name, old_tag, new_tag):
        for i in range(len(self.data[name].tags)):
            if old_tag.value == self.data[name].tags[i].value:
                self.data[name].tags[i].value = new_tag.value

    def serialize(self, file_name="notebook.bin"):
        with open(file_name, 'wb') as file:
            json.dump(self.data, file)

    def deserialize(self, file_name="notebook.bin"):
        with open(file_name, 'rb') as file:
            self.data = json.load(file)

    def show_records(self):
        return self.data

    # def get_notes(self):
    #     return self.notes
