"""
    Method that creates the notes for the melody through the utilization of genetic algorithms
    Constraints: The Scale and Key inputs given by user
"""
from random import randint
from d_connection import execute_query_command, insert_population_list, insert_melodies, update_table

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


def mutation_function(melody_a):

    startPoint, endPoint = [randint(1, len(melody_a) // 2), randint(len(melody_a) // 2 + 1, len(melody_a) - 1)]
    melody_a[startPoint], melody_a[endPoint] = melody_a[endPoint], melody_a[startPoint]
    return melody_a


def crossover_function(melody_a, melody_b):
    if len(melody_a) != len(melody_b):
        exit()
    c_point = randint(1, len(melody_a) - 1)
    return melody_a[0:c_point] + melody_b[c_point:], melody_b[0:c_point] + melody_a[c_point:]


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
        self.current_generation = 1
        self.current_generation_fitness_score = 0
        self.chord_progression_scales_list = chord_progression_scales_list
        self.user_population_size = None

    """
        Creates the initial population for our genetic algorithm using Heuristic initialization for some of the populationm,
        and then random initilization for the rest of our population to allow diversity 
    """

    def initial_population(self, population_size, notes_count = 5):
        # Population = [initial_population size][Length of melody][Note]   -> Note is for access to chromatic note degree
        # [[1,3,5,1], [1,2,3,4], [1,2,6,11]]

        ## Create initial_population array
        initial_population = []
        self.user_population_size = population_size

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
        insert_population_list(str(self.current_generation), str(len(initial_population)), str(initial_population))

        # Insert Each Melody from initial_population into melodies table in database
        for melody in initial_population:
            insert_melodies(self.current_generation, melody)
        self.current_population = initial_population

    """
    
    """

    def new_gen_pop_dev(self,generation, new_pop):
        # Add Initial Population to Database table population
        insert_population_list(str(self.current_generation), str(len(new_pop)),str(new_pop))

        # Insert Each Melody from initial_population into melodies table in database
        for melody in new_pop:
            insert_melodies(str(generation), melody)
        self.current_population = new_pop

    """
        Uses the fitness function to be used on constraint of chord progression desired by user
    """


    def fitness_function(self,i):
        # Get all chord progression base melodies to compare for fitness
        # print(self.bass_cp)
        # Select every melody
        current_chord_index = 0
        for melody in self.current_population:
            if current_chord_index >= len(self.chord_progression):
                current_chord_index = len(self.chord_progression)-1
            fitness_score = 0
            # Rate melody on:
            # Checks if it is only the baseline of our chord progression
            if melody == self.chord_progression:
                fitness_score-=1

            counter = 0
            prior_leap_result = 0
            for note in melody:
                if current_chord_index >= len(self.chord_progression):
                    current_chord_index = len(self.chord_progression) - 1
                # Is it base note of the progression? or in the scale
                if note == self.chord_progression[current_chord_index]:
                    # it is a base note
                    fitness_score -=1
                    current_chord_index += 1
                    continue

                # in key contraint by user
                if note in self.current_scale:
                    fitness_score += 1

                # Checks if the note is in the chord progression's scale
                if note == self.chord_progression[current_chord_index]:
                    fitness_score += 1
                    current_chord_index += 1
                    continue

                    # Check if the note is also in our own scale rn
                    # if so, gives a bigger fitness score as our ear won't hear as clearly the chord transition but it
                    # occurs through this
                    if note in self.current_scale:
                        fitness_score += 3
                        # Is it base note of the progression? or in the scale
                        if note != self.chord_progression[current_chord_index]:
                            # it is a base note
                            fitness_score += 2
                            current_chord_index += 1
                            continue

                if 1 < counter <= len(melody) - 2:
                    # Leap larger than a m3
                    a = melody[counter-1]
                    b = melody[counter]
                    if isinstance(a, list):
                        a = a[len(a) -1]
                    if isinstance(b, list):
                        b= b[len(b) - 1]
                    if abs(a-b) > 3:
                        # Controlled Leap
                        if abs(b - prior_leap_result) <= 3:
                            fitness_score += 7
                        # Uncontrolled leap
                        else:
                            fitness_score -= 2
                        prior_leap_result = abs(a-b)

                counter += 1
            # Store fitness score specific melody in database
            SQL_set = "SET fitness_score = %s" % str(fitness_score)

            if isinstance(melody, list) and isinstance(melody[0], int):
                SQL_where = "WHERE melody = array%s;" % str(melody)

            update_table("melodies", SQL_set, SQL_where)
            # Add to cumulative score in class variable
            self.current_generation_fitness_score += fitness_score
        # Updates population table with cummulative fitness for population
        SQL_set = "SET population_fitness = %s" % str(self.current_generation_fitness_score)

        SQL_where = "WHERE generation = %s;" % str(self.current_generation+i)
        self.current_generation += i

        update_table("population", SQL_set, SQL_where)
        return True

    ### GENETIC ALGORITHM ####

    # Newest additions!
    """
        Crossover_function: Selects a random index from array melody_a and flips the ending halves between
            melody_a and melody_b.
    """

    """
        Mutation_function: Selects two random indices from the array melody_a and flips the contents of their
            positions. Potentially could call mutation_function multiple times to scramble up the entire chromosome
    """

    """
        Selection of Genetic Algorithm that chooses the best chromosome to put in our next generation population 
    """
    def selection(self):
        # Calculate average fitness per chromosome of current generation
        avg_current_fit = self.current_generation_fitness_score / len(self.current_population)
        # Calculate average fitness per chromosome of prior generation
        print("select population_size from population WHERE generation = \'%s\';" % str(self.current_generation - 1))
        # Set as constant due to errors
        prior_gen_size = self.user_population_size
        prior_gen_fit = 1
        avg_last_gen_fit = prior_gen_fit/prior_gen_size
        # Compare the averages
        new_pop=[]
        if abs(avg_current_fit - avg_last_gen_fit) > 0:
            current_gen_melody = execute_query_command(
                "select melody from melodies WHERE generation = %s and fitness_score > %s;" % (str(self.current_generation), str(abs(avg_current_fit - avg_last_gen_fit))))
            new_pop+= (current_gen_melody)
            if self.current_generation > 1:
                prior_gen_melody = execute_query_command("select melody from melodies WHERE generation = %s and fitness_score > %s;" % (str(self.current_generation-1), str(abs(avg_current_fit - avg_last_gen_fit))))
                new_pop+= (prior_gen_melody)
            if self.current_generation == 1:
                pass
        else:
            new_pop += self.current_population[0, len(self.current_population) // 4]

        n = []
        for s in range(len(new_pop)):
            if s % 2 == 0:
                n.append(new_pop[s])
        self.user_population_size = len(self.current_population)
        self.current_population = n

        return n
