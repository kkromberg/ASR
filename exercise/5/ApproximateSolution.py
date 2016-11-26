import sys
class SpeechDetection:
    def __init__(self, fileLocation="data/probe1.ascii"):
        self.data = []
        for line in open(fileLocation, 'r'):
            self.data.append(int(line.strip()))

    def calculateScoreOfSegment(self,sumCosts, squareSumCosts, segmentBegin, segmentEnd):
        temp = sumCosts[segmentEnd] - sumCosts[segmentBegin - 1]
        score = squareSumCosts[segmentEnd] - squareSumCosts[segmentBegin - 1]
        score -= self.multiply(temp,temp) / (segmentEnd - segmentBegin + 1)
        return score

    def approximateSolution(self):
        self.numberOfCalculations = 0
        T = len(self.data)
        # Precompute values
        sumCosts = [0] * T
        squareSumCosts = [0] * T
        currentSum = 0
        currentSquareSum = 0
        for i in range(0, len(squareSumCosts)):
            currentSum += self.data[i]
            currentSquareSum += self.multiply(self.data[i], self.data[i])
            sumCosts[i] = currentSum
            squareSumCosts[i] = currentSquareSum

        #uniform boundary initialization
        B1 = T / 2 - 1
        B2 = T / 2
        numberOfIterations = 3
        for i in range(0, numberOfIterations):
            #Optimize first boundary
            bestCosts = 123421134
            newBoundary = B1
            for t in range(1, B2-1):
                newCosts = self.calculateScoreOfSegment(sumCosts, squareSumCosts, 1, t) + self.calculateScoreOfSegment(sumCosts, squareSumCosts, t+1, B2);

                if (newCosts < bestCosts):
                    newBoundary = t
                    bestCosts   = newCosts

            B1 = newBoundary
            #Optimize secondary boundary
            bestCosts = 123421134
            newBoundary = B2
            for t in range(B1+1, T-1):
                newCosts = self.calculateScoreOfSegment(sumCosts, squareSumCosts, B1+1, t) + self.calculateScoreOfSegment(sumCosts, squareSumCosts, t+1, T-1);

                if (newCosts < bestCosts):
                    newBoundary = t
                    bestCosts   = newCosts
            B2 = newBoundary
        print "numberOfCalculations", self.numberOfCalculations
        print "boundaries:"
        print B1, B2
        print "Mean of the speech: ", (sumCosts[B2] - sumCosts[B1]) / (B2 - B1)
        print "Mean of two silence segments: ", (sumCosts[B1] - sumCosts[0]) / (B1+1), (sumCosts[T - 1] - sumCosts[B2]) / (T - B2)
    def multiply(self, x, y):
        self.numberOfCalculations += 1
        return x * y

if __name__ == "__main__":
    fileLocation = "data/probe1.ascii"
    if (len(sys.argv) == 2):
        fileLocation = sys.argv[1]
    s = SpeechDetection(fileLocation)
    s.approximateSolution()
