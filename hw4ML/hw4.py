import math

#conver the string of number separated by commas into an array of number 
def converstringtoint (stringofnum):
    result = []
    temp = ''
    for i in range(len(stringofnum)):
        if (stringofnum[i] == ',' or stringofnum[i] == '\n'):
            result.append(int(temp))
            temp = ''
        else:
            temp += stringofnum[i]
   
    return result

trainingData = open("optdigits.train",'r')                    #this is our traning data
arrayofnumberofeachdigits = [0,0,0,0,0,0,0,0,0,0]             #number of each digit in the training data
arrayofnumberofprobmodel = [[],[],[],[],[],[],[],[],[],[]]    #number of learning model

#initialize the number of learning model to zero
for i in range(10):
    for j in range(64):
        arrayofnumberofprobmodel[i].append([])
        for k in range(17):
            arrayofnumberofprobmodel[i][j].append(0)

#calculating the number of learning model
for line in trainingData:
    temparray = converstringtoint(line)
    arrayofnumberofeachdigits[temparray[-1]] += 1
    for i in range(64):
        arrayofnumberofprobmodel[temparray[-1]][i][temparray[i]] += 1

totalNumberoftraining = sum(arrayofnumberofeachdigits)       #number of tranining set            
arrayofProbofeachdigits = []                                 #probability of each digit in training set   
arrayofProbofprobmodel = [[],[],[],[],[],[],[],[],[],[]]     #probabilistic model

#calculating probability of each digit
for i in range(10):
    arrayofProbofeachdigits.append(float(arrayofnumberofeachdigits[i])/totalNumberoftraining)

#calculating probabilistic model
for i in range(10):
    for j in range(64):
        arrayofProbofprobmodel[i].append([])
        for k in range(17):
            arrayofProbofprobmodel[i][j].append((float(arrayofnumberofprobmodel[i][j][k])+1)/(arrayofnumberofeachdigits[i]+17))


testdata = open("optdigits.test",'r')        #this is our test data
confusionmatrix = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]] #confusion matrix
numberoftestdata = 0

#calculating the accuracy and confusion matrix
for line in testdata:
    numberoftestdata += 1
    temparray = converstringtoint(line)
    argmaxnumber = -9999999999999
    predictclass = 0
    for i in range(10):
        tempnumber = (math.log10(arrayofProbofeachdigits[i]))
        for j in range(64):
            tempnumber = tempnumber + math.log10(arrayofProbofprobmodel[i][j][temparray[j]])
        if(tempnumber>argmaxnumber):
            argmaxnumber = tempnumber
            predictclass = i
    confusionmatrix[predictclass][temparray[-1]] += 1
accuracy = float(confusionmatrix[0][0]+confusionmatrix[1][1]+confusionmatrix[2][2]+confusionmatrix[3][3]+confusionmatrix[4][4]+confusionmatrix[5][5]+confusionmatrix[6][6]+confusionmatrix[7][7]+confusionmatrix[8][8]+confusionmatrix[9][9])/numberoftestdata

#print out the accuracy and confusion matrix
print "The Confusion Matrix:"
print " |0 1 2 3 4 5 6 7 8 9"
print "-|- - - - - - - - - -"
for i in range(10):
    print str(i) + "|" + str(confusionmatrix[0][i]) + " " + str(confusionmatrix[1][i]) + " " + str(confusionmatrix[2][i]) + " "+ str(confusionmatrix[3][i]) + " "+ str(confusionmatrix[4][i]) + " "+ str(confusionmatrix[5][i]) + " "+ str(confusionmatrix[6][i]) + " "+ str(confusionmatrix[7][i]) + " "+ str(confusionmatrix[8][i]) + " "+ str(confusionmatrix[9][i])
print "\nThe accuracy on the test set: " + str(accuracy)

print arrayofnumberofprobmodel
