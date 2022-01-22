# Mark Ligonde and Sagana Ondande
# Professor Adam Eck
# CS364
# Final Artificial Intelligence Project
#
# I affirm that we have adhered to the Honor Code on this assignment - Mark Ligonde & Sagana Ondande

import os
import psycopg2
from d_connection import execute_query_command
from random import randint, random
from collections import OrderedDict


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
    sql_c = "SELECT interval_transition FROM scale_type WHERE scale_type_full_name=\'" + scale + "\';"
    scale_transition_result = execute_query_command(sql_c)[0]
    scale_transition_result = [int(s) for s in scale_transition_result.split(", ") if s.isdigit()]

    # Takes root scale degree and adds transitions to it to get the next scale degree of that scale and add to an array
    scale_degree_scale = [root_scale_degree]
    last_spot = root_scale_degree
    for degree in scale_transition_result:
        last_spot = last_spot + degree
        if last_spot > 12:
            last_spot -= 12
        scale_degree_scale.append(last_spot)
    return scale_degree_scale
