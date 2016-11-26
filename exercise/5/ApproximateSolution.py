import sys
class StartStopDetection:
    def __init__(self, fileLocation="data/probe1.ascii"):
        self.data = []
        for line in open(fileLocation, 'r'):
            self.data.append(int(line.strip()))

    def calculateScoreOfSegment(self,sumCosts, squareSumCosts, segmentBegin, segmentEnd):
        temp = sumCosts[segmentEnd] - sumCosts[segmentBegin - 1]
        score = squareSumCosts[segmentEnd] - squareSumCosts[segmentBegin - 1]
        score -= self.multiply(temp,temp) / (segmentEnd - segmentBegin + 1)
        return score

    def calculateMeanOfSpeech(self,sumCosts,segmentBegin,segmentEnd):
        return sumCosts[segmentEnd] - sumCosts[segmentBegin - 1]/ (segmentEnd - segmentBegin + 1)

    def approximateSolution(self):
        self.numberOfCalculations = 0
        T = len(self.data)
        # Precompute values
        dataSumTable = [0] * T
        dataSquareSumTable = [0] * T
        currentDataSum = 0
        currentSquareDataSum = 0
        for i in range(0, len(dataSquareSumTable)):
            currentDataSum += self.data[i]
            currentSquareDataSum += self.multiply(self.data[i], self.data[i])
            dataSumTable[i] = currentDataSum
            dataSquareSumTable[i] = currentSquareDataSum

        #uniformboundaryinitialization
        B1 = T / 2 - 1
        B2 = T / 2
        numberOfIterations = 3
        for i in range(0, numberOfIterations):
            #Optimize first boundary
            bestCosts = 123421134
            newBoundary = B1
            for t in range(1, B2-1):
                newCosts = self.calculateScoreOfSegment(dataSumTable, dataSquareSumTable, 1, t) + self.calculateScoreOfSegment(dataSumTable, dataSquareSumTable, t+1, B2);

                if (newCosts < bestCosts):
                    newBoundary = t
                    bestCosts   = newCosts


            B1 = newBoundary
            #Optimize secondary boundary
            bestCosts = 123421134
            newBoundary = B2
            for t in range(B1+1, T-1):
                newCosts = self.calculateScoreOfSegment(dataSumTable, dataSquareSumTable, B1+1, t) + self.calculateScoreOfSegment(dataSumTable, dataSquareSumTable, t+1, T-1);

                if (newCosts < bestCosts):
                    newBoundary = t
                    bestCosts   = newCosts
            B2 = newBoundary
        print "numberOfCalculations", self.numberOfCalculations
        print "boundaries:"
        print B1, B2
        print "Mean of the speech: ", (dataSumTable[B2] - dataSumTable[B1]) / (B2 - B1)
        print "Mean of two silence segments: ", (dataSumTable[B1] - dataSumTable[0]) / (B1+1), (dataSumTable[T - 1] - dataSumTable[B2]) / (T - B2)
    def multiply(self, x, y):
        self.numberOfCalculations += 1
        return x * y

if __name__ == "__main__":
    fileLocation = "data/probe1.ascii"
    if (len(sys.argv) == 2):
        fileLocation = sys.argv[1]
    s = StartStopDetection(fileLocation)
    s.approximateSolution()
