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


def insert_population_list(generation, population_size, population_list):
    """ insert multiple vendors into the vendors table  """
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    sql = "INSERT INTO population(generation, population_size, population_list) VALUES(%s,%s,%s);"
    con = None
    try:
        # Establish connection to Database if exists/ has a stable connection
        con = psycopg2.connect(DATABASE_URL)

        # Create new cursor
        cur = con.cursor()

        # execute the INSERT statement
        cur.execute(sql, (generation, population_size, population_list))
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
    # inserts into database table only unique items using ON CONFLICT(melody) DO NOTHING where if there is a duplicate melody, don't do anything/don't add
    sql = "INSERT INTO melodies(generation, melody) VALUES(%s,%s) ON CONFLICT(melody) DO NOTHING"
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

"""
    Update table with Fitness scores
"""

def update_table(table,set_statement,where_statement):
    """ update vendor name based on the vendor id """
    sql = "UPDATE %s %s %s" % (str(table),str(set_statement),str(where_statement))
    print(sql)
    # Grabs environment variable set in application configurations
    DATABASE_URL = os.environ.get('DATABASE_URL')
    con = None
    updated_rows = 0
    try:
        # Establish connection to Database if exists/ has a stable connection
        con = psycopg2.connect(DATABASE_URL)

        # create a new cursor
        cur = con.cursor()
        # execute the UPDATE  statement
        cur.execute(sql)
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        con.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return updated_rows

