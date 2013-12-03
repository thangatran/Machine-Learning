import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

predictFile = open ('spam.predictions','r')  # spam predictions file
testFile = open ('spam.test','r')            # spam test file
arrayofValue = []                            # array of values in the predicitons file
arrayofThreshold = []                        # array of 20 threshold
arrayofTestExample = []                      # array of test examples
numberofPositive = 0                         # number of positive
numberofNegative = 0                         # number of negative
arrayofTPrate = []                           # array of true positive rate
arrayofFPrate = []                           # array of false positive rate

#reading predictions file and calculating 20 thresholds
for line in predictFile:
    arrayofValue.append(float(line))
increNum = (max(arrayofValue) - min(arrayofValue))/19 
tempvalue = min(arrayofValue)
for i in range(20):
    arrayofThreshold.append(tempvalue)
    tempvalue = tempvalue + increNum 

#reading test file
for line in testFile:
    if(line[0] == '1'):
        arrayofTestExample.append(1)
        numberofPositive += 1
    else:
        arrayofTestExample.append(-1)
        numberofNegative += 1

#calculating TPR and FPR
numberofExample = numberofPositive + numberofNegative 
for i in range(20):
    numberofTP = 0.0
    numberofFP = 0.0
    for j in range(numberofExample):
        if(arrayofValue[j] >= arrayofThreshold[i]):
            if(arrayofTestExample[j] == 1):
                numberofTP += 1
            else:
                numberofFP += 1
    arrayofTPrate.append(numberofTP/numberofPositive)
    arrayofFPrate.append(numberofFP/numberofNegative)

#plot the ROC curve and output to pdf file
fig = plt.figure()
plt.plot(arrayofFPrate,arrayofTPrate,'ro',arrayofFPrate,arrayofTPrate,'b')
print arrayofFPrate
print arrayofTPrate
plt.axis('scaled')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve')
pp = PdfPages('outputROCcurve.pdf')
fig.savefig(pp, format='pdf')
pp.close()
