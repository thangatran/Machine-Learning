import random
import os
import subprocess
import math

testFile = open ('spam.test','r')    # Test file contains examples S
arrayoftestExample = []              # all possible examples in S
numberoftestExample = 0              # total number of examples
arrayofW = []                        # array of weight w
numberofBoosting = 20                # number of boosting iterations K. for experiment 2 K=10 and experiment 3 K=20 
arrayofalpha = []                    # array of alpha values
arrayofhypothesis = []               # array of hypothesis e.g. h1, h2, h3,..,hk

#read file to arrayoftestExample and initialize w
for line in testFile:
    arrayoftestExample.append(line)
numberoftestExample = len(arrayoftestExample)
for i in range(numberoftestExample):
    arrayofW.append(1.0/numberoftestExample)

#begin doing Adaboost algorithm
print 'The Ensemble Learing H is running. Please wait...'
for i in range(numberofBoosting):
    arrayofSpacedW = []
    tempnum = 0.0
    arrayofSpacedW.append(tempnum)
    for j in range(numberoftestExample):
        tempnum += arrayofW[j]    
        arrayofSpacedW.append(tempnum)
    St = open ('temp.train', 'w')
    for h in range(numberoftestExample):
        randomnum = random.random() 
        for g in range(numberoftestExample):
            if(arrayofSpacedW[g]<=randomnum<=arrayofSpacedW[g+1]): 
                St.write(arrayoftestExample[g])
                break
    FNULL = open(os.devnull, 'w')
    subprocess.call(["./svm_learn","-t","0","temp.train","temp.model"], stdout=FNULL, stderr=subprocess.STDOUT)
    subprocess.call(["./svm_classify","spam.test","temp.model","temp.predictions"], stdout=FNULL, stderr=subprocess.STDOUT)
    predicFile = open ('temp.predictions','r')
    epsilon = 0
    count = 0
    arrayofpredic = []
    for line in predicFile:
        if((line[0]!='-' and arrayoftestExample[count][0]=='-') or (line[0]=='-' and arrayoftestExample[count][0]!='-')):
            epsilon += arrayofW[count]   
        count+=1
        arrayofpredic.append(line)
    arrayofhypothesis.append(arrayofpredic)
    alpha = (math.log((1-epsilon)/epsilon))/2
    arrayofalpha.append(alpha)

    for m in range(numberoftestExample):
        if(arrayoftestExample[m][0]=='-'):
            y = -1
        else:
            y = 1
        if(arrayofpredic[m][0]=='-'):
            h = -1
        else:
            h = 1
        arrayofW[m] = arrayofW[m] * math.exp((-1)*alpha*y*h)

    Z = sum(arrayofW)
    for n in range(numberoftestExample):
        arrayofW[n] = arrayofW[n]/Z
    print 'Finished ' + str(i+1) + ' boosting iterations'

#calculating the final H for test data
Hypo = []
for i in range(numberoftestExample):
    tempNum = 0
    for j in range(numberofBoosting):
        if(arrayofhypothesis[j][i][0]=='-'):
            tempNum += arrayofalpha[j]*(-1)    
        else:
            tempNum += arrayofalpha[j]*1
    if tempNum>=0:
        Hypo.append(1)
    else:
        Hypo.append(-1)

#calculating the test accuracy of H
numberofAccuracy = 0.0
for i in range (numberoftestExample):
    if(Hypo[i]==1 and arrayoftestExample[i][0]!='-'):
        numberofAccuracy += 1
    if(Hypo[i]==-1 and arrayoftestExample[i][0]=='-'):
        numberofAccuracy += 1
print 'Final test accuracy of H is ' + str(numberofAccuracy/numberoftestExample)

