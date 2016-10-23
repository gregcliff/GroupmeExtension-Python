import random


def generate_roast():

    word1 = None
    word2 = None
    word3 = None

    with open("resources/mean_shakespeare1.txt") as f:
        for i, line in enumerate(f.readlines()):
            if random.random() * float(i + 1) < 1:
                word1 = line.strip()

    with open("resources/mean_shakespeare2.txt") as f2:
        for i, line in enumerate(f2.readlines()):
            if random.random() * float(i + 1) < 1:
                word2 = line.strip()

    with open("resources/mean_shakespeare3.txt") as f3:
        for i, line in enumerate(f3.readlines()):
            if random.random() * float(i + 1) < 1:
                word3 = line.strip()

    r = random.randint(1, 10)
    if r < 4:
        return word1 + " " + word2 + " " + word3
    elif r > 7:
        return word2 + " " + word3
    else:
        return word1 + " " + word3
