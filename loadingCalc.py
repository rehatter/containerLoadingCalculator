from math import floor

'''  _________
    /         /
 L /         / 
  /         / 
 /________ /
 |        |
 |        | H
 |        |
 |        |
  ________
     W


    Algorithm Description
    Step 1
    Generate all possible ways to put the given box along the W side of the container.
    I.E. - Supposing we have a box with sides S1, S2, S3; we may place this box in the container
    in the following ways: Keeping only one side of the box along width, keeping a mix of two sides, or keeping all three sides.
    For example, We could do something like: S1S1S1S1, S1S1S2S2, S1S2S3 moreover, we can do all combinations of this.
    

'''

class genericContainer(object):
    def __init__(self):
        self.loadingConfigurationsWidth = {}
        self.loadingConfigurationsHigh = []
        self.lowestWasteConfig = []
        self.totalQuantity = 0
        self.Wid = 0
        self.Len = 0
        self.Hig = 0
        

    def generateWidthCombos(self, boxWid, boxLen, boxHig):
        
        maxBoxLen = floor(self.Wid / boxLen) # Used to generate maximum number of boxes which can be loaded when they are put among any given orientation
        maxBoxWid = floor(self.Wid / boxWid)
        maxBoxHig = floor(self.Wid / boxHig)

        for i in range(maxBoxLen + 1):
            balanceSpace = self.Wid - (i * boxLen)
            numWidth = floor(balanceSpace / boxWid)
            loadingString = 'L' * i + 'W' * numWidth
            wastedSpace = self.Wid - (i * boxLen) - (numWidth * boxWid)
            self.loadingConfigurationsWidth[loadingString] = wastedSpace

        for i in range(maxBoxWid + 1):
            balanceSpace = self.Wid - (i * boxWid)
            numHigh = floor(balanceSpace / boxHig)
            loadingString = 'W' * i + 'H' * numHigh
            wastedSpace = self.Wid - (i * boxWid) - (numHigh * boxHig)
            self.loadingConfigurationsWidth[loadingString] = wastedSpace
        
        for i in range(maxBoxLen + 1):
            balanceSpace = self.Wid - (i * boxLen)
            numHigh = floor(balanceSpace / boxHig)
            loadingString = 'L' * i + 'H' * numHigh
            wastedSpace = self.Wid - (i * boxLen) - (numHigh * boxHig)
            self.loadingConfigurationsWidth[loadingString] = wastedSpace

        # Length, Width and Height
        for i in range(1, maxBoxLen + 1):
            for j in range(1, maxBoxWid + 1):
                balanceSpace = self.Wid - (i * boxLen) - (j * boxWid)
                if (balanceSpace < 0):
                    continue
                numHigh = floor(balanceSpace / boxHig)
                wastedSpace = self.Wid - (i * boxLen) - (j * boxWid) - (numHigh * boxHig)
                loadingString = 'L' * i + 'W' * j + 'H' * numHigh
                self.loadingConfigurationsWidth[loadingString] = wastedSpace
                
        

    def generateHighCombos(self, boxWid, boxLen, boxHig):

        maxBoxLen = floor(self.Hig / boxLen)
        maxBoxWid = floor(self.Hig / boxWid)
        maxBoxHig = floor(self.Hig / boxHig)

        for loadingString in self.loadingConfigurationsWidth:
            loadingConfigsList = []
            loadingWastedSpace = []
            uniqueSidesDone = ''
            for char in loadingString:
                if (char in uniqueSidesDone):
                    continue
                else:
                    uniqueSidesDone += char
                if (char == 'L'):
                    wastedSpace = self.Hig
                    bestString = ''
                    for i in range(maxBoxWid + 1):
                        balanceSpace = self.Hig - (boxWid * i)
                        numHigh = floor(balanceSpace /  boxHig)
                        curSpace = self.Hig - (i * boxWid) - (numHigh * boxHig)
                        loadingString = ('W' * i) + ('H' * numHigh)
                        if (curSpace < wastedSpace):
                            wastedSpace = curSpace
                            bestString = loadingString
                    loadingConfigsList.append(bestString)
                    loadingWastedSpace.append(wastedSpace)

                elif (char == 'W'):
                    wastedSpace = self.Hig
                    bestString = ''
                    for i in range(maxBoxLen + 1):
                        balanceSpace = self.Hig - (boxLen * i)
                        numHigh = floor(balanceSpace /  boxHig)
                        curSpace = self.Hig - (i * boxLen) - (numHigh * boxHig)
                        loadingString = ('L' * i) + ('H' * numHigh)
                        if (curSpace < wastedSpace):
                            wastedSpace = curSpace
                            bestString = loadingString
                    loadingConfigsList.append(bestString)
                    loadingWastedSpace.append(wastedSpace)

                elif (char == 'H'):
                    wastedSpace = self.Hig
                    bestString = ''
                    for i in range(maxBoxLen + 1):
                        balanceSpace = self.Hig - (boxWid * i)
                        numLen = floor(balanceSpace /  boxLen)
                        curSpace = self.Hig - (i * boxWid) - (numLen * boxLen)
                        loadingString = ('W' * i) + ('L' * numLen)
                        if (curSpace < wastedSpace):
                            wastedSpace = curSpace             
                            bestString = loadingString
                    loadingConfigsList.append(bestString)
                    loadingWastedSpace.append(wastedSpace)
                    
            self.loadingConfigurationsHigh.append((loadingConfigsList, loadingWastedSpace))

    def getLowestWastageConfig(self):

        lowestWastageConfig = []
        lowestWastage = 2350 + 2700

        indexForHigh = 0
        for config, wastage in self.loadingConfigurationsWidth.items():
            calculateWastageHigh = lambda wasteList : wasteList[0] if (len(wasteList) == 1) else wasteList[0] + calculateWastageHigh(wasteList[1:])
            thisConfigWaste = wastage + calculateWastageHigh(self.loadingConfigurationsHigh[indexForHigh][1])
            if (thisConfigWaste < lowestWastage):
                self.lowestWasteConfig = [config] + self.loadingConfigurationsHigh[indexForHigh][0]
                lowestWastage = thisConfigWaste
            indexForHigh += 1
        #print(self.lowestWasteConfig)
    def calculateLoadingCapacity(self, boxWid, boxLen, boxHig):       

        previousLetter = self.lowestWasteConfig[0][0]
        index = 1

        for charW in self.lowestWasteConfig[0]:
            
            if (charW == previousLetter):
                previousLetter = charW
            else:
                previousLetter = charW
                index += 1
                
            for charH in self.lowestWasteConfig[index]:
                if (charW == 'L'):
                    if (charH == 'H'):
                        self.totalQuantity += floor(self.Len / boxWid)
                    elif(charH == 'W'):
                        self.totalQuantity += floor(self.Len / boxHig)
                elif(charW == 'W'):
                    if (charH == 'H'):
                        self.totalQuantity += floor(self.Len / boxLen)
                    elif(charH == 'L'):
                        self.totalQuantity += floor(self.Len / boxHig)
                elif(charW == 'H'):
                    if (charH == 'L'):
                        self.totalQuantity += floor(self.Len / boxWid)
                    elif(charH == 'W'):
                        self.totalQuantity += floor(self.Len / boxLen)
                        
    def executeCalculations(self, boxWid, boxLen, boxHig):
        self.generateWidthCombos(boxWid, boxLen, boxHig)
        self.generateHighCombos(boxWid, boxLen, boxHig)
        self.getLowestWastageConfig()
        self.calculateLoadingCapacity(boxWid, boxLen, boxHig)
        print("Total loadable quantity is: {}".format(self.totalQuantity))
        print("Loading schematic depicted below: ")

    def displayResults(self):

        def multiplesLens(string):
            multiples = []
            previousLetter = string[0]
            count = 0
            for char in string:
                if (char != previousLetter):
                    multiples.append(count)
                    count = 1
                    previousLetter = char
                else:
                    count += 1
                    previousLetter = char

            multiples.append(count)

            for multiple in range(len(multiples)):
                multiples[multiple] -= 1

            return multiples

        def transposeAndSpaceString(thisIndex, string):
            stringRows = []
            for char in string:
                stringRows.append(char + ' ' * thisIndex)
            return stringRows
        
        def doAllStrings(indices, strings):
            allRows = []
            for string in range(len(strings)):
                thisString = transposeAndSpaceString(indices[string], strings[string])
                allRows.append(thisString)
            #print(allRows)
            return allRows

        def longestSublist(listOfLists):
            longest = 0
            for item in listOfLists:
                if (len(item) > longest):
                    longest = len(item)
            return longest


    
        indices = multiplesLens(self.lowestWasteConfig[0])
        rows = doAllStrings(indices, self.lowestWasteConfig[1:])
        tallest = longestSublist(rows)

        for item in rows:
            while (len(item) < tallest):
                item.append(' ')


        totalLength = len(rows[0])
        final = []
        for item in range(totalLength):
            i = 0
            newString = ''
            while (i < len(rows)):
                newString += rows[i][item]
                i += 1
            final.append(newString)

        actualEnd = ''
        for item in final:
            actualEnd += item
            actualEnd += '\n'

        actualEnd += self.lowestWasteConfig[0]
        print (actualEnd)
                  
class fortyFootHighCube(genericContainer):
    def __init__(self):
        super().__init__()
        self.Wid = 2350
        self.Len = 12032
        self.Hig = 2700

class fortyFootDry(genericContainer):
    def __init__(self):
        super().__init__()
        self.Wid = 2340
        self.Len = 12032
        self.Hig = 2380

class twentyFootDry(genericContainer):
    def __init__(self):
        super().__init__()
        self.Wid = 2340
        self.Len = 5850
        self.Hig = 2380

if __name__ == "__main__":
    containerType = input("Please enter the type of container, either 40HC, 40 or 20: ")
    boxSizes = input("Please enter the box sizes (in mm) in L x W x H (just type the numbers separated by a space): ")
    boxSizes = [int(s) for s in boxSizes.split() if s.isdigit()]
    if (containerType == '40HC'):
        y = fortyFootHighCube()
        y.executeCalculations(boxSizes[1], boxSizes[0], boxSizes[2])
       # print(y.lowestWasteConfig)
        y.displayResults()
    elif(containerType == '40'):
        y = fortyFootDry()
        y.executeCalculations(boxSizes[1], boxSizes[0], boxSizes[2])
        y.displayResults()
    else:
        y = twentyFootDry()
        y.executeCalculations(boxSizes[1], boxSizes[0], boxSizes[2])
        y.displayResults()


    
        

