'''
Name: Thang Tran
CS445 - Homework 2
'''

import random
#Covert string of number to array of number. For example: convert "1,2,3" to [1,2,3]
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

#Calculate the predicted output of a given example and weight
def calculateOk(attributes, we):
    result = we[0]
    for i in range(len(attributes)-1):
        result += (we[i+1]* attributes[i])
    if result>0:
        return 1
    if result<0:
        return -1
    if result==0:
        return 0

#Calculate the Accuracy of a test data, with a given weight, and which classification is negative
def calculateAccuracy (testdata, we, negative):
    numberofcorrect = 0.00
    for i in range(len(testdata)):
        example = converstringtoint(testdata[i])
        output = calculateOk(example,we)
        if((output == 1 and example[-1]!=negative) or (output == -1 and example[-1]==negative)):
            numberofcorrect += 1
    return numberofcorrect/len(testdata)

#Similar to the calculateAccuracy method, but in addition, it calculates the confusion maxtrix e.g. TP,FP,FN,TN 
def AccuracyAndMatrix (testdata, we, negative):
    global numberofpostivecorrect
    global numberofpostiveincorrect
    global numberofnegativecorrect
    global numberofnegativeincorrect
    numberofcorrect = 0.00
    for i in range(len(testdata)):
        example = converstringtoint(testdata[i])
        output = calculateOk(example,we)
        if(output == 1 and example[-1]!=negative):
            numberofcorrect += 1
            numberofpostivecorrect += 1
        elif(output == -1 and example[-1]==negative):
            numberofcorrect += 1
            numberofnegativecorrect += 1 
        elif(output == 1 and example[-1]==negative):
            numberofpostiveincorrect += 1
        elif(output == -1 and example[-1]!=negative): 
            numberofnegativeincorrect += 1
    return numberofcorrect/len(testdata)

#Calculate each task of 2 given numbers (positive and negative), with the initialize random weight, and the learning rate
def task(positivetrain,negativetrain, weight, learningrate):
    samplenega = converstringtoint(negativetrain[0])
    trainingdata = positivetrain + negativetrain
    accuracy = 0.00;
    global numberofepochs
    while (accuracy < 1.00):
        numberofepochs += 1
        for i in range(len(trainingdata)):
            example = converstringtoint(trainingdata[i])
            output = calculateOk(example,weight)
            if example[-1] != samplenega[-1]:
                target = 1
            else:
                target = -1
            deltaw = learningrate*(target-output)*1
            weight[0] += deltaw 
            for j in range(64):
                deltaw = learningrate*(target-output)*example[j]
                weight[j+1] += deltaw
        accuracy = calculateAccuracy(trainingdata, weight, samplenega[-1])
    return weight           

#Our main function will go here

fin1 = open('optdigits.data', 'r')
fin2 = open('optdigits.test', 'r')
fout = open('outputResult','w')

#reading the training data, and save all the examples into an array
trainnums = [[],[],[],[],[],[],[],[],[],[]]
for line in fin1:
    if line[-1] != '\n':
        line += '\n'
    if line[-2] == '0':
        trainnums[0].append(line) 
    elif line[-2] == '1':
        trainnums[1].append(line)
    elif line[-2] == '2':
        trainnums[2].append(line)
    elif line[-2] == '3':
        trainnums[3].append(line)
    elif line[-2] == '4':
        trainnums[4].append(line)
    elif line[-2] == '5':
        trainnums[5].append(line)
    elif line[-2] == '6':
        trainnums[6].append(line)
    elif line[-2] == '7':
        trainnums[7].append(line)
    elif line[-2] == '8':
        trainnums[8].append(line)
    elif line[-2] == '9':
        trainnums[9].append(line)

#reading and saving the test data
testnums = [[],[],[],[],[],[],[],[],[],[]]
for line in fin2:
    if line[-1] != '\n':
        line += '\n'
    if line[-2] == '0':
        testnums[0].append(line) 
    elif line[-2] == '1':
        testnums[1].append(line)
    elif line[-2] == '2':
        testnums[2].append(line)
    elif line[-2] == '3':
        testnums[3].append(line)
    elif line[-2] == '4':
        testnums[4].append(line)
    elif line[-2] == '5':
        testnums[5].append(line)
    elif line[-2] == '6':
        testnums[6].append(line)
    elif line[-2] == '7':
        testnums[7].append(line)
    elif line[-2] == '8':
        testnums[8].append(line)
    elif line[-2] == '9':
        testnums[9].append(line)

#Begin to train each task as well as test the task with the resulting weight
LearningRate = 0.05     #Change learning rate here
numberoftask = 0
print 'The perceptrons are calculating. Please wait...'
for u in range(9):
    v = u + 1
    while(v<=9):
        w = []
        for i in range(65):
            w.append(round(random.uniform(-0.9,0.9),1))
        numberofepochs = 0
        numberofpostivecorrect = 0
        numberofpostiveincorrect = 0
        numberofnegativecorrect = 0
        numberofnegativeincorrect = 0
        numberoftask += 1
        fout.write("Task " + str(numberoftask) + ": " + str(u) + " and " + str(v) + '\n')
        w = task(trainnums[u],trainnums[v], w, LearningRate)
        fout.write("    -Number of epochs: ")
        fout.write(str(numberofepochs) + '\n')
        testdata = testnums[u] + testnums[v]
        fout.write("    -Accuracy on training data: 100\n")
        fout.write("    -Accuracy on test data: ")
        fout.write(str(AccuracyAndMatrix(testdata, w, v)*100) + '\n')
        fout.write("    -Confusion Matrix :")
        fout.write(" " + str(numberofpostivecorrect) + ' ')
        fout.write(str(numberofnegativeincorrect)+ '\n')
        fout.write("                        " + str(numberofpostiveincorrect)+ ' ')
        fout.write(str(numberofnegativecorrect)+ '\n')
        v += 1
print 'Done! The result can be found in the file named outputResult'
