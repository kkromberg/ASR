class CartStateVocabulary:
    def __init__(self):
        self.phoneme2int = {}
        self.int2phoneme = {}
        # Initialize the vocabulary mappings
        cart = open('cart.state', 'r')
        for line in cart:
            leftPhoneme = line.split('{')[1].split('+')[0]
            middlePhoneme = line.split('{')[0]
            rightPhoneme =  line.split('{')[1].split('+')[1].split('}')[0]
            stateIdx = line.split('{')[1].split('+')[1].split('}')[1][1:2]
            clusterIdx = int(line.split('{')[1].split('+')[1].split('}')[1][3:])
            self.addSymbol(leftPhoneme + middlePhoneme + rightPhoneme + stateIdx, clusterIdx)
            #print leftPhoneme + middlePhoneme + rightPhoneme + stateIdx, clusterIdx
    def size(self):
        return self.nextID + 1
    def addSymbol(self, triphone, clusterIdx):
        if triphone not in self.phoneme2int:
            self.phoneme2int[triphone] = clusterIdx
            self.int2phoneme[clusterIdx] = triphone
        return self.phoneme2int[triphone]
    def symbol(self, ID):
            return self.int2phoneme[ID]
    def index(self, word):
            return self.phoneme2int[word]