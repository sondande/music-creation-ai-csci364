"""
    All methods related to connecting and interacting with the Heroku Database located here
"""

import os
import psycopg2

"""
    Find Scale degree
"""
def scale_degree_search(scale_degree):
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    # Set connection variable
    sql_command = "SELECT note FROM chromatic_scale WHERE scale_degree=\'" + str(scale_degree) + "\';"
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
    Only SELECT SQL command
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
    Inserts population list for current generation into population table in database
"""


def insert_population_list(population_list):
    """ insert multiple vendors into the vendors table  """
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    sql = "INSERT INTO population(population_list) VALUES(%s)"
    con = None
    try:
        # Establish connection to Database if exists/ has a stable connection
        con = psycopg2.connect(DATABASE_URL)

        # Create new cursor
        cur = con.cursor()

        # execute the INSERT statement
        cur.execute(sql, (population_list,))
        # commit the changes to the database
        con.commit()
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if con is not None:
            con.close()
    return True

"""
    Inserts melody for current_population into melodies table in database
"""

def insert_melodies(generation, melody):
    """ insert multiple vendors into the vendors table  """
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    sql = "INSERT INTO melodies(generation, melody) VALUES(%s,%s)"
    con = None
    try:
        # Establish connection to Database if exists/ has a stable connection
        con = psycopg2.connect(DATABASE_URL)

        # Create new cursor
        cur = con.cursor()

        # execute the INSERT statement
        cur.execute(sql, (generation,melody))
        # commit the changes to the database
        con.commit()
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if con is not None:
            con.close()
    return True

