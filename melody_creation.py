# Mark Ligonde and Sagana Ondande
# Professor Adam Eck
# CS364
# Final Artificial Intelligence Project
#
# I affirm that we have adhered to the Honor Code on this assignment - Mark Ligonde & Sagana Ondande

import os
import psycopg2
from random import randint, random

# ARE WE CHANGING THE DATABASE INFORMATION TO INDEX OFF ZERO? OR ARE WE CHANGING THE NOTE_MAPPING ABOVE TO INDEX OFF 1?
# I PERSONALLY LIKE INDEXING OFF ZERO, BUT WE'LL DO WHAT MAKES THE MOST SENSE TO ENSURE THE MOST SEAMLESS CAPABILITY
# BETWEEN PYTHON AND THE DATABASE.
#
# Just updated all the personal id's so that they are starting off of 0. Thank you for spotting that
# Some global variables for convenience...

NOTE_MAPPING = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
Major = [2, 2, 1, 2, 2, 2, 1]
Minor = [2, 1, 2, 2, 1, 2, 2]

"""
    Connection to database and execution of fundamental code to query through information 
"""


def connectToDatabase():
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    # Set connection variable
    con = None
    try:
        # Establish connection to Database if exists/ has a stable connection
        con = psycopg2.connect(DATABASE_URL)
        #  create a new cursor
        cur = con.cursor()

        # execute an SQL statement to get the HerokuPostgres database version
        print('PostgreSQL database version:')

        # Execute SQL command
        cur.execute("SELECT key_id, key FROM keys ORDER BY key_id")

        # Fetch the first row if there is one, and print it out
        db_version = cur.fetchone()
        print("Fetching one row result:", db_version, "\n")

        print("Fetching all rows section results:")
        # Fetch all rows in database one by one
        # This can also be achieved with cur.fetchall() command but this format can help with searching if we don't
        # know the id of what we are looking for or the actual name of something in our database
        while db_version is not None:
            print(db_version)
            db_version = cur.fetchone()

        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Cause: {}'.format(error))

    # "Finally" section of try-catch statements are used to close objects and clean up resources
    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')


# scaleQualityAssignment: This function takes the two inputs from the main function (mainly the scale quality and
# designates which function to send it to for interpretation.
def scaleQualityAssignment(root, qualityNumber):
    quality = ''
    if int(qualityNumber) == 1:
        quality = "Major"
        majorScale(root, quality)

    elif int(qualityNumber) == 2:
        quality = "Minor"
        minorScale(root, quality)


# majorScale: The function that helps declare the parameters for a major scale.
def majorScale(root, quality):
    counter = NOTE_MAPPING[root]
    array = [NOTE_MAPPING[root]]
    for i in range(6):
        counter += Major[i]
        array.append(counter % 12)
    print("The scale degrees are: ")
    print(array)
    print("The scale is " + root + " " + quality + ". The notes are:")
    for i in range(7):
        key_list = list(NOTE_MAPPING.keys())
        val_list = list(NOTE_MAPPING.values())
        print(key_list[val_list.index(array[i])], end=" ")


# minorScale: The function that helps declare the parameters for a major scale.
def minorScale(root, quality):
    counter = NOTE_MAPPING[root]
    array = [NOTE_MAPPING[root]]
    for i in range(6):
        counter += Minor[i]
        array.append(counter % 12)
    print("The scale degrees are: ")
    print(array)
    print("The scale is " + root + " " + quality + ". The notes are:")
    for i in range(7):
        key_list = list(NOTE_MAPPING.keys())
        val_list = list(NOTE_MAPPING.values())
        print(key_list[val_list.index(array[i])], end=" ")


# Newest additions!

# crossover_function: Selects a random index from array melody_a and flips the ending halves between
# melody_a and melody_b.

def crossover_function(melody_a, melody_b):
    if len(melody_a) != len(melody_b):
        print("The two melodies chosen must be of same length")
        exit()
    c_point = randint(1, len(melody_a) - 1)
    return melody_a[0:c_point] + melody_b[c_point:], melody_b[0:c_point] + melody_a[c_point:]


# mutation_function: Selects two random indices from the array melody_a and flips the contents of their
# positions. Potentially could call mutation_function multiple times to scramble up the entire chromosome.
# TODO we can do that actually. We would want to use it as part of the termination function because we stop the
# algorithm when we run out of options/ met the desired amount of iterations specified
def mutation_function(melody_a):
    print(melody_a)

    startPoint, endPoint = [randint(1, len(melody_a) // 2), randint(len(melody_a) // 2 + 1, len(melody_a) - 1)]
    melody_a[startPoint], melody_a[endPoint] = melody_a[endPoint], melody_a[startPoint]
    return melody_a


# Main function: The place we start our program, and interact with the user based on their needs and specifications.
def main():
    root = input("What scale do you want?: ").capitalize()
    if len(root) > 2:
        print("Not a valid root note, maybe too many characters.")
        exit()
    elif root not in NOTE_MAPPING.keys():
        print(
            "Not a valid root note, choose one of the following: 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'.")
        exit()

    qualityNumber = input("Major or Minor? (Select 1 for major, 2 for minor): ")
    if len(qualityNumber) != 1:
        print("Not a valid scale quality, maybe too many characters.")
        exit()
    if int(qualityNumber) < 1 or int(qualityNumber) > 2:
        print("Not a valid scale quality, look over the options again.")
        exit()

    scaleQualityAssignment(root, qualityNumber)


connectToDatabase()
# main()
