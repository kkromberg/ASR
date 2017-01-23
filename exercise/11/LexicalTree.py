import sys
sys.setrecursionlimit(1000)
class PrefixTreeNode:
    def __init__(self):
        self.children = None
        self.count = 0

    def recursiveAddWord(self, word):
        # nGram: vector of word IDs (integers)
        self.count += 1

        if len(word) == 0:
            return

        if self.children == None:
            self.children = {}

        # len(word) != 0
        nextPhonemeID = word[0]
        if nextPhonemeID not in self.children:
            self.children[nextPhonemeID] = PrefixTreeNode()

        # Connection to the next node already exists
        childNode = self.children[nextPhonemeID]
        childNode.recursiveAddWord(word[1:])

    def getNPhonemeCount(self, nPhoneme):
        # nPhoneme: vector of phoneme IDs (integers)

        if len(nPhoneme) == 0:
            return self.count

        if self.children == None:
            self.children = {}

            nextPhonemeID = nPhoneme[0]
        if nextPhonemeID not in self.children:
            return 0

        # Connection to the next node already exists
        childNode = self.children[nextPhonemeID]
        return childNode.getNPhonemeCount(nPhoneme[1:])

    def getNPhonemeNode(self, nPhoneme):
        if len(nPhoneme) == 0:
            return self

        if self.children == None:
            self.children = {}

            nextPhonemeID = nPhoneme[0]
        if nextPhonemeID not in self.children:
            return None

        # Connection to the next node already exists
        childNode = self.children[nextPhonemeID]
        return childNode.getNPhonemeNode(nPhoneme[1:])

    def subtreeSize(self):
        if self.children != None:
            return 1 + sum([child.subtreeSize() for id, child in self.children.items()])
        else:
            return 1

    def getChildren(self):
        if self.children != None:
            return self.children
        else:
            return {}

    def getNumberOfChildren(self):
        if self.children != None:
            return len(self.children)
        else:
            return 0
