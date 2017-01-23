from lxml import etree
class TriphoneVocabulary:
    def __init__(self):
        self.phoneme2int = {}
        self.int2phoneme = {}
        self.nextID = -1
        # Initialize the vocabulary mappings
        tree = etree.parse("lexicon.xml")
        root = tree.getroot()
        phonemeList = root.findall(".//phoneme")
        for phLeft in phonemeList:
            for phMiddle in phonemeList:
                for phRight in phonemeList:
                    #print ph.find('symbol').text
                    self.addSymbol(phLeft.find('symbol').text + phMiddle.find('symbol').text +
                                   phRight.find('symbol').text)
                self.addSymbol('#' + phMiddle.find('symbol').text +
                                phLeft.find('symbol').text)
                self.addSymbol(phLeft.find('symbol').text + phMiddle.find('symbol').text +
                                '#')
            self.addSymbol('#' + phLeft.find('symbol').text + '#')
    def size(self):
        return self.nextID + 1
    def addSymbol(self, triphone):
        if triphone not in self.phoneme2int:
            self.nextID += 1
            self.phoneme2int[triphone] = self.nextID
            self.int2phoneme[self.nextID] = triphone
        return self.phoneme2int[triphone]
    def symbol(self, ID):
            return self.int2phoneme[ID]
    def index(self, word):
            return self.phoneme2int[word]
#voc = TriphoneVocabulary()
#print voc.size()