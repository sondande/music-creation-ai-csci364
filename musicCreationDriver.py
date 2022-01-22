""" PERSONAL CHECK. MAIN IS GETTING IMPORTED AGAIN SO MAIN IS GETTING RUN TWICE. NEED TO FIX """

"""
    Driver Class for Application
"""
import sys
import os
import psycopg2
from melodyNotes import Population
from scaleCreation import chromatic_scale_creation
from d_connection import execute_query_command
from encode_decoder import decodeNotes
from random import randint, random
from collections import OrderedDict

"""
    Main function for the program. We will create and take in inputs from here and guide them to the according spots to 
    be analyzed. Purpose of all the files is to seperate functions away from each other to be able to help with 
    debugging,analysis, and overall production of different elements that create a melody 
"""

""" Functions that need to run before main and set variables that are universal for project """

## Global Variables for Entire Application
# Takes in inputs from user and evaluates
root = str(sys.argv[1]).capitalize()

# TODO Implement Check if scale type is in our database
scale_type = str(sys.argv[2]).capitalize()

### Initial creation of Population for melody through the creation of scales from the inputs given ###

# Creates a list of all possible roots by combining the columns note and e_harm_note from our chromatic scale
# database. We also use the fromKeys method to take away all duplicates
CHROMATIC_NOTE_MAPPING = list(OrderedDict.fromkeys(
    execute_query_command("SELECT note FROM chromatic_scale;") + execute_query_command(
        "SELECT e_harm_note FROM chromatic_scale;")))

# Sort the list for easier search later
CHROMATIC_NOTE_MAPPING.sort()

if len(root) > 2:
    print("Not a valid root note, maybe too many characters.")
    exit()
elif root not in CHROMATIC_NOTE_MAPPING:
    print(
        "Not a valid root note, choose one of the following: ", CHROMATIC_NOTE_MAPPING)
    exit()

# Chromatic Scale Creation and reference variable
KEY_SCALE = chromatic_scale_creation(root, scale_type)
population = Population(root, KEY_SCALE, scale_type, CHROMATIC_NOTE_MAPPING)
population.initial_population(0, 16,4)

# def main():
#
#     decoded_scale = decodeNotes(KEY_SCALE)
#     print(decoded_scale)
#
#     ## Create initial population ###
#
#     # Be used as unique index??? For storing the population of each generation and then we can see the difference between different generations
#     generation = 0
#     melodyNotes.initial_population(generation, 16,4)
#
#
# # if __name__ == "__main__":
# #     main()