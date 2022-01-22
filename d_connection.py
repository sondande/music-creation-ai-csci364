"""
    All methods related to connecting and interacting with the Heroku Database located here
"""

import os
import psycopg2

"""
    Used to imported command to interact with database and return desired information
"""


def execute_query_command(sql_command, values = None):
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

def insert_population_list(generation, population_list):
    """ insert multiple vendors into the vendors table  """
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    sql = "INSERT INTO population(generation, population_list) VALUES(%s,%s)"
    con = None
    try:
        # Establish connection to Database if exists/ has a stable connection
        con = psycopg2.connect(DATABASE_URL)

        # Create new cursor
        cur = con.cursor()

        # execute the INSERT statement
        cur.execute(sql, (generation,population_list))
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
# """
#     Connection to database and execution of fundamental code to query through information
#
#     # Shows the fundamentals of connecting, utilizing, and executing commands to interact with Postgres database
# """
#
#
# def connectToDatabase():
#     # Grabs environment variable set in application configurations
#     DATABASE_URL = os.environ.get('DATABASE_URL')
#     # Set connection variable
#     con = None
#     try:
#         # Establish connection to Database if exists/ has a stable connection
#         con = psycopg2.connect(DATABASE_URL)
#
#         # Create new cursor
#         cur = con.cursor()
#
#         # Execute SQL command
#         cur.execute("SELECT key_id, key FROM keys ORDER BY key_id")
#
#         # Fetch the first row if there is one, and print it out
#         db_version = cur.fetchone()
#         print("Fetching one row result:", db_version, "\n")
#
#         print("Fetching all rows section results:")
#         # Fetch all rows in database one by one
#         # This can also be achieved with cur.fetchall() command but this format can help with searching if we don't
#         # know the id of what we are looking for or the actual name of something in our database
#         while db_version is not None:
#             print(db_version)
#             db_version = cur.fetchone()
#
#         # close the communication with the HerokuPostgres
#         cur.close()
#     except Exception as error:
#         print('Cause: {}'.format(error))
#
#     # "Finally" section of try-catch statements are used to close objects and clean up resources
#     finally:
#         # close the communication with the database server by calling the close()
#         if con is not None:
#             con.close()
#             # print('Database connection closed.')

