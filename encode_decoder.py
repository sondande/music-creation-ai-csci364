"""
    File with all methods to encode and decode formats. Used when specifically translating Genotype and Phenotypes
"""
import d_connection

"""
    Decode input array to note names
"""


def decodeNotes(encoded_scale):
    scale_notes = []
    for scale_degree in encoded_scale:
        sql = "SELECT note FROM chromatic_scale WHERE scale_degree=\'" + str(scale_degree) + "\';"
        note_name = d_connection.execute_query_command(sql)[0]
        scale_notes.append(note_name)

    return scale_notes
