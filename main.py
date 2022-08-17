import random


class Conteudo:

    def __init__(self):
        self.word = ""
        self.meanings = []

    def __str__(self):
        return self.word + " MEANS: " + self.meanings


def appender(pick, already_read, guessed, counter):
    already_read.append(pick)
    already_read.sort()
    print("\n" + str(counter-guessed) + " CHOSEN!" +
          "\n" + str(guessed) + " WRITEN!\n"+str(already_read))
    return already_read


def swap(meanings):
    meanings = meanings.split("(")[1:]
    random.shuffle(meanings)
    meanings2 = ["(" + meaning for meaning in meanings]
    return "".join(meanings2)


def removesArticle(word):
    if word.find('a ') == 0:
        return(word[2:])
    if word.find('an ') == 0:
        return(word[3:])
    return word


def orRemover(m):
    or1 = m.split("/")
    random.shuffle(or1)
    or1 = [or1[0]] + [removesArticle(w) for w in or1[1:]]
    last = or1.pop()
    return ", ".join(or1) + ' or ' + last


def removeLargeOr(meanings):
    while '<' in meanings:
        or1 = meanings[meanings.index('<')+1:meanings.index('>')]
        meanings = meanings[:meanings.index('<')] + orRemover(or1) + meanings[meanings.index('>') + 1:]
    return(meanings)


def removeSmallOr(or1):
    if "/" not in or1:
        return or1
    s = len(or1)-1
    found = False
    for i in reversed(range(len(or1))):
        if or1[i] == "/":
            found = True
        char = or1[i]
        if or1[i] in [" ", '"', ",", ".", ";", ":", ")", "("] or i == 0:
            if found:
                found = False
                or1 = or1[:i+1] + orRemover(or1[i+1: s]) + or1[s:]
            s = i
    return or1


def extractMeaning(meanings):
    swapped = swap(meanings)
    swapped = swapped.replace("//", "&*")
    or1 = removeLargeOr(swapped)
    or2 = removeSmallOr(or1)
    return(or2.replace("&*", "/"))


def word_is_present_in(w, list, dict):
    for i in range(len(list)):
        if dict[list[i]].word == w:
            return True
    return False


def process_file():
    keywords = open("Keywords.txt", "r")

    dictionary = []
    for line in keywords.readlines():
        if line != "\n":

            while line[0].isdigit():  # removes first digits
                line = line[1:]

            line = line.replace('\n', "")  # removes new lines

            wm = line.split(" - ")  # splits word and its meaning

            content = Conteudo()
            content.word = wm[0]

            content.meanings = wm[1]

            dictionary.append(content)

    """
    for content in dictionary:
        print(content)
    """
    keywords.close()

    return dictionary


def m_to_w(dictionary):

    # Starts the game
    i = 1
    already_read = []
    counter = 0
    guessed = 0
    while True:  # Runs the game

        #  Searches for an unused word to be guessed
        counter += 1
        while True:
            pick = random.randint(0, len(dictionary)-1)
            if pick not in already_read:
                break

        # Prompts the user to guess it
        guess = input('\nLVL ' + str(i) + ': What word represents ' + extractMeaning(dictionary[pick].meanings) + ' ?\n')
        if guess == dictionary[pick].word:
            i += 3
            guessed += 1
            already_read = appender(pick, already_read, guessed, counter)
            continue

        print('OPTIONS:')

        falses = random.sample(range(0, len(dictionary)), 5)
        while word_is_present_in(guess, falses, dictionary):
            falses = random.sample(range(0, len(dictionary)), 5)

        if pick not in falses:
            correct = random.randint(0, 4)
            falses[correct] = pick
        else:
            correct = falses.index(pick)

        for j in range(5):
            print(str(j+1) + " -> " + dictionary[falses[j]].word)

        guessed_number = int(input())
        if correct == guessed_number-1:
            already_read = appender(falses[correct], already_read, guessed, counter)
        elif guessed_number == 0 and counter != 1:
            print("\nRight answer was: " + dictionary[falses[correct]].word + "\n")
            print("You guessed with no help " + str(100 * guessed / (counter-1)) + "% of the time !")
            break
        else:
            print("\nWRONG right answer was: " + dictionary[falses[correct]].word + "\n")
            print("You guessed with no help " + str(100*guessed/counter) + "% of the time !")
            break

        i += 1

def testSwaps(dictionary):
    for word in dictionary:
        print(word.word + " = " + extractMeaning(word.meanings))

if __name__ == '__main__':

    d = process_file()
    #testSwaps(d)
    # w_to_m(d)
    m_to_w(d)
