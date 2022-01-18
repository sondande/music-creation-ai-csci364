# I HATE COMPUTER SCIENCE
# CHROMOSOMES: the random four-note melodies
# GENES: the notes within a given melodies
# FITNESS FUNCTION: Rating how well the melodies meets the constraints given by the user.
#   -> Desiring a major key, root, type of scale used, and rating function

NOTE_MAPPING = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
Major = [2, 2, 1, 2, 2, 2, 1]
Minor = [2, 1, 2, 2, 1, 2, 2]


def scale_to_scaleDegrees(root, qualityNumber):
    quality = ''

    if int(qualityNumber) == 1:
        quality = "Major"
    elif int(qualityNumber) == 2:
        quality = "Minor"

    print("The scale is " + root + " " + quality)
    # ADD MINOR FUNCTIONALITY, AND FIGURE OUT AN EASIER WAY TO REFER TO THE ARRAYS FROM THE USER INPUT
    counter = NOTE_MAPPING[root]
    array = [NOTE_MAPPING[root]]
    for i in range(6):
        counter += Major[i]
        array.append(counter % 12)
    print(array)

    for i in range(6):
        print(Major[array[i]])


def main():
    root = input("What scale do you want?: ").capitalize()
    if len(root) > 2:
        print("Not a valid root note, maybe too many characters.")
        exit()
    elif root not in NOTE_MAPPING.keys():
        print(
            "Not a valid root note, choose one of the following: 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'.")
        exit()

    quality = input("Major or Minor? (Select 1 for major, 2 for minor): ")
    if len(quality) != 1:
        print("Not a valid scale quality, maybe too many characters.")
        exit()
    if int(quality) < 1 or int(quality) > 2:
        print("Not a valid scale quality, look over the options again.")
        exit()

    scale_to_scaleDegrees(root, quality)


main()
