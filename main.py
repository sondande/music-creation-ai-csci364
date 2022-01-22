"""
    Driver Class for Application
"""

import os
import psycopg2
import scaleCreation
import d_connection
import encode_decoder
from random import randint, random
from collections import OrderedDict

def main():
    # Takes in inputs from user and evaluates
    root = input("What root note for your scale do you want?: ").capitalize()
    qualityNumber = int(input("Major or Minor? (Select 1 for major, 2 for minor): "))
    scale_input = "Minor" if qualityNumber == 2 else "Major"

    # Creates a list of all possible roots by combining the columns note and e_harm_note from our chromatic scale
    # database. We also use the fromKeys method to take away all duplicates
    NOTE_MAPPING = list(OrderedDict.fromkeys(
        d_connection.execute_query_command("SELECT note FROM chromatic_scale;") + d_connection.execute_query_command(
            "SELECT e_harm_note FROM chromatic_scale;")))
    # Sort the list for easier search later
    NOTE_MAPPING.sort()

    if len(root) > 2:
        print("Not a valid root note, maybe too many characters.")
        exit()
    elif root not in NOTE_MAPPING:
        print(
            "Not a valid root note, choose one of the following: ", NOTE_MAPPING)
        exit()

    # TODO will take in argument from command line in first finished project and then web api for later use
    scale_result = scaleCreation.chromatic_scale_creation(root,scale_input)
    print(encode_decoder.decodeNotes(scale_result))


if __name__ == "__main__":
    main()
else:
    print("Executed when imported")
