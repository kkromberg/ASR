import copy
from Vocabulary import Vocabulary
from LexicalTree import PrefixTreeNode
import operator
from Queue import Queue
from lxml import etree
import string
#logging.basicConfig(level=logging.DEBUG)

vocabulary = Vocabulary()
prefixTreeRoot = PrefixTreeNode()
tree = etree.parse("lexicon.xml")
root = tree.getroot()
lemmaList = root.findall(".//lemma")

numWords = 1
numPhonemes = 1
numWordsWith2Phonemes, numWordsWith3Phonemes = 0, 0

#adding silence phoneme:

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

print "Number of words in the lexicon: ", prefixTreeRoot.count
print "Number of phonemes in the lexicon: ", numPhonemes

# breadth first search to get n-gram counts
queue = Queue()
phonemeIDQueue = Queue()

queue.put(prefixTreeRoot)
phonemeIDQueue.put([])
n = 3
arcsNum = [0] * 16

while not queue.empty():
    nextNode = queue.get()
    nextNPhoneme = phonemeIDQueue.get()

    # Fill the queue
    for childPhonemeID, childNode in nextNode.getChildren().items():
        #arcsNum2 += 1
        childNGram = copy.copy(nextNPhoneme)
        childNGram.append(childPhonemeID)

        queue.put(childNode)
        phonemeIDQueue.put(childNGram)
    #for i in range (0,len(nextNPhoneme)):
        arcsNum[len(nextNPhoneme)] += 1

#compFactor, compFactor2, compFactor3 = 0.0, 0.0, 0.0
compFactor2 = (numWordsWith2Phonemes * 2 + 0.0) / sum(arcsNum[:2])
compFactor3 = (numWordsWith3Phonemes * 3 + 0.0) / sum(arcsNum[:3])
compFactor = (numPhonemes + 0.0) / sum(arcsNum)
print  sum(arcsNum)
print "Compression factor for the whole tree: ", compFactor
print "Compression factor for the first two phoneme generations : ", compFactor2
print "Compression factor for the first three phoneme generations: ", compFactor3
