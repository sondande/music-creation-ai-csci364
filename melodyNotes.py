"""
    Method that creates the notes for the melody through the utilization of genetic algorithms
    Constraints: The Scale and Key inputs given by user
"""
from random import randint
from d_connection import execute_query_command, insert_population_list, insert_melodies

"""
    Population Model: 
    
    -> Follows Generational Model as a means to limit reproduction of similar data and allow 
    flexibility to create new constraints (creation of new scales) to allow us the ability to emulate the "imperfection" 
    
    -> Stores population between each generation Use this object to connect with the database and get 
    the associated generation We keep all generation in the database to be used as references and to start with the same 
    initial population for everyone as we use the heuristic of "Standard" chord progressions and using their base notes 
    as the melody notes are the heuristic side. Randomly generated part of the initial population will be generated 
    based on the user 
"""


class Population:
    """
         Will only use the constructor once to create program population. Will be managed from musicCreationDriver.py. We will use this as a
         means to add to our population. We store in the object the current population we have
    """

    # Global variables for Reference of Key, Scale Type, and Chromatic Scale Generated in Main.py
    def __init__(self, root, KEY_SCALE, scale_type, CHROMATIC_NOTE_MAPPING, chord_progression, chord_progression_scales_list):
        self.current_root = root
        self.current_scale = KEY_SCALE
        self.scale_type = scale_type
        self.chord_progression = chord_progression
        self.chromatic_scale = CHROMATIC_NOTE_MAPPING
        self.current_population = None
        self.current_generation = None
        # self.bass_cp = bass_c_list
        self.chord_progression_scales_list = chord_progression_scales_list

    """
        Creates the initial population for our genetic algorithm using Heuristic initialization for some of the populationm,
        and then random initilization for the rest of our population to allow diversity 
    """

    def initial_population(self, generation, population_size, notes_count = 5):
        # Population = [initial_population size][Length of melody][Note]   -> Note is for access to chromatic note degree
        # [[1,3,5,1], [1,2,3,4], [1,2,6,11]]

        ## Create initial_population array
        initial_population = []

        ### Go through database to get notes for heauristic created initial_population
        basic_chord_progressions = execute_query_command("SELECT chord_progression_melody FROM chord_progressions;")
        for chord_p in basic_chord_progressions:
            initial_population.append(chord_p)

        # Ensure each initial chromosome is of length 4. If not, insert '0' at index 0 or after last index as that maintains
        # a common ideology of "standard" classical music theory
        for i in range(len(initial_population)):
            while len(initial_population[i]) < notes_count:
                if initial_population[i] == 0:
                    initial_population[i].append(0)
                else:
                    initial_population[i].insert(0,0)

        # Creating randomized section of initial population by filling the last bit with randomized combinations
        while len(initial_population) < population_size:
            # Random Chromosome initialization
            random_chrom = []
            # Choose a random index number from our scale to create base notes of a chord progression
            # TOOD can be used as part of our new chord progression ideas. Will be evaluated in the fitness function
            for i in range(notes_count):
                # Add to Chromosome random scale degree from our current scale through choosing a random index
                random_chrom.append(self.current_scale[randint(0,len(self.current_scale)-1)])
            initial_population.append(random_chrom)

        # Add Initial Population to Database table population
        insert_population_list(str(initial_population))

        # Insert Each Melody from initial_population into melodies table in database
        for melody in initial_population:
            insert_melodies(generation, melody)
        self.current_population = initial_population
        self.current_generation = generation

    """
        Uses the fitness function to be used on constraint of chord progression desired by user
    """


    def fitness_function(self):
        # Get all chord progression base melodies to compare for fitness
        #print(self.bass_cp)
        # Select every melody
        for melody in self.current_population:
            fitness_score = 0
            # Rate melody on:
            # Checks if it is only the baseline of our chord progression 
            if melody == self.chord_progression:
                fitness_score-=1
            for note in melody:
                # in key contraint by user
                if note in self.current_scale:
                    fitness_score += 1




        return


    def parent_selection(self):
        return


    ### GENETIC ALGORITHM ####

    # Newest additions!
    """
        Crossover_function: Selects a random index from array melody_a and flips the ending halves between
            melody_a and melody_b.
    """


    def crossover_function(self,melody_a, melody_b):
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
    def mutation_function(self,melody_a):
        print(melody_a)

        startPoint, endPoint = [randint(1, len(melody_a) // 2), randint(len(melody_a) // 2 + 1, len(melody_a) - 1)]
        melody_a[startPoint], melody_a[endPoint] = melody_a[endPoint], melody_a[startPoint]
        return melody_a