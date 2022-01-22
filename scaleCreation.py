# Mark Ligonde and Sagana Ondande
# Professor Adam Eck
# CS364
# Final Artificial Intelligence Project
#
# I affirm that we have adhered to the Honor Code on this assignment - Mark Ligonde & Sagana Ondande

import os
import psycopg2
from random import randint, random
from collections import OrderedDict

# NOTE_MAPPING = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
Major = [2, 2, 1, 2, 2, 2, 1]
Minor = [2, 1, 2, 2, 1, 2, 2]

"""
    Connection to database and execution of fundamental code to query through information 
    
    # Shows the fundamentals of connecting, utilizing, and executing commands to interact with Postgres database 
"""


def connectToDatabase():
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    # Set connection variable
    con = None
    try:
        # Establish connection to Database if exists/ has a stable connection
        con = psycopg2.connect(DATABASE_URL)

        # Create new cursor
        cur = con.cursor()

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
            # print('Database connection closed.')


"""
    Used to imported command to interact with database and return desired information
"""


def execute_query_command(sql_command):
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    # Set connection variable
    con = None
    try:
        # Establish connection to Database if exists/ has a stable connection
        con = psycopg2.connect(DATABASE_URL)

        # Create new cursor
        cur = con.cursor()

        """
            SQL Command Execution Section 
        """

        # Execute SQL command
        cur.execute(sql_command)

        # Fetch all that meet the query result
        db_result = cur.fetchall()

        # Returns a single array with the results from the query
        return [i[0] for i in db_result]

        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Cause: {}'.format(error))
        # Return string "Error" to prevent type error later in code when using returned value
        return "Error"
    # "Finally" section of try-catch statements are used to close objects and clean up resources
    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            # print('Database connection closed.')
    # Included just in case of complication
    return "Completed"


"""
    Create the chromatic scale for use to create scales
"""


def chromatic_scale_degree(root):
    # Find root scale degree in database
    sql_c = "SELECT scale_degree FROM chromatic_scale WHERE note=\'" + root + "\' or e_harm_note=\'" + root + "\';"
    root_scale_degree = execute_query_command(sql_c)[0]
    return root_scale_degree


"""
    Scale Creation: Creates scale given based off scale information given
"""


def chromatic_scale_creation(root, scale):
    # Find root scale degree in database
    root_scale_degree = int(chromatic_scale_degree(root))
    print("root scale degree result", root_scale_degree)
    sql_c = "SELECT interval_transition FROM scale_type WHERE scale_type_full_name=\'" + scale + "\';"
    scale_transition_result = execute_query_command(sql_c)[0]
    print(scale_transition_result)
    scale_transition_result = [int(s) for s in scale_transition_result.split(", ") if s.isdigit()]
    # Takes root scale degree and adds transitions to it to get the next scale degree of that scale and add to an array
    scale_degree_scale = [root_scale_degree]
    last_spot = root_scale_degree
    for degree in scale_transition_result:
        last_spot = last_spot + degree
        if last_spot > 12:
            last_spot -= 12
        scale_degree_scale.append(last_spot)
    print(scale_degree_scale)
    return scale_degree_scale

### GENETIC ALGORITHM ####

# Newest additions!
"""
    Crossover_function: Selects a random index from array melody_a and flips the ending halves between
        melody_a and melody_b.
"""


def crossover_function(melody_a, melody_b):
    if len(melody_a) != len(melody_b):
        print("The two melodies chosen must be of same length")
        exit()
    c_point = randint(1, len(melody_a) - 1)
    return melody_a[0:c_point] + melody_b[c_point:], melody_b[0:c_point] + melody_a[c_point:]


"""
    Mutation_function: Selects two random indices from the array melody_a and flips the contents of their
        positions. Potentially could call mutation_function multiple times to scramble up the entire chromosome
"""


# TODO we can do that actually. We would want to use it as part of the termination function because we stop the
#   algorithm when we run out of options/ met the desired amount of iterations specified
def mutation_function(melody_a):
    print(melody_a)

    startPoint, endPoint = [randint(1, len(melody_a) // 2), randint(len(melody_a) // 2 + 1, len(melody_a) - 1)]
    melody_a[startPoint], melody_a[endPoint] = melody_a[endPoint], melody_a[startPoint]
    return melody_a
