import copy
from Vocabulary import Vocabulary
from TriphoneVocabulary import TriphoneVocabulary
from CartVocabulary import CartVocabulary
from CartStateVocabulary import CartStateVocabulary
from LexicalTree import PrefixTreeNode
import operator
from Queue import Queue
from lxml import etree
import string
#logging.basicConfig(level=logging.DEBUG)

def parseTree (prefixTreeRoot):
    # breadth first search
    queue = Queue()
    phonemeIDQueue = Queue()

    queue.put(prefixTreeRoot)
    phonemeIDQueue.put([])
    arcsNum = [0] * 16 *3

    while not queue.empty():
        nextNode = queue.get()
        nextNPhoneme = phonemeIDQueue.get()

        # Fill the queue
        for childPhonemeID, childNode in nextNode.getChildren().items():
            # arcsNum2 += 1
            childNGram = copy.copy(nextNPhoneme)
            childNGram.append(childPhonemeID)

            queue.put(childNode)
            phonemeIDQueue.put(childNGram)
            # for i in range (0,len(nextNPhoneme)):
            arcsNum[len(nextNPhoneme)] += 1
    return arcsNum

vocabulary = Vocabulary()
vocabularyTriphones = TriphoneVocabulary()
vocabularyCartPhones = CartVocabulary()
vocabularyCartStatePhones = CartStateVocabulary()
prefixTreeRoot = PrefixTreeNode()
prefixTreeRootTriphones = PrefixTreeNode()
prefixTreeRootCartPhones = PrefixTreeNode()
prefixTreeRootCartStatePhones = PrefixTreeNode()
tree = etree.parse("lexicon.xml")
root = tree.getroot()
lemmaList = root.findall(".//lemma")

numWords = 1
numPhonemes = 1
numWordsWith2Phonemes, numWordsWith3Phonemes = 0, 0

#adding silence word:
prefixTreeRoot.recursiveAddWord([vocabulary.index(lemmaList[0].find('phon').text)])

#generating lexical prefix tree
for word in lemmaList[4:]:
    currentPhonemeIDs = []
    numWords += 1
    #print word.find('phon').text
    currentStringPhonemes = word.find('phon').text.strip().split(' ')
    for phoneme_idx in range(0, len(currentStringPhonemes)):
        numPhonemes += 1
        #print currentStringPhonemes[phoneme_idx]
        #print vocabulary.index(currentStringPhonemes[phoneme_idx])
        currentPhonemeID = vocabulary.index(currentStringPhonemes[phoneme_idx])
        currentPhonemeIDs.append(currentPhonemeID)
    #print currentPhonemeIDs
    if len(currentStringPhonemes) == 2:
        numWordsWith2Phonemes += 1
    if len(currentStringPhonemes) == 3:
        numWordsWith3Phonemes += 1
    prefixTreeRoot.recursiveAddWord(currentPhonemeIDs)

#adding silence word:
prefixTreeRootTriphones.recursiveAddWord([vocabularyTriphones.index('#' + lemmaList[0].find('phon').text + '#')] )
prefixTreeRootCartPhones.recursiveAddWord([vocabularyCartPhones.index('#' + lemmaList[0].find('phon').text + '#')])
prefixTreeRootCartStatePhones.recursiveAddWord([vocabularyCartStatePhones.index('#' + lemmaList[0].find('phon').text + '#' + '0')])
numTriphones = 0
#generating lexical prefix tree with triphones
for word in lemmaList[4:]:
    currentTriphoneIDs = []
    currentCartPhoneIDs = []
    currentCartStatePhoneIDs = []
    numWords += 1
    #print word.find('phon').text
    currentStringTriphones = ['#']
    currentStringTriphones += word.find('phon').text.strip().split(' ')
    currentStringTriphones.append('#')
    #print currentStringTriphones
    for phoneme_idx in range(1, len(currentStringTriphones) - 1):
        numTriphones += 1
        #print currentStringPhonemes[phoneme_idx]
        #print vocabulary.index(currentStringPhonemes[phoneme_idx])
        currentTriphoneID = vocabularyTriphones.index(currentStringTriphones[phoneme_idx - 1] +
                                                      currentStringTriphones[phoneme_idx] +
                                                      currentStringTriphones[phoneme_idx + 1])
        currentCartPhoneID = vocabularyCartPhones.index(currentStringTriphones[phoneme_idx - 1] +
                                                      currentStringTriphones[phoneme_idx] +
                                                      currentStringTriphones[phoneme_idx + 1])
        currentCartStatePhoneID0 = vocabularyCartStatePhones.index(currentStringTriphones[phoneme_idx - 1] +
                                                      currentStringTriphones[phoneme_idx] +
                                                      currentStringTriphones[phoneme_idx + 1] + '0')
        currentCartStatePhoneID1 = vocabularyCartStatePhones.index(currentStringTriphones[phoneme_idx - 1] +
                                                                   currentStringTriphones[phoneme_idx] +
                                                                   currentStringTriphones[phoneme_idx + 1] + '1')
        currentCartStatePhoneID2 = vocabularyCartStatePhones.index(currentStringTriphones[phoneme_idx - 1] +
                                                                   currentStringTriphones[phoneme_idx] +
                                                                   currentStringTriphones[phoneme_idx + 1] + '2')
        currentTriphoneIDs.append(currentTriphoneID)
        currentCartPhoneIDs.append(currentCartPhoneID)
        currentCartStatePhoneIDs.append(currentCartStatePhoneID0)
        currentCartStatePhoneIDs.append(currentCartStatePhoneID1)
        currentCartStatePhoneIDs.append(currentCartStatePhoneID2)
    prefixTreeRootTriphones.recursiveAddWord(currentTriphoneIDs)
    prefixTreeRootCartPhones.recursiveAddWord(currentCartPhoneIDs)
    prefixTreeRootCartStatePhones.recursiveAddWord(currentCartStatePhoneIDs)


print "Number of words in the lexicon: ", prefixTreeRoot.count
print "Number of phonemes in the lexicon: ", numPhonemes




compFactor2 = (numWordsWith2Phonemes * 2 + 0.0) / sum(parseTree(prefixTreeRoot)[:2])
compFactor3 = (numWordsWith3Phonemes * 3 + 0.0) / sum(parseTree(prefixTreeRoot)[:3])
compFactor = (numPhonemes + 0.0) / sum(parseTree(prefixTreeRoot))


compFactorTriphone2 = (numWordsWith2Phonemes * 2 + 0.0) / sum(parseTree(prefixTreeRootTriphones)[:2])
compFactorTriphone3 = (numWordsWith3Phonemes * 3 + 0.0) / sum(parseTree(prefixTreeRootTriphones)[:3])
compFactorTriphone = (numPhonemes + 0.0) / sum(parseTree(prefixTreeRootTriphones))

compFactorCartPhone2 = (numWordsWith2Phonemes * 2 + 0.0) / sum(parseTree(prefixTreeRootCartPhones)[:2])
compFactorCartPhone3 = (numWordsWith3Phonemes * 3 + 0.0) / sum(parseTree(prefixTreeRootCartPhones)[:3])
compFactorCartPhone = (numPhonemes + 0.0) / sum(parseTree(prefixTreeRootCartPhones))

compFactorCartStatePhone2 = (numWordsWith2Phonemes * 2 * 3 + 0.0) / sum(parseTree(prefixTreeRootCartStatePhones)[:2])
compFactorCartStatePhone3 = (numWordsWith3Phonemes * 3 * 3 + 0.0) / sum(parseTree(prefixTreeRootCartStatePhones)[:3])
compFactorCartStatePhone = (numPhonemes * 3 + 0.0) / sum(parseTree(prefixTreeRootCartStatePhones))

print "Results for monophones:"
print "Compression factor for the whole tree: ", compFactor
print "Compression factor for the first two phoneme generations : ", compFactor2
print "Compression factor for the first three phoneme generations: ", compFactor3

print "Results for triphones:"
print "Compression factor for the whole tree: ", compFactorTriphone
print "Compression factor for the first two phoneme generations : ", compFactorTriphone2
print "Compression factor for the first three phoneme generations: ", compFactorTriphone3

print "Results for cartphones:"
print "Compression factor for the whole tree: ", compFactorCartPhone
print "Compression factor for the first two phoneme generations : ", compFactorCartPhone2
print "Compression factor for the first three phoneme generations: ", compFactorCartPhone3

print "Results for cartStatePhones:"
print "Compression factor for the whole tree: ", compFactorCartStatePhone
print "Compression factor for the first two phoneme generations : ", compFactorCartStatePhone2
print "Compression factor for the first three phoneme generations: ", compFactorCartStatePhone3