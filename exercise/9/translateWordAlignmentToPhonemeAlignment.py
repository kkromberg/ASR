import numpy as np
import json
import operator
import matplotlib.pyplot as plt


# plotting for b and c
def plot(num_oberservations):
    separated_tuples = zip(*num_oberservations)
    print separated_tuples
    plt.scatter(*separated_tuples)
    plt.title('Number of observation for each mixture')
    plt.xlabel('Mixture index')
    plt.ylabel('Amount of observations')
    plt.xticks(separated_tuples[0])
    plt.show()

# task b
def num_obersvations_word(src_file):
    word_alignment = open(src_file, 'r')
    all_prefixes = [1, 13, 22, 28, 37, 46, 55, 67, 82, 88, 97]
    num_observations = {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                        7: 0, 8: 0, 9: 0, 10: 0}

    for line in word_alignment:
        line_int = np.fromstring(line, dtype=int, sep=' ')
        current_prefix = line_int[0]
        for elem in line_int:
            if elem in all_prefixes and current_prefix != elem:
                current_prefix = elem
                if elem == 1:
                    num_observations[0] += 1
                elif elem == 13:
                    num_observations[1] += 1
                elif elem == 22:
                    num_observations[2] += 1
                elif elem == 28:
                    num_observations[3] += 1
                elif elem == 37:
                    num_observations[4] += 1
                elif elem == 46:
                    num_observations[5] += 1
                elif elem == 55:
                    num_observations[6] += 1
                elif elem == 67:
                    num_observations[7] += 1
                elif elem == 82:
                    num_observations[8] += 1
                elif elem == 88:
                    num_observations[9] += 1
                elif elem == 97:
                    num_observations[10] += 1
            # count each silence state as word
            elif elem == 0:
                num_observations[-1] += 1
    # close file
    word_alignment.close()
    # write count to file
    num_observations_sorted = sorted(num_observations.items(), key=lambda x: x[1], reverse=True)
    count = open('num_obersvations_per_mixture.word', 'w')
    for elem in num_observations_sorted:
        count.write(str(elem[0]) + ' ' + str(elem[1]) + '\n')

    count.close()
    # plotting
    plot(num_observations_sorted)


num_obersvations_word('alignment.word')
# task c
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
# task c
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
word_to_phoneme('alignment.word', 'alignment.phoneme')
