# This is the LeadLag program. It processes folder.SMTTRN.csv files produced by DAAP10
# There one output file; folder.LL.csv considers both all turns of speech (TOS) and those TOS
#  with at least TurnL words.

import re
import os
import statistics
import math
TurnL = 25


def correl(list1, list2):
    if len(list1) != len(list2):
        print('unequal number of items for Corr', len(list1), len(list2))
    mean1 = statistics.mean(list1)
    mean2 = statistics.mean(list2)
    psum = 0
    var1 = 0
    var2 = 0
    corr = 0
    for i1 in range(len(list1)):
        var1 += (list1[i1] - mean1) ** 2
        var2 += (list2[i1] - mean2) ** 2
        psum += (list1[i1] - mean1) * (list2[i1] - mean2)
    if var1 > 0 and var2 > 0:
        correl = psum / math.sqrt(var1 * var2)
    return correl


def firstquartile(numlist):
    a = sorted(numlist)
    n = len(a)
    if n < 5:
        answer = 'NA'
    else:
        if n % 4 == 0:
            lowanswer = a[int(n/4) - 1]
            highanswer = a[int(n/4)]
            answer = (highanswer + lowanswer)/2
        elif n % 4 == 1:
            lowanswer = a[int((n - 1)/4) - 1]
            highanswer = a[int((n - 1)/4)]
            answer = (lowanswer + highanswer)/2
        elif n % 4 == 2:
            answer = a[int((n+2)/4) - 1]
        elif n % 4 == 3:
            answer = a[int((n + 1)/4 - 1)]
    return answer


def thirdquartile(numlist):
    a = sorted(numlist)
    n = len(a)
    if n < 5:
        answer = 'NA'
    else:
        if n % 4 == 0:
            lowanswer = a[int(3*n/4) - 1]
            highanswer = a[int(3*n/4)]
            answer = (lowanswer + highanswer)/2
        elif n % 4 == 1:
            lowanswer = a[int(3*(n - 1)/4)]
            highanswer = a[int(3*(n - 1)/4) + 1]
            answer = (lowanswer + highanswer) / 2
        elif n % 4 == 2:
            answer = a[int(3*(n + 2)/4) - 2]
        elif n % 4 == 3:
            answer = a[int((3*n + 3)/4) - 1]
    return answer

WDics = []
Dir = input('Type the name of the directory to be processed')
os.chdir(Dir)
os.chdir('Dics')
Dics0 = os.listdir('.')

for v in range(len(Dics0)):
    SplitFile = re.split('\.', Dics0[v])
    if len(SplitFile) > 2:
        print('ERROR 7: File name contains more than one period (dot)')
        # print('ERROR 7: File name contains more than one period (dot)', file=open(LOGFile, 'a'))
        continue
    elif len(SplitFile) == 1:
        continue
    elif re.match('Wt', SplitFile[1]) is not None:
        WDics.append(Dics0[v])

os.chdir('../DATA')

InFile = Dir + '.SMTTRN.csv'
OutFile = Dir +'.LLCorrs.csv'
open (OutFile, 'w')
print ('File, n All S1Leads, Words All S1Leads, n 25 S1Leads, Words25 S1Leads, WRAD25 S1Leads, n All S2Leads,'
       ' Words All S2Leads, n 25 S2Leads, Words25 S2Leads,WRAD25 S2Leads', file=open(OutFile, 'a'))
Start = 0
NewDATA = []
WDic = []
File = ''
for line in open(InFile):
    if re.search('\w', line) is None:
        continue
    elif re.search('File', line) is not None:
        Columns = re.split(r',', line)
        for j in range(len(WDics)):
            Dic = re.split('\.', WDics[j])
            D = Dic[0]
            Top = D + ' Mean'
            for i in range(len(Columns)):
                if re.search(Top, Columns[i]) is not None:
                    WDic.append(i)
                    break
    elif re.search('File', line) is None:
        Columns = re.split(',', line)
        NewDATA.append(Columns)

for i in range(len(NewDATA)):
    if i == 0:
        File = NewDATA[0][0]
MinTurn = 5

print('The default minimum number of turns of speech for the LL correlation is currently 5')
print('If you wish to change this, type the new number')
Response = input()
if re.match('\d+',Response) is not None:
    MinTurn = int(Response)
Words121 = []
Words122 = []
Words211 = []
Words212 = []
Words25121 = []
Words25122 = []
Words25211 = []
Words25212 = []
WRAD121 = []
WRAD122 = []
WRAD211 = []
WRAD212 = []
GCorrAW12 = []
GCorr25W12 = []
GCorr25WRAD12 = []
GCorrAW21 = []
GCorr25W21 = []
GCorr25WRAD21 = []

for i in range(len(NewDATA) - 1):
    if NewDATA[i][0] == File and NewDATA[i + 1][0] == File:
        if NewDATA[i][2] == '1' and NewDATA[i + 1][2] == '2':
            Words121.append(int(NewDATA[i][3]))
            Words122.append(int(NewDATA[i + 1][3]))
            if int(NewDATA[i][3]) >= TurnL and int(NewDATA[i + 1][3]) >= TurnL:
                Words25121.append(int(NewDATA[i][3]))
                Words25122.append(int(NewDATA[i + 1][3]))
                WRAD121.append(float(NewDATA[i][WDic[0]]))
                WRAD122.append(float(NewDATA[i + 1][WDic[0]]))
        elif NewDATA[i][2] == '2' and NewDATA[i + 1][2] == '1':
            Words211.append(int(NewDATA[i][3]))
            Words212.append(int(NewDATA[i + 1][3]))
            if int(NewDATA[i][3]) >= TurnL and int(NewDATA[i + 1][3]) >= TurnL:
                Words25211.append(int(NewDATA[i][3]))
                Words25212.append(int(NewDATA[i + 1][3]))
                WRAD211.append(float(NewDATA[i][WDic[0]]))
                WRAD212.append(float(NewDATA[i + 1][WDic[0]]))

    elif NewDATA[i][0] == File and NewDATA[i + 1][0] != File:
        if len(Words121) > MinTurn:
            Corr1 = correl(Words121, Words122)
            GCorrAW12.append(Corr1)
        else:
            Corr1 = 'na'
        if len(Words25121) > MinTurn:
            Corr2 = correl(Words25121,Words25122)
            Corr3 = correl(WRAD121, WRAD122)
            GCorr25W12.append(Corr2)
            GCorr25WRAD12.append(Corr3)
        else:
            Corr2 = 'na'
            Corr3 = 'na'
        if len(Words211) > MinTurn:
            Corr4 = correl(Words211, Words212)
            GCorrAW21.append(Corr4)
        else:
            Corr4 = 'na'
        if len(Words25211) > MinTurn:
            Corr5 = correl(Words25211, Words25212)
            Corr6 = correl(WRAD211, WRAD212)
            GCorr25W21.append(Corr5)
            GCorr25WRAD21.append(Corr6)
        else:
            Corr5 = 'na'
            Corr6 = 'na'
        print(File, ',', len(Words121), ',', Corr1, ',', len(Words25121), ',', Corr2, ',', Corr3, end=',',
              file=open(OutFile, 'a'))
        print(len(Words211), ',', Corr4, ',', len(Words25211), ',', Corr5, ',', Corr6, file=open(OutFile, 'a'))

        File = NewDATA[i + 1][0]
        print('Now processing', File)
        Words121[:] = []
        Words122[:] = []
        Words211[:] = []
        Words212[:] = []
        Words25121[:] = []
        Words25122[:] = []
        Words25211[:] = []
        Words25212[:] = []
        WRAD121[:] = []
        WRAD122[:] = []
        WRAD211[:] = []
        WRAD212[:] = []

if len(Words121) > MinTurn:
    Corr1 = correl(Words121, Words122)
    GCorrAW12.append(Corr1)
else:
    Corr1 = 'na'
if len(Words25121) > MinTurn:
    Corr2 = correl(Words25121,Words25122)
    Corr3 = correl(WRAD121, WRAD122)
    GCorr25W12.append(Corr2)
    GCorr25WRAD12.append(Corr3)
else:
    Corr2 = 'na'
    Corr3 = 'na'
if len(Words211) > MinTurn:
    Corr4 = correl(Words211, Words212)
    GCorrAW21.append(Corr4)
else:
    Corr4 = 'na'
if len(Words25211) > MinTurn:
    Corr5 = correl(Words25211,Words25212)
    Corr6 = correl(WRAD211, WRAD212)
    GCorr25W21.append(Corr5)
    GCorr25WRAD21.append(Corr6)
else:
    Corr5 = 'na'
    Corr6 = 'na'

print(File, ',', len(Words121), ',', Corr1, ',', len(Words25121), ',', Corr2, ',', Corr3, end=',',
      file=open(OutFile,'a'))
print(len(Words211), ',', Corr4, ',', len(Words25211), ',', Corr5, ',', Corr6, file=open(OutFile,'a'))

print('\n\nStatistic,,AllWdsS1Leads,,25WdsS1Leads,WRADS1Leads,,AllWdsS2Leads,,Words25S2Leads,WRADS2Leads',
      file=open(OutFile,'a'))
Mean1 = statistics.mean(GCorrAW12)
Mean2 = statistics.mean(GCorr25W12)
Mean3 = statistics.mean(GCorr25WRAD12)
Mean4 = statistics.mean(GCorrAW21)
Mean5 = statistics.mean(GCorr25W21)
Mean6 = statistics.mean(GCorr25WRAD21)
Median1 = statistics.median(GCorrAW12)
Median2 = statistics.median(GCorr25W12)
Median3 = statistics.median(GCorr25WRAD12)
Median4 = statistics.median(GCorrAW21)
Median5 = statistics.median(GCorr25W21)
Median6 = statistics.median(GCorr25WRAD21)
SD1 = statistics.pstdev(GCorrAW12)
SD2 = statistics.pstdev(GCorr25W12)
SD3 = statistics.pstdev(GCorr25WRAD12)
SD4 = statistics.pstdev(GCorrAW21)
SD5 = statistics.pstdev(GCorr25W21)
SD6 = statistics.pstdev(GCorr25WRAD21)
FQ1 = firstquartile(GCorrAW12)
FQ2 = firstquartile(GCorr25W12)
FQ3 = firstquartile(GCorr25WRAD12)
FQ4 = firstquartile(GCorrAW21)
FQ5 = firstquartile(GCorr25W21)
FQ6 = firstquartile(GCorr25WRAD21)
TQ1 = thirdquartile(GCorrAW12)
TQ2 = thirdquartile(GCorr25W12)
TQ3 = thirdquartile(GCorr25WRAD12)
TQ4 = thirdquartile(GCorrAW21)
TQ5 = thirdquartile(GCorr25W21)
TQ6 = thirdquartile(GCorr25WRAD21)
Min1 = min(GCorrAW12)
Min2 = min(GCorr25W12)
Min3 = min(GCorr25WRAD12)
Min4 = min(GCorrAW21)
Min5 = min(GCorr25W21)
Min6 = min(GCorr25WRAD21)
Max1 = max(GCorrAW12)
Max2 = max(GCorr25W12)
Max3 = max(GCorr25WRAD12)
Max4 = max(GCorrAW21)
Max5 = max(GCorr25W21)
Max6 = max(GCorr25WRAD21)


print('Min,,', Min1, ',,', Min2, ',', Min3, ',,', Min4, ',,', Min5, ',', Min6, file=open(OutFile,'a'))
print('1stQuartile,,', FQ1, ',,', FQ2, ',', FQ3, ',,', FQ4, ',,', FQ5, ',', FQ6, file=open(OutFile,'a'))
print('Median,,', Median1, ',,', Median2, ',', Median3, ',,', Median4, ',,', Median5, ',', Median6,
      file=open(OutFile,'a'))
print('3RDQuartile,,', TQ1, ',,', TQ2, ',', TQ3, ',,', TQ4, ',,', TQ5, ',', TQ6, file=open(OutFile,'a'))
print('Max,,', Max1, ',,', Max2, ',', Max3, ',,', Max4, ',,', Max5, ',', Max6, file=open(OutFile,'a'))
print('Mean,,', Mean1, ',,', Mean2, ',', Mean3, ',,', Mean4, ',,', Mean5, ',', Mean6, file=open(OutFile,'a'))
print('SD,,', SD1, ',,', SD2, ',', SD3, ',,', SD4, ',,', SD5, ',', SD6, file=open(OutFile,'a'))
