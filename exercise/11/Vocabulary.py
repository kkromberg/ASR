from lxml import etree
class Vocabulary:
    def __init__(self):
        self.phoneme2int = {}
        self.int2phoneme = {}
        self.nextID = -1
        # Initialize the vocabulary mappings
        tree = etree.parse("lexicon.xml")
        root = tree.getroot()
        phonemeList = root.findall(".//phoneme")
        for ph in phonemeList:
            #print ph.find('symbol').text
            self.addSymbol(ph.find('symbol').text)
    def size(self):
        return self.nextID + 1
    def addSymbol(self, phoneme):
        if phoneme not in self.phoneme2int:
            self.nextID += 1
            self.phoneme2int[phoneme] = self.nextID
            self.int2phoneme[self.nextID] = phoneme
        return self.phoneme2int[phoneme]
    def symbol(self, ID):
        if ID not in self.int2phoneme:
            return self.unknownWordString()
        else:
            return self.int2phoneme[ID]
    def index(self, word):
        if word not in self.phoneme2int:
            return self.unknownWordID()
        else:
            return self.phoneme2int[word]
#voc = Vocabulary()
#print voc.int2phoneme[20]
#print voc.size()
