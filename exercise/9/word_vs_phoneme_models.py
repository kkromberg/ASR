import numpy as np
import json
import operator
import matplotlib.pyplot as plt
import collections


# plotting for b and c
def plot(num_oberservations):
    separated_tuples = zip(*num_oberservations)
    print separated_tuples
    counter = 0
    x_range = []
    for elem in separated_tuples[0]:
        x_range.append(counter)
        counter += 1
    print x_range

    #plt.scatter(*separated_tuples)
    plt.title('Number of observation for each mixture')
    plt.xlabel('Mixture')
    plt.ylabel('Amount of observations')
    plt.xticks(x_range, separated_tuples[0])
    plt.plot(x_range, separated_tuples[1])
    plt.plot(x_range, separated_tuples[1], 'or')
    plt.show()

####################################### task b #######################################
def num_obersvations_word(src_file):
    word_alignment = open(src_file, 'r')
    all_prefixes = [1, 13, 22, 28, 37, 46, 55, 67, 82, 88, 97]
    num_observations = {'silence': 0, 'zero': 0, 'one': 0, 'two': 0, 'three': 0, 'four': 0, 'five': 0, 'six': 0,
                        'seven': 0, 'eight': 0, 'nine': 0, 'oh': 0}

    for line in word_alignment:
        line_int = np.fromstring(line, dtype=int, sep=' ')
        current_prefix = line_int[0]
        for elem in line_int:
            if elem in all_prefixes and current_prefix != elem:
                current_prefix = elem
                if elem == 1:
                    num_observations['zero'] += 1
                elif elem == 13:
                    num_observations['one'] += 1
                elif elem == 22:
                    num_observations['two'] += 1
                elif elem == 28:
                    num_observations['three'] += 1
                elif elem == 37:
                    num_observations['four'] += 1
                elif elem == 46:
                    num_observations['five'] += 1
                elif elem == 55:
                    num_observations['six'] += 1
                elif elem == 67:
                    num_observations['seven'] += 1
                elif elem == 82:
                    num_observations['eight'] += 1
                elif elem == 88:
                    num_observations['nine'] += 1
                elif elem == 97:
                    num_observations['oh'] += 1
            # count each silence state as word
            elif elem == 0:
                num_observations['silence'] += 1
    # close file
    word_alignment.close()
    # write count to file
    num_observations_sorted = sorted(num_observations.items(), key=lambda x: x[1], reverse=True)
    count = open('num_observations_per_mixture.word', 'w')
    for elem in num_observations_sorted:
        count.write(str(elem[0]) + ' ' + str(elem[1]) + '\n')

    count.close()
    # plotting
    plot(num_observations_sorted)
#num_obersvations_word('alignment.word')

####################################### task c #######################################
def num_obersvations_phoneme(src_file):
    word_alignment = open(src_file, 'r')
    all_prefixes = [0, 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55]
    num_observations = {'silence': 0, 'ah': 0, 'ax': 0, 'ay': 0, 'f': 0, 'eh': 0, 'ey': 0, 'ih': 0, 'iy':0, 'k': 0, 'n': 0,
                        'ow': 0, 's': 0, 'r':0, 't':0, 'th':0, 'uw':0, 'v':0, 'w':0, 'z':0}


    for line in word_alignment:
        line_int = np.fromstring(line, dtype=int, sep=' ')
        current_prefix = line_int[0]
        for elem in line_int:
            if elem in all_prefixes and current_prefix != elem:
                current_prefix = elem
                if elem == 1:
                    num_observations['ah'] += 1
                elif elem == 4:
                    num_observations['ax'] += 1
                elif elem == 7:
                    num_observations['ay'] += 1
                elif elem == 10:
                    num_observations['f'] += 1
                elif elem == 13:
                    num_observations['eh'] += 1
                elif elem == 16:
                    num_observations['ey'] += 1
                elif elem == 19:
                    num_observations['ih']
                elif elem == 22:
                    num_observations['iy'] += 1
                elif elem == 25:
                    num_observations['k'] += 1
                elif elem == 28:
                    num_observations['n'] += 1
                elif elem == 31:
                    num_observations['ow'] += 1
                elif elem == 34:
                    num_observations['s'] += 1
                elif elem == 37:
                    num_observations['r'] += 1
                elif elem == 40:
                    num_observations['t'] += 1
                elif elem == 43:
                    num_observations['th'] += 1
                elif elem == 46:
                    num_observations['uw'] += 1
                elif elem == 49:
                    num_observations['v'] += 1
                elif elem == 52:
                    num_observations['w'] += 1
                elif elem == 55:
                    num_observations['z'] += 1
                elif elem == 0:
                    num_observations['silence'] += 1
            # count each silence state as word
            elif elem == 0:
                num_observations['silence'] += 1
    # close file
    word_alignment.close()
    # write count to file
    num_observations_sorted = sorted(num_observations.items(), key=lambda x: x[1], reverse=True)
    count = open('num_observations_per_mixture.phoneme', 'w')
    for elem in num_observations_sorted:
        count.write(str(elem[0]) + ' ' + str(elem[1]) + '\n')

    count.close()
    # plotting
    plot(num_observations_sorted)
#num_obersvations_phoneme('alignment.phoneme')

####################################### task c #######################################
def translate_word_to_phoneme(word):
    """
    Translate a word to corresponding phonemes.
    Each word is hard coded.
    :param word:
    :return:
    """

    result = []
    # Oh
    if len(set(word)) == 3:
        phoneme_state = 31
        for i in range(len(word)):
            result.append(phoneme_state)
            if i < len(word)-1:
                if word[i] != word[i+1]:
                    phoneme_state += 1
    # Two, Eight
    elif len(set(word)) == 6:
        second_part = False
        # Two
        if word[0] == 22:
            phoneme_state = 40
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i+1]) > 2 and not second_part:
                            phoneme_state = 46
                            second_part = True
                        else:
                            phoneme_state += 1
        # Eight
        else:
            phoneme_state = 16
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i + 1]) > 2 and not second_part:
                            phoneme_state = 40
                            second_part = True
                        else:
                            phoneme_state += 1
    # One, Three, Four, Five, Nine
    elif len(set(word)) == 9:
        second_part = False
        third_part  = False
        # One
        if word[0] == 13:
            phoneme_state = 52
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i+1]) > 2 and not second_part:
                            phoneme_state = 1
                            second_part = True
                        elif abs(word[0] - word[i+1]) > 5 and not third_part:
                            phoneme_state = 28
                            third_part = True
                        else:
                            phoneme_state += 1
        # Three
        elif word[0] == 28:
            phoneme_state = 43
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i + 1]) > 2 and not second_part:
                            phoneme_state = 37
                            second_part = True
                        elif abs(word[0] - word[i + 1]) > 5 and not third_part:
                            phoneme_state = 22
                            third_part = True
                        else:
                            phoneme_state += 1
        # Four
        elif word[0] == 37:
            phoneme_state = 10
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i + 1]) > 2 and not second_part:
                            phoneme_state = 31
                            second_part = True
                        elif abs(word[0] - word[i + 1]) > 5 and not third_part:
                            phoneme_state = 37
                            third_part = True
                        else:
                            phoneme_state += 1
        # Five
        elif word[0] == 46:
            phoneme_state = 10
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i + 1]) > 2 and not second_part:
                            phoneme_state = 7
                            second_part = True
                        elif abs(word[0] - word[i + 1]) > 5 and not third_part:
                            phoneme_state = 49
                            third_part = True
                        else:
                            phoneme_state += 1
        # Nine
        elif word[0] == 88:
            phoneme_state = 28
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i + 1]) > 2 and not second_part:
                            phoneme_state = 7
                            second_part = True
                        elif abs(word[0] - word[i + 1]) > 5 and not third_part:
                            phoneme_state = 28
                            third_part = True
                        else:
                            phoneme_state += 1

    # Zero, Six
    elif len(set(word)) == 12:
        second_part = False
        third_part  = False
        fourth_part = False
        # Zero
        if word[0] == 1:
            phoneme_state = 55
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i + 1]) > 2 and not second_part:
                            phoneme_state = 19
                            second_part = True
                        elif abs(word[0] - word[i + 1]) > 5 and not third_part:
                            phoneme_state = 37
                            third_part = True
                        elif abs(word[0] - word[i + 1]) > 8 and not fourth_part:
                            phoneme_state = 31
                            fourth_part = True
                        else:
                            phoneme_state += 1
        # Six
        else:
            phoneme_state = 34
            for i in range(len(word)):
                result.append(phoneme_state)
                if i < len(word) - 1:
                    if word[i] != word[i + 1]:
                        if abs(word[0] - word[i + 1]) > 2 and not second_part:
                            phoneme_state = 19
                            second_part = True
                        elif abs(word[0] - word[i + 1]) > 5 and not third_part:
                            phoneme_state = 25
                            third_part = True
                        elif abs(word[0] - word[i + 1]) > 8 and not fourth_part:
                            phoneme_state = 34
                            fourth_part = True
                        else:
                            phoneme_state += 1
    # Seven
    elif len(set(word)) == 15:
        second_part = False
        third_part  = False
        fourth_part = False
        fifth_part  = False
        # Zero
        phoneme_state = 34
        for i in range(len(word)):
            result.append(phoneme_state)
            if i < len(word) - 1:
                if word[i] != word[i + 1]:
                    if abs(word[0] - word[i + 1]) > 2 and not second_part:
                        phoneme_state = 13
                        second_part = True
                    elif abs(word[0] - word[i + 1]) > 5 and not third_part:
                        phoneme_state = 49
                        third_part = True
                    elif abs(word[0] - word[i + 1]) > 8 and not fourth_part:
                        phoneme_state = 4
                        fourth_part = True
                    elif abs(word[0] - word[i + 1]) > 11 and not fifth_part:
                        phoneme_state = 28
                        fifth_part = True
                    else:
                        phoneme_state += 1
    return result
####################################### task c #######################################
def word_to_phoneme(src_file, target_file):
    word_alignment = open(src_file, 'r')
    phoneme_alignment = open(target_file, 'w')
    all_prefixes = [0,1,13,22,28,37,46,55,67,82,88,97]

    all_words = []
    for line in word_alignment:
        current_word = []
        line_int = np.fromstring(line, dtype=int, sep=' ')
        current_prefix = line_int[0]
        for elem in line_int:
            # new word
            if elem in all_prefixes and current_prefix != elem:
                current_prefix = elem
                # translate current word into corresponding phoneme states
                phonemes = translate_word_to_phoneme(current_word)
                all_words.append(current_word)
                current_word = []
                if phonemes:
                    for phoneme in phonemes:
                        phoneme_alignment.write(str(phoneme) + ' ')

                if elem == 0:
                    phoneme_alignment.write('0 ')
                else:
                    current_word.append(elem)
                    #phoneme_aligntment.write('0 ')
            # write zero to file if we have more than one zero
            elif elem == 0:
                phoneme_alignment.write('0 ')
            # save state for the current word
            else:
                current_word.append(elem)
        phoneme_alignment.write('\n')

    # close files
    word_alignment.close()
    phoneme_alignment.close()

# task c
#word_to_phoneme('alignment.word', 'alignment.phoneme')


####################################### task d #######################################
def write_triphone_models(ordered_triphones):
    output = open('triphone.models', 'w')
    starting_index = 58
    for elem in ordered_triphones:
        tabs = str()
        if len(elem) < 8:
            tabs = '\t\t'
        else:
            tabs = '\t'
        output.write(elem + tabs + str(starting_index) + ' ' + str(starting_index + 1) + ' ' + str(starting_index + 2) + '\n')
        starting_index +=3
    output.close()

def plot_triphone(observations):
    for elem in observations.iteritems():
        print elem[0]
        print elem[1]


def determine_phoneme(state):
    phoneme_prefix    = {0: 'silence', 1: 'ah', 4: 'ax', 7: 'ay', 10: 'f', 13: 'eh', 16: 'ey', 19: 'ih', 22: 'iy',
                         25: 'k', 28: 'n', 31: 'ow', 34: 's', 37: 'r', 40: 't', 43: 'th', 46: 'uw', 49: 'v', 52: 'w',
                         55: 'z'}
    try:
        return phoneme_prefix[state]
    except:
        return None


# each phoneme consits of three different states
def translate_triphone(src_file):
    phoneme_alignment = open(src_file, 'r')
    phoneme_prefix    = {'silence': 0, 'ah': 1, 'ax': 4, 'ay': 7, 'f': 10, 'eh': 13, 'ey': 16, 'ih': 19, 'iy': 22,
                         'k': 25, 'n': 28, 'ow': 31, 's': 34, 'r': 37, 't': 40, 'th': 43, 'uw': 46, 'v': 49, 'w': 52,
                         'z': 55}
    triphones = {}
    for line in phoneme_alignment:
        # convert string to integers
        line_int = np.fromstring(line, dtype=int, sep=' ')

        left_context   = str()
        middle_phoneme = str()
        right_context  = str()

        counter = 0
        for i in range(len(line_int)):
            i = counter
            # prefix of the left context (skip silence state)
            #print i
            if i < len(line_int) and line_int[i] != 0:
                # set left context by
                left_context = determine_phoneme(line_int[i])
                # middle phoneme
                for j in range(i, len(line_int)):
                    if abs(line_int[i] - line_int[j]) > 2 and line_int[j] != 0:
                        middle_phoneme = determine_phoneme(line_int[j])
                        counter = j
                        # right context
                        for k in range(j, len(line_int)):
                            if abs(line_int[j] - line_int[k]) > 2 and line_int[k] != 0:
                                right_context = determine_phoneme(line_int[k])
                                break
                        break
            if None not in (left_context, middle_phoneme, right_context):
                if str(middle_phoneme) + '{' + str(left_context) + ',' + str(right_context) + '}' in triphones:
                    triphones[str(middle_phoneme) + '{' + str(left_context) + ',' + str(right_context) + '}'] += 1
                else:
                    triphones[str(middle_phoneme) + '{' + str(left_context) + ',' + str(right_context) + '}'] = 1
            if counter == i:
                counter += 1
        #break
    #print triphones
    ordered_triphones =  collections.OrderedDict(sorted(triphones.items()))
    # write triphone models
    write_triphone_models(ordered_triphones)
    plot_triphone(ordered_triphones)
    #print ordered_triphones

translate_triphone('alignment.phoneme')
