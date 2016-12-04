import sys
import math
class StartStopDetection:
    def __init__(self,fileLocation="data/probe1.ascii"):
        self.data = []
        for line in open(fileLocation,'r'):
            self.data.append( int(line.strip()) )
    
        self.backTrack = [0] * 3
        for k in range(0, len(self.backTrack) ):
            self.backTrack[k] = [0] * len(self.data)
       
       
    def printMatrix(self,m):
        for i in range(0, len(m)):
            for j in range(0, len(m[i])):
                print m[i][j],
            print "\n"
        
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
                energyVar = 0.0000001
                for k in range(i,j+1):
                    energyVar += (self.data[k] - energyMean) ** 2
                value = (j+1-i) / 2
                value = value * (math.log(energyVar/(j+1-i)) + math.log(2 * math.pi) + 1)

                matrix[i][j] = value

        return matrix

        
    def recursiveSearch(self, localCostMatrix, k, t):
        if k >= t:
            return 9999999999
        #print "debug",k,t
        if k == 0:
            return 0

        boundaryValues = []
        for t_prime in range(1, t):
            energyAtPoint = 0
            for i in range(t_prime+1,t+1):
                energyAtPoint += pow(self.data[i] - localCostMatrix[t_prime+1][t], 2)
            #energyAtPoint = energyAtPoint / (t+1-t_prime)
            boundaryValues.append( self.recursiveSearch(localCostMatrix, k-1, t_prime) + energyAtPoint )
        
        minValue = 123456789
        #print boundaryValues, len(boundaryValues),k,t
        for t_prime in range(1, t):
            #print t_prime
            if minValue > boundaryValues[t_prime-1]:
                minValue = boundaryValues[t_prime-1]
                self.backTrack[k-1][t] = t_prime-1

        #print minValue + energyAtPoint
        return minValue + energyAtPoint
        
    def retardedNonDynamicSearch(self,costMatrix):  
        minCosts = 123421134
        boundary1 = 0
        boundary2 = 0
        for i in range(0, len(costMatrix)):
            for j in range(i+1, len(costMatrix[i])):
                tempCosts = costMatrix[0][i] + costMatrix[i][j] + costMatrix[j][len(costMatrix)-1]
                if tempCosts < minCosts:
                    print i,j
                    boundary1 = i
                    boundary2 = j
                    minCosts = tempCosts

        print "boundaries", boundary1, boundary2

    def dynamicProgramming(self):
        self.numberOfCalculations = 0
        K = 3
        T = len(self.data) 
        H = [0] * (K+1)
        B = [0] * (K+1)
        localCostMatrix = self.calculateLocalCostMatrix()
        for k in range(0,K+1):
            H[k] = [sys.maxint] * T
            B[k] = [0] * T

        H[0][0] = 0
        for k in range(1,K+1):
            for t in range(1,T):
                for t_prime in range(0,t):
                    # Local costs
                    energyAtPoint = 0
                    for i in range(t_prime+1, t+1):
                        energyAtPoint += self.multiply( self.data[i]-localCostMatrix[t_prime+1][t], self.data[i]-localCostMatrix[t_prime+1][t] )

                    if H[k][t] >= H[k-1][t_prime] + energyAtPoint:
                        B[k][t] = t_prime 
                        H[k][t] = H[k-1][t_prime] + energyAtPoint

        print "numberOfCalculations", self.numberOfCalculations
        print "boundaries"
        print B[3][T-1], B[2][ B[3][T-1] ]

        
    def dynamicProgrammingWithRunningSums(self):
        self.numberOfCalculations = 0
        K = 3
        T = len(self.data) 
        H = [0] * (K+1)
        B = [0] * (K+1)
        localCostMatrix = self.calculateLocalCostMatrix()
        for k in range(0,K+1):
            H[k] = [sys.maxint] * T
            B[k] = [0] * T
        H[0][0] = 0

        # Precompute values
        dataSumTable = [0] * T
        dataSquareSumTable = [0] * T
        currentDataSum = 0
        currentSquareDataSum = 0
        for i in range(0,len(dataSquareSumTable) ):
            currentDataSum += self.data[i]
            currentSquareDataSum += self.multiply(self.data[i], self.data[i])
            dataSumTable[i] = currentDataSum
            dataSquareSumTable[i] = currentSquareDataSum

        #print dataSumTable
        #print dataSquareSumTable    
        for k in range(1,K+1):
            for t in range(1,T):
                for t_prime in range(0,t):
                    # Local costs
                    energyAtPoint = (dataSquareSumTable[t] - dataSquareSumTable[t_prime]) - self.multiply( self.multiply(2,localCostMatrix[t_prime+1][t]) , (dataSumTable[t] - dataSumTable[t_prime]) ) + self.multiply( localCostMatrix[t_prime+1][t] , self.multiply(localCostMatrix[t_prime+1][t] , (t - t_prime) )) 
                    if H[k][t] >= H[k-1][t_prime] + energyAtPoint:
                        B[k][t] = t_prime 
                        H[k][t] = H[k-1][t_prime] + energyAtPoint
            
        print "numberOfCalculations", self.numberOfCalculations
        print "boundaries"
        print B[3][T-1], B[2][ B[3][T-1] ]

    def multiply(self,x,y):
        self.numberOfCalculations += 1
        return x * y

if __name__ == "__main__":
    fileLocation = "data/probe1.ascii"
    if (len(sys.argv) == 2):
        fileLocation = sys.argv[1]
    s = StartStopDetection(fileLocation)
    s.dynamicProgramming()
    s.dynamicProgrammingWithRunningSums()







