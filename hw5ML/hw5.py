import math
import numpy
import random
import scipy

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

#read the training data and store all the datapoints
trainingdata = open("optdigits.train",'r')
arrayofdatapoint = []                   #array of datapoints
numberK = 30                            #number of K. Change K here
arrayofclass = []
for line in trainingdata:
    temparray = converstringtoint(line)
    arrayofclass.append(temparray[-1])
    temparray.pop()
    arrayofdatapoint.append(numpy.array(temparray))

bestsse = 1000000000.0                  #final sum-squared error
arrayofbestK = []                       #array of k centroid 
arrayClusterofeachBestK = []            #array of data in each cluster
arrayofCorrespondingclass = []          #array of corresponding class in each data in each cluster    

#begin to calculate the centroid, calculate 5 time to find the best
for time in range(5):
    arrayofK = []
    sse = 1000000000.0
    #random k cluster
    for i in range(numberK):
        randomK = []
        for j in range(64):
            randomK.append(random.randint(0,16))
        arrayofK.append(numpy.array(randomK))
    
    checkstop = False
    tempCluster = []
    tempclass = []
    while(checkstop == False):
        arrayClusterofeachK = [[] for x in range(numberK)]
        arrayoftrackclass = [[] for x in range(numberK)]

        for i in range(len(arrayofdatapoint)):
            closestdis = numpy.linalg.norm(arrayofdatapoint[i]-arrayofK[0])
            closecandidate = 0
            for j in range(1,numberK):
                tempdis = numpy.linalg.norm(arrayofdatapoint[i]-arrayofK[j])
                if(tempdis < closestdis):
                    closestdis = tempdis
                    closecandidate = j
            arrayClusterofeachK[closecandidate].append(arrayofdatapoint[i])
            arrayoftrackclass[closecandidate].append(arrayofclass[i])         

        for i in range(numberK):
            if(len(arrayClusterofeachK[i])==0):
                randomK = []
                for j in range(64):
                    randomK.append(random.randint(0,16))
                arrayofK[i] = numpy.array(randomK)
            elif(len(arrayClusterofeachK[i])==1):
                arrayofK[i] = arrayClusterofeachK[i][0]
            else:
                temp = arrayClusterofeachK[i][0]
                for j in range(1,len(arrayClusterofeachK[i])):
                    temp = numpy.vstack((temp,arrayClusterofeachK[i][j]))
                arrayofK[i] = temp.mean(axis=0)
        tempsse = 0.0
        for i in range(numberK):
            temp = 0.0
            for j in range(len(arrayClusterofeachK[i])):
                temp += pow(numpy.linalg.norm(arrayClusterofeachK[i][j]-arrayofK[i]),2.0)
            tempsse += temp  
        if(tempsse < sse):
            sse = tempsse
        else:
            checkstop = True
            tempCluster = arrayClusterofeachK
            tempclass = arrayoftrackclass
    if(sse < bestsse):        
        bestsse = sse
        arrayofbestK = arrayofK
        arrayClusterofeachBestK = tempCluster
        arrayofCorrespondingclass = tempclass

#calculate entropy in each cluster
arrayofEntropyOfeachK = []
for i in range(numberK):
    numberofinstanceinclusteri = len(arrayClusterofeachBestK[i]) 
    tempEntropy = 0.0
    for j in range(10):
        numberofinstwithclassj = 0.0
        for k in range(numberofinstanceinclusteri):
            if(arrayofCorrespondingclass[i][k] == j):
                numberofinstwithclassj += 1.0
        if(numberofinstanceinclusteri == 0):
            proba = 0
        else:
            proba = numberofinstwithclassj/numberofinstanceinclusteri
        if(proba!=0):
            tempEntropy += proba * math.log(proba, 2.0)
    tempEntropy = tempEntropy * (-1.0)
    arrayofEntropyOfeachK.append(tempEntropy)
#calculate average entropy   
averageEntropy = 0.0
for i in range(numberK):
    temp = float(len(arrayClusterofeachBestK[i]))/len(arrayofdatapoint)
    averageEntropy += temp * arrayofEntropyOfeachK[i]

#calculate the most frequency class
arrayoffrequencyclassofK = []
for i in range(numberK):
    arrayofcountclass = [0,0,0,0,0,0,0,0,0,0]
    for j in range(len(arrayClusterofeachBestK[i])):
        arrayofcountclass[arrayofCorrespondingclass[i][j]] += 1
    temp1 = max(arrayofcountclass)
    temp2 = arrayofcountclass.index(temp1)
    if(temp1 == 0):
        arrayoffrequencyclassofK.append(random.randint(0,9))
    else:
        arrayoffrequencyclassofK.append(temp2)

#test on test data
testdata = open("optdigits.test",'r')
arrayofactualclass = []
arrayofpredictclass = []
for line in testdata:
    temparray = converstringtoint(line)
    arrayofactualclass.append(temparray[-1])
    temparray.pop()
    testexample = numpy.array(temparray)
     
    closestdis = numpy.linalg.norm(testexample-arrayofbestK[0])
    closecandidate = 0
    for i in range(1,numberK):
        tempdis = numpy.linalg.norm(testexample-arrayofbestK[i])
        if(tempdis < closestdis):
            closestdis = tempdis
            closecandidate = i
    arrayofpredictclass.append(arrayoffrequencyclassofK[closecandidate])

#print out the result: sum-squared error, Average Entropy, Accuracy on test data, and confusion matrix
accuracy = 0.0
confusionmatrix = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]

for i in range (len(arrayofactualclass)):
    confusionmatrix[arrayofpredictclass[i]][arrayofactualclass[i]] += 1
    if (arrayofactualclass[i] == arrayofpredictclass[i]):
        accuracy += 1.0
print "Sum-Squared error:" + str(bestsse)
print "Average Entropy: " + str(averageEntropy)
print "Accuracy on test data: " + str(accuracy/len(arrayofactualclass))
print "The Confusion Matrix:"
print " |0 1 2 3 4 5 6 7 8 9"
print "-|- - - - - - - - - -"
for i in range(10):
    print str(i) + "|" + str(confusionmatrix[0][i]) + " " + str(confusionmatrix[1][i]) + " " + str(confusionmatrix[2][i]) + " "+ str(confusionmatrix[3][i]) + " "+ str(confusionmatrix[4][i]) + " "+ str(confusionmatrix[5][i]) + " "+ str(confusionmatrix[6][i]) + " "+ str(confusionmatrix[7][i]) + " "+ str(confusionmatrix[8][i]) + " "+ str(confusionmatrix[9][i])

#Visualize the resulting cluster centers in jpg format
for i in range(numberK):
    drawMatrix = numpy.split(arrayofbestK[i],8)        
    scipy.misc.imsave("digitofCluster"+str(i+1)+".jpg", drawMatrix)
