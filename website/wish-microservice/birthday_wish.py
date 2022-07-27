from file_watcher import FileWatcher

import json
import random

f = open("../static/birthday-quotes-with-relationship-formatted.json")


def file_modified():
    with open("relationship.txt", "r") as infile:
        text_file = infile.readline()
    wish_generator(text_file)
    return False


data = json.load(f)
json_data = {}
invalid_string = [
    "This relationship is not valid. Please search for a different relationship."]


# create set of possible relations from the json file
relations = set()
for item in data:
    for key in item:
        if key == "relation":
            relations.add(item[key])


def wish_generator(relationship):
    """
    Reads relationship.txt and checks if it's a relationship that matches a relation.
    If so, it will return up to 5 greetings
    Valid relationships are: 'brother-in-law', 'boss', 'aunt', 'teacher', 'brother', 'grand-son',
    'friend', 'son', 'sister', 'girlfriend', 'uncle', 'nephew', 'grandfather', 'student', 'father-in-law',
    'wife', 'fiance', 'grand-daughter', 'mother', 'boyfriend', 'niece', 'cousin', 'colleague', 'grandmother',
    'daughter', 'father', 'sister-in-law', 'mother-in-law', 'husband'
    """
    if relationship not in relations:
        json_data["greetings"] = invalid_string
        with open("../static/wishes.json", "w") as outfile:
            json.dump(json_data, outfile)
    else:
        matching_greetings = []
        for item in data:
            for key in item:
                if item[key] == relationship:
                    matching_greetings.append(item["quote"])

        # return up to 5 greetings
        if len(matching_greetings) < 5:
            json_data["greetings"] = random.sample(
                matching_greetings, len(matching_greetings)
            )
        else:
            json_data["greetings"] = random.sample(matching_greetings, 5)

        # write the wishes to wishes.json
        with open("../static/wishes.json", "w") as outfile:
            json.dump(json_data, outfile)


fileWatcher = FileWatcher(r"relationship.txt", file_modified)
fileWatcher.start()
