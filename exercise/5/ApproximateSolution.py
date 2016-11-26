import sys
class StartStopDetection:
    def __init__(self, fileLocation="data/probe1.ascii"):
        self.data = []
        for line in open(fileLocation, 'r'):
            self.data.append(int(line.strip()))

    def calculateLocalCostMatrix(self):
        matrix = [0.] * len(self.data)
        for i in range(0, len(matrix) ):
            matrix[i] = [0.] * len(self.data)

        for i in range(0, len(matrix) ):
            for j in range(i, len(matrix[i]) ):
                energyMean = 0.
                for k in range(i,j+1):
                    energyMean += self.data[k]
                energyMean = energyMean / (j+1-i)

                matrix[i][j] = energyMean
        return matrix

    def calculateScoreOfSegment(self,sumCosts, squareSumCosts, segmentBegin, segmentEnd):
        temp = sumCosts[segmentEnd] - sumCosts[segmentBegin - 1]
        score = squareSumCosts[segmentEnd] - squareSumCosts[segmentBegin - 1]
        score -= self.multiply(temp,temp) / (segmentEnd - segmentBegin + 1)
        return score

    def calculateMeanOfSpeech(self,sumCosts,segmentBegin,segmentEnd):
        return sumCosts[segmentEnd] - sumCosts[segmentBegin - 1]/ (segmentEnd - segmentBegin + 1)


    # solution for d
    def startStopDetectionUsingSums(self):
        self.numberOfCalculations = 0
        K = 3
        T = len(self.data)
        H = [0] * (K + 1)
        B = [0] * (K + 1)
        localCostMatrix = self.calculateLocalCostMatrix()
        for k in range(0, K + 1):
            H[k] = [sys.maxint] * T
            B[k] = [0] * T
        H[0][0] = 0

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

        # print dataSumTable
        # print dataSquareSumTable
        for k in range(1, K + 1):
            for t in range(1, T):
                for t_prime in range(0, t):
                    # Local costs
                    energyAtPoint = (dataSquareSumTable[t] - dataSquareSumTable[t_prime]) - self.multiply(
                        self.multiply(2, localCostMatrix[t_prime + 1][t]),
                        (dataSumTable[t] - dataSumTable[t_prime])) + self.multiply(localCostMatrix[t_prime + 1][t],
                                                                                   self.multiply(
                                                                                       localCostMatrix[t_prime + 1][t],
                                                                                       (t - t_prime)))
                    if H[k][t] >= H[k - 1][t_prime] + energyAtPoint:
                        B[k][t] = t_prime
                        H[k][t] = H[k - 1][t_prime] + energyAtPoint

        print "numberOfCalculations", self.numberOfCalculations
        print "boundaries"
        B1 = B[2][B[3][T - 1]]
        B2 = B[3][T - 1]
        print B1, B2
        print "Mean of the speech: ", (dataSumTable[B2] - dataSumTable[B1]) / (B2 - B1)
        print "Mean of two silence segments: ", (dataSumTable[B1] - dataSumTable[0]) / (B1+1), (dataSumTable[T - 1] - dataSumTable[B2]) / (T - B2)

    # solution for c
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
    print 'Detection of speech using approximation:'
    s.approximateSolution()
    print '----------------------'
    print 'Detection of speech using sums:'
    s.startStopDetectionUsingSums()
