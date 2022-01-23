""" PERSONAL CHECK. MAIN IS GETTING IMPORTED AGAIN SO MAIN IS GETTING RUN TWICE. NEED TO FIX """

"""
    Driver Class for Application
"""
import sys
import os
import psycopg2
from melodyNotes import Population
from scaleCreation import chromatic_scale_creation, chromatic_scale_degree
from d_connection import execute_query_command, scale_degree_search
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

root_scale= chromatic_scale_degree(root)

# TODO Implement Check if scale type is in our database
scale_type = str(sys.argv[2]).capitalize()

chord_progression_id = str(sys.argv[3])
# Grab user chord progression

# Get's chord progressions bass line melody in array and storing the notes as their chromatic values
chord_progression = execute_query_command("SELECT chord_progression_melody FROM chord_progressions WHERE chord_progression_id=" + chord_progression_id + ";")
chord_progression = chord_progression[0]
# Get's chord progressions with qualities
chord_progressions_quality = execute_query_command("SELECT chord_progression FROM chord_progressions WHERE chord_progression_id=" + chord_progression_id + ";")
# Creates list of the quality of scales in desired chord progression
scale_quality = []

for chord_p in chord_progressions_quality:
    progression = []
    for s in chord_p.split("-"):
        if s.isdigit():
            quality = "Major"
        else:
            quality = "Minor"
        progression.append(quality)
    scale_quality.append(progression)

chord_progression_scales_list = []
counter = 0
# creates all the notes in the scale for the specific chord in chord progression
for degree in chord_progression:
    chord_progression_scales_list.append(chromatic_scale_creation(degree+1, scale_quality[0][counter]))

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
KEY_SCALE = chromatic_scale_creation(root_scale, scale_type)
#bass_chord_progressions = execute_query_command("SELECT chord_progression_melody FROM chord_progressions;")
population = Population(root, KEY_SCALE, scale_type, CHROMATIC_NOTE_MAPPING, chord_progression, chord_progression_scales_list)
population.initial_population(16,5)
generation = 0
# doing it for chosen iterations
for i in range(1,3):
    # calculates current population's fitness
    population.fitness_function(generation)
    # Creates new population
    new_pop = population.selection()
    # Stores and sets new pop as our current
    population.new_gen_pop_dev(generation, new_pop)
    generation += i

# Finished creating our options: return desired amount of options
sql_comm = "select melody from melodies order by fitness_score; "
result = execute_query_command(sql_comm)
# Prints results from query

for r in result:
    print("Melody Choices:", r)
