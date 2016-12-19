#  NOTE: This program does not support either NADF or Z-Dictionaries.

#  This is DAAP10.1.3.py; it is based on DAAP09.6; it adds several
#  additional functions: The construction of density functions based
#  on user defined segmentation; automatic disambiguator for disfluency;
# and automatic designation of certain short turns of speech as non-interruptions.

#  Copyright (C) 2016 Bernard Maskit, Wilma Bucci and Sean Murphy

#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.

#   This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.


#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.

#    Contact Information:    Bernard Maskit: bmaskit@icloud.com
#                            Wilma Bucci: wbucci@icloud.com
#                            Sean Murphy: smurphy1@gmail.com


import os
import re
import math
import statistics
from operator import itemgetter

MTTWord = 50  # markers every MTTWord in the marked text

ListH1 = ['um-hmm', 'uh-huh', 'uh-oh', 'ah-ha', 'un-hum', 'mm-hmm']
ListH2 = ['anti', 'co', 'ex', 'mid', 'non', 'pro', 're', 'self']
ListK1 = ['some', 'any', 'this', 'that']
ListK2 = ['likex', 'ah', 'mm', 'uhm', 'um', 'er', 'hm', 'hmm', 'youknow', 'welld']

ListL1 = ['feel', 'feeling', 'feels', 'felt', 'look', 'looked', 'looking',
          'looks', 'seem', 'seemed', 'seeming', 'seems', 'sound', 'sounded',
          'sounding', 'sounds']
ListL3 = ['act', 'acted', 'acting', 'acts']
ListL4 = ['how', 'that', 'what']
ListL5 = ['would', 'should', 'could', 'shall', 'will', 'can', 'do', 'does',
          'd', 'll']
ListL6 = ['can', 'shouldn', 'shan', 'wouldn', 'don', 'didn', 'won']
ListL7 = ['can', 'could', 'do', 'might', 'should', 'would', 'will']
ListL9 = ['get']
ListL10 = ['i', 'you', 'we', 'they']
ListL12 = ['i', 'it', 'he', 'she', 'you', 'they']
ListL13 = ['her', 'him', 'i', 'me', 'them', 'us']
ListL14 = ['this', 'that']
ListL15 = ['found', 'saw', 'heard']
ListM1 = ['aah', 'ah', 'ahh', 'eh', 'ehm', 'hm', 'hmm', 'hmmm', 'mhm', 'mhmm', 'mmm', 'uh',
          'uhh', 'uhhh', 'uhm', 'uhmm', 'um', 'umm', 'ummm', 'unh']
ListP1 = ['ah-ha', 'allright', 'alright', 'good', 'mmhm', 'mhmm', 'mm-hm', 'mm_hm', 'mm-hmm',
          'mmhmm', 'mm_hmm', 'ok', 'okay', 'right', 'sure', 'uh-huh', 'uhhuh',
          'um-hmm', 'umhmm', 'wow', 'yea', 'yeah', 'yep', 'yes', 'yup']
ListW1 = ['awfully', 'feeling', 'into', 'really', 'definitely',
          'particularly', 'very', 'somewhat', 'doing', 'quite',
          'perfectly']
ListW3 = ['in', 'on', 'by', 'and', 'near', 'far', 'to', 'of', 'now', 'before',
          'then', 'think', 'say', 'said', 'says', 'well', 'welld', 'like',
          'liked']
ListW5 = ['i', 'we', 'if', 'and', 'or', 'but', 'well', 'why', 'where', 'who',
          'what', 'how']
ListX1 = ['aah', 'ah', 'ahh', 'ahhh', 'eh', 'ehm', 'er', 'hm', 'hmm', 'hmmm', 'huh', 'like',
          'mm', 'mh', 'mhm', 'mhmm', 'mmhmm', 'mmmhmm', 'mmm', 'mmmm', 'mmmm', 'mmmmm', 'oh', 'so', 'uh', 'uhm', 'uhh',
          'uhhh', 'um', 'um-hm', 'uhmm', 'uhhmm', 'um', 'umhmm', 'umm', 'ummm', 'well', 'welld']
ListY1 = ['this', 'that', 'what', 'who', 'where', 'when', 'which', 'how']
ListY2 = ['should', 'would', 'can', 'shall', 'will', 'do', 'if']

ListL2 = []
for line in open('ListL2.txt'):
    ListL2.append(line.rstrip())
ListL8 = []
for line in open('ListL8.txt'):
    ListL8.append(line.rstrip())
ListL11 = []
for line in open('ListL11.txt'):
    ListL11.append(line.rstrip())
ListW2 = []
for line in open('ListW2.txt'):
    ListW2.append(line.rstrip())
ListLOL = []
for line in open('TheDic.txt'):
    ListLOL.append(line.rstrip())


def remove_non_ascii_1(text):
    return ''.join(q1 for q1 in text if ord(q1) < 128)


def disambiguator(text):  # returns list of words

    paren = 0
    errors = []
    errorn = 0
    words3 = []
    words1 = re.split(r'([([)\]])', text)
    for word1 in words1:
        if word1 == '(' or word1 == ']':
            paren += 1
        elif word1 == ')' or word1 == ']':
            paren -= 1
        else:
            if paren < 0:
                errors.append('ERROR 3')
                errorn += 1
            elif paren > 0:
                continue
            elif paren == 0:
                phrases = re.split(r'[.,?!;:]', word1)
                for phrase in phrases:
                    words2 = []
                    words2t = re.split(r'\s', phrase)
                    for word2t in words2t:
                        if re.match('\w+-\w+', word2t) is not None:
                            word2t = word2t.replace('-', '')
                        word2t = word2t.replace('_', '')
                        newworda = re.search("(\w+)'(\w+)", word2t)
                        if newworda is not None:
                            newword1 = newworda.group(1)
                            newword2 = newworda.group(2)
                            words2.append(newword1)
                            words2.append(newword2)
                        else:
                            newwordb = re.search("\W?(\w+-?)\W?", word2t)
                            if newwordb is not None:
                                newwordb = newwordb.group(1)
                                words2.append(newwordb)

                    if len(words2) > 0:
                        words2[0] = words2[0].replace('like', 'likex')
                        words2[0] = words2[0].replace('well', 'welld')

                    if len(words2) > 1:
                        if words2[0] == 'you' and words2[1] == 'know':
                            if len(words2) == 2:
                                words2[1] = 'knowd'
                            elif len(words2) > 2:
                                hit = 0
                                for listmat in ListY1:
                                    if listmat == words2[2]:
                                        hit += 1
                                if hit == 0:
                                    words2[1] = 'knowd'

                    for w in range(len(words2)):
                        if re.search('^\W?ok\W?$', words2[w]) is not None:
                            words2[w] = 'okay'

                    for w in range(len(words2)):
                        for listmat1 in ListM1:
                            if listmat1 == words2[w]:
                                words2[w] = 'mm'

                    for w in range(len(words2)):  # Like1
                        if words2[w] == 'like':
                            for listmat2 in ListL1:
                                if listmat2 == words2[w - 1]:
                                    words2[w] = 'likec'

                    if 7 > len(words2) > 1:
                        if words2[len(words2) - 1] == 'like':
                            words2[len(words2) - 1] = 'likex'

                    for w in range(1, len(words2)):
                        if words2[w] == 'like':
                            for listmat3 in ListL2:
                                if listmat3 == words2[w - 1]:
                                    words2[w] = 'likex'

                    for w in range(1, len(words2)):
                        if words2[w] == 'like' and ((words2[w - 1] == 'was') or
                           (words2[w - 1] == 'is') or (words2[w - 1] == 's')):
                                words2[w] = 'likex'

                    for w in range(2, len(words2)):
                        if words2[w] == 'like' and words2[w - 1] == 'not' and words2[w - 2] == 's':
                            words2[w] = 'likex'

                    for w in range(1, len(words2) - 1):
                        if words2[w] == 'like' and words2[w + 1] == 'i':
                            for listmat4 in ListL3:
                                if listmat4 == words2[w - 1]:
                                    words2[w] = 'likec'

                    for w in range(len(words2) - 1):
                        if words2[w] == 'like':
                            for listmat5 in ListL1:
                                if listmat5 == words2[w + 1]:
                                    words2[w] = 'likex'

                    for w in range(len(words2) - 2):
                        if words2[w] == 'like' and words2[w + 1] == 'i' and words2[w + 2] == 'don':
                            words2[w] = 'likex'

                    for w in range(len(words2) - 1):
                        if words2[w] == 'like':
                            if words2[w + 1] == 'you':
                                words2[w] = 'likex'

                    for w in range(3, len(words2)):
                        if words2[w] == 'like':
                            if words2[w - 2] == 'it' and words2[w - 1] == 's':
                                hit = 0
                                for listmat6 in ListL4:
                                    if listmat6 == words2[w - 3]:
                                        words2[w] = 'likec'
                                        hit += 1
                                if hit == 0:
                                    words2[w] = 'likex'

                    for w in range(1, len(words2)):
                        if words2[w] == 'like':
                            for listmat7 in ListL5:
                                if listmat7 == words2[w - 1]:
                                    words2[w] = 'likev'

                    for w in range(2, len(words2)):
                        if words2[w] == 'like' and words2[w - 1] == 't':
                            for listmat8 in ListL6:
                                if listmat8 == words2[w - 2]:
                                    words2[w] = 'likev'

                    for w in range(2, len(words2)):
                        if words2[w] == 'like' and words2[w - 1] == 'not':
                            for listmat9 in ListL7:
                                if listmat9 == words2[w - 2]:
                                    words2[w] = 'likev'

                    for w in range(1, len(words2) - 1):
                        if words2[w] == 'like':
                            for listmat10 in ListL8:
                                if listmat10 == words2[w - 1]:
                                    hit = 0
                                    for listmat11 in ListL10:
                                        if listmat11 == words2[w + 1]:
                                            hit += 1
                                            words2[w] = 'likex'
                                    if hit == 0:
                                        words2[w] = 'likec'

                    for w in range(1, len(words2)):
                        if words2[w] == 'like' and words2[w - 1] == 'to':
                            for listmat12 in ListL8:
                                if listmat12 == words2[w - 2]:
                                    words2[w] = 'likex'

                    for w in range(1, len(words2) - 1):
                        if words2[w] == 'like' and words2[w + 1] == 'to':
                            hit = 0
                            for listmat13 in ListL10:
                                if listmat13 == words2[w - 1]:
                                    hit = 1
                            if hit > 0:
                                words2[w] = 'likev'

                    for w in range(1, len(words2) - 1):
                        if words2[w] == 'like':
                            hit = 0
                            for listmat14 in ListL10:
                                if listmat14 == words2[w - 1]:
                                    if listmat14 != words2[w + 1]:
                                        hit = 1
                            if hit > 0:
                                words2[w] = 'likev'

                    for w in range(1, len(words2) - 1):
                        if words2[w] == 'like':
                            for listmat15 in ListL12:
                                if listmat15 == words2[w + 1]:
                                    words2[w] = 'likec'

                    for w in range(len(words2) - 1):
                        if words2[w] == 'like':
                            for listmat16 in ListL13:
                                if listmat16 == words2[w + 1]:
                                    words2[w] = 'likev'

                    for w in range(2, len(words2) - 1):
                        if words2[w] == 'like':
                            for listmat17 in ListL14:
                                hit1 = 0
                                if listmat17 == words2[w + 1]:
                                    hit1 = 1
                                    for listmat18 in ListL15:
                                        if listmat18 == words2[w - 1]:
                                            hit1 = 2
                                if hit1 == 1:
                                    words2[w] = 'likec'
                                elif hit1 == 2:
                                    words2[w] = 'likex'

                    for w in range(len(words2) - 2):
                        if words2[w] == 'you' and words2[w + 1] == 'know':
                            hit1 = 0
                            hit2 = 0
                            for listmat19 in ListY1:
                                if listmat19 == words2[w + 2]:
                                    hit1 = 1
                            for listmat20 in ListY2:
                                if listmat20 == words2[w - 1]:
                                    hit2 = 1
                            if hit1 == 0 and hit2 == 0:
                                words2[w + 1] = 'knowd'

                    for w in range(1, len(words2)):
                        if words2[w] == 'well' and words2[w - 1] == 'as':
                            words2[w] = 'wellc'

                    for w in range(1, len(words2)):
                        if words2[w] == 'well':
                            hit = 0
                            for listmat21 in ListW1:
                                if listmat21 == words2[w - 1]:
                                    hit = 1
                            for listmat22 in ListW2:
                                if listmat22 == words2[w - 1]:
                                    hit = 1
                            if hit == 1:
                                words2[w] = 'wella'

                    for w in range(1, len(words2)):
                        if words2[w] == 'well':
                            hit = 0
                            for listmat23 in ListW3:
                                if listmat23 == words2[w - 1]:
                                    hit = 1
                            for listmat24 in ListK2:
                                if listmat24 == words2[w - 1]:
                                    hit = 1
                            if hit == 1:
                                words2[w] = 'welld'

                    for w in range(len(words2) - 1):
                        if words2[w] == 'well':
                            for listmat24 in ListW5:
                                if listmat24 == words2[w + 1]:
                                    words2[w] = 'welld'

                    for w in range(len(words2) - 1):
                        if words2[w] == 'well' and words2[w + 1] == 'of':
                            words2[w] = 'wellw'

                    if len(words2) > 2:
                        if words2[len(words2) - 1] == 'know' \
                                and words2[len(words2) - 2] == 'you':
                            words2[len(words2) - 1] = 'knowd'

                    for w in range(len(words2) - 1):
                        if words2[w] == 'like' and words2[w + 1] == 'welld':
                            words2[w] = 'likex'

                    for w in range(len(words2) - 1):
                        if words2[w] == 'like' and words2[w + 1] == 'mean':
                            words2[w] = 'likex'

                    for w in range(len(words2)):
                        if words2[w] == 'well':
                            words2[w] = 'welld'
                        if words2[w] == 'likex':
                            words2[w] = 'like'

                    if len(words2) > 0:
                        if words2[0] == 'likev' or words2[0] == 'likec':
                            words2[0] = 'like'

                    if len(words2) > 0:
                        for w in range(len(words2)):
                            words3.append(words2[w])
    return words3


def wordcount(text):  # return = [ErrorsN,List of Errors] or [0, WordCount, Words]
    paren = 0
    wordn = 0
    errors = []
    errorn = 0
    final = []
    words = ''
    words1 = re.split(r'([([)\]])', text)
    for word1 in words1:
        if word1 == '(' or word1 == '[':
            paren += 1
        elif word1 == ')' or word1 == ']':
            paren -= 1
        else:
            if paren < 0:
                errors.append('ERROR 3')
                errorn += 1
            elif paren > 0:
                continue
            elif paren == 0:
                words2 = re.split(r'\s', word1)
                for word2 in words2:
                    words3 = re.split(r"'", word2)
                    for word3 in words3:
                        words = words + ' ' + word3
                        if re.search('.*\w', word3) is not None:
                            wordn += 1
    if paren > 0:
        errors.append('ERROR 2')
        errorn += 1
    final.append(errorn)
    if errorn > 0:
        final.append(errors)
    elif errorn == 0:
        newwords = disambiguator(words)
        nwordn = len(newwords)
        final.append(nwordn)
        if nwordn > 0:
            snewwords = str(newwords[0])
            for w in range(1, len(newwords)):
                snewwords = snewwords + ' ' + str(newwords[w])
        else:
            snewwords = ''
        final.append(snewwords)
    return final


def mttwords(text):  # Return [[Errors], words, number of words]
    paren = 0
    rawwords = text[0]
    errors = []
    errorn = 0
    final = []
    wordn = int(text[1])
    words = ''
    words1 = re.split(r'([([)\]])', rawwords)
    for word1 in words1:
        if word1 == '(' or word1 == '[':
            paren += 1
            words += word1
        elif word1 == ')' or word1 == ']':
            paren -= 1
            words += word1
        else:
            if paren < 0:
                errors.append('ERROR 3')
                errorn += 1
            elif paren > 0:
                words += word1
                continue
            elif paren == 0:
                words2 = re.split(r'\s', word1)
                for word2 in words2:
                    words = words + ' ' + word2
                    words3 = re.split(r"'", word2)
                    for word3 in words3:
                        if re.search('\w', word3) is not None:
                            wordn += 1
                            if wordn % MTTWord == 0:
                                words = words + ' [' + str(wordn) + '] '
    if paren > 0:
        errors.append('ERROR 2')
        errorn += 1
    final.append(errorn)
    if errorn > 0:
        final.append(errors)
    elif errorn == 0:
        final.append(words)
        final.append(wordn)
    return final


def smallturns(wordn, text):  # returns 'X' or 'P' or 'N' (meaning not 'X' and not 'P')
    list1 = re.split('\s', text)
    list2 = []
    for word in list1:
        if re.search('\w', word) is not None:
            newword = re.search('\W?(\w+)\W?', word)
            list2.append(newword.group(1))
    mark = []
    for word2 in list2:
        locmark = 'a'
        for ow in ListX1:
            if ow == word2:
                locmark = 'X'
                break
        for ow in ListP1:
            if ow == word2:
                locmark = 'P'
                break
        mark.append(locmark)
    psum = 0
    xsum = 0
    stfinal = 'N'
    if wordn == 0:
        stfinal = 'X'
    for m1 in mark:
        if m1 == 'P':
            psum += 1
        elif m1 == 'X':
            xsum += 1

    if xsum == wordn:
        stfinal = 'X'
    if xsum + psum == wordn and psum > 0:
        stfinal = 'P'

    return stfinal


def finalsplit(num, text):  # Returns [number of errors, list of words, number of words]
    mfin = ''
    errorn = 0
    wordn = num
    paren = 0
    words1 = re.split(r'([([)\]])', text)

    for word1 in words1:
        if word1 == '(' or word1 == '[':
            paren += 1
            mfin = mfin + ' ' + word1
        elif word1 == ')' or word1 == ']':
            paren -= 1
            mfin = mfin + word1 + ' '
        else:
            if paren < 0:
                print('ERROR 3: Improper parentheses in: ', text, 'at word number:', wordn)
                print('ERROR 3: Improper parentheses in: ', text, 'at word number:', wordn,
                      file=open(LOGFile, 'a'))
                errorn += 1
            elif paren > 0:
                mfin = mfin + ' ' + word1
            elif paren == 0:
                words2 = re.split(r'\s', word1)
                for word2 in words2:
                    mfin = mfin + ' ' + word2
                    if re.match('\w+-', word2) is not None:
                        wordn += 1
                        if wordn % MTTWord == 0:
                            mfin = mfin + ' [' + str(wordn) + ']'
                    else:
                        word2 = word2.replace('-', '')
                        if re.match('.*\w+.*', word2) is not None:
                            firstsplit = re.split("'", word2)
                            for fwd in firstsplit:
                                newsplit = re.split('\W', fwd)
                                for swd in newsplit:
                                    if re.match('.*\w.*', swd) is not None:
                                        wordn += 1
                                        if wordn % MTTWord == 0:
                                            mfin = mfin + ' [' + str(wordn) + ']'
            continue

    final = [errorn, mfin, wordn]
    return final


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
            answer = lowanswer + (highanswer - lowanswer)/4
        elif n % 4 == 2:
            answer = a[int((n+2)/4) - 1]
        elif n % 4 == 3:
            lowanswer = a[int((n - 3)/4)]
            highanswer = a[int((n + 1)/4)]
            answer = lowanswer + 3*(highanswer - lowanswer)/4
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
            lowanswer = a[int(3*(n - 1)/4) - 1]
            highanswer = a[int(3*(n - 1)/4)]
            answer = lowanswer + 3*(highanswer - lowanswer)/4
        elif n % 4 == 2:
            answer = a[int(3*(n + 2)/4) - 2]
        elif n % 4 == 3:
            lowanswer = a[int(3*(n - 3)/4)]
            highanswer = a[int(3*(n + 1)/4)]
            answer = lowanswer + (highanswer - lowanswer)/4
    return answer

param = 100
paraq = 2.0
totalwgt = 0
for j3 in range(1, param):
    totalwgt += 2 * math.exp(-paraq * (param ** 2) * ((param ** 2) + j3 ** 2) / ((param ** 2 - j3 ** 2) ** 2))
totalwgt += math.exp(-paraq)


def wts(i1):
    weight = math.exp((-paraq * (param ** 2) * (param ** 2 + i1 ** 2)) / (param ** 2 - i1 ** 2) ** 2)
    return weight


def smth(list1):
    vals = []
    for i1 in range(len(list1)):
        vals.append(list1[i1])
    for i1 in range(len(list1)):
        vals.append(list1[len(list1) - 1 - i1])
    mod = len(vals)
    smooth = []
    for i1 in range(len(list1)):
        avg = 0
        for j1 in range(1, param):
            if i1 - j1 < 0:
                k1 = (j1 - i1 - 1) % mod
                avg += float(vals[k1]) * wts(j1)
            else:
                k1 = (i1 - j1) % mod
                avg += float(vals[k1]) * wts(j1)
        for j2 in range(param):
            k2 = (i1 + j2) % mod
            avg += float(vals[k2]) * wts(j2)
        avg /= totalwgt
        smooth.append(avg)
    return smooth


def covar(list1, list2):
    if len(list1) != len(list2):
        print('unequal number of items for Covar', len(list1), len(list2))
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
        corr = psum / math.sqrt(var1 * var2)
    return corr

Directory = input('Type subDirectory name containing your files:')
os.chdir(Directory)
LOGFile = 'DATA/' + Directory + '.LOGFile.txt'
open(LOGFile, 'w')
MTTFile = 'DATA/' + Directory + '.MTTFile.txt'
open(MTTFile, 'w')
SMTAG0File = 'DATA/' + Directory + '.SMTAG0.csv'
open(SMTAG0File, 'w')
RAWAG0File = 'DATA/' + Directory + '.RAWAG0.csv'
open(RAWAG0File, 'w')
RAWAG1File = 'DATA/' + Directory + '.RAWAG1.csv'
open(RAWAG1File, 'w')
SMTAG1File = 'DATA/' + Directory + '.SMTAG1.csv'
open(SMTAG1File, 'w')
RAWAG2File = 'DATA/' + Directory + '.RAWAG2.csv'
open(RAWAG2File, 'w')
SMTAG2File = 'DATA/' + Directory + '.SMTAG2.csv'
open(SMTAG2File, 'w')
TTGFile = 'DATA/' + Directory + '.TTG.txt'
open(TTGFile, 'w')
RAWTRNFile = 'DATA/' + Directory + '.RAWTRN.csv'
open(RAWTRNFile, 'w')
SMTTRNFile = 'DATA/' + Directory + '.SMTTRN.csv'
open(SMTTRNFile, 'w')
LOLFile = 'DATA/' + Directory + '.LOL.txt'
open(LOLFile, 'w')

TxtFiles = []
SMTFiles = []
WRDFiles = []
TTRFiles = []
Files0 = os.listdir('.')
for v in range(len(Files0)):
    SplitFile = re.split('\.', Files0[v])
    if len(SplitFile) > 2:
        print('ERROR 7: File name contains more than one period (dot)')
        print('ERROR 7: File name contains more than one period (dot)', file=open(LOGFile, 'a'))
        continue
    elif len(SplitFile) == 1:
        continue
    elif re.match('txt', SplitFile[1]) is not None or re.match('TXT', SplitFile[1]) is not None:
        TxtFiles.append(Files0[v])
        WRDFile = 'DATA/' + SplitFile[0] + '.WRD.csv'
        WRDFiles.append(WRDFile)
        SMTFile = 'DATA/' + SplitFile[0] + '.SMT.csv'
        SMTFiles.append(SMTFile)
        TTRFile = 'DATA/' + SplitFile[0] + '.TTR.txt'
        TTRFiles.append(TTRFile)
    else:
        continue
DFDic = -1
ACATS = []
DCATS = []
OCATS = []
CurrOCAT = {}
StartSwitch = 0
CATList = []
CATS = {}
TDics = []
DCATSDic = {}
TTGList = []
os.chdir('./Dics')
DicFiles = []
Dics = {}
WDic = []
DicsN = 0
WDicsN = 0
ERRORS = 0
GSpeakers = []
DicFiles0 = os.listdir('.')
for dic in DicFiles0:
    if re.search('\.', dic) is None:
        DicFiles.append(dic)
        DicsN += 1

    elif re.search('\.Wt', dic) is not None:
        DicFiles.append(dic)
        DicsN += 1
        WDicsN += 1
        DicSplit = re.split('\.', dic)
        WDic.append(DicSplit[0])

DicFiles = sorted(DicFiles)

for v in range(len(DicFiles)):
    if DicFiles[v] == 'DF':
        DFDic = v
    for line in open(DicFiles[v]):
        NewLine = re.split('\s', line)
        if len(NewLine) == 2:
            if NewLine[0] not in Dics:
                if v == 0:
                    Dics[NewLine[0]] = [1]
                elif v > 0:
                    List = []
                    for k in range(v):
                        List.append(0)
                    List.append(1)
                    Dics[NewLine[0]] = List
            elif NewLine[0] in Dics:
                List = Dics[NewLine[0]]
                if len(List) < v:
                    for k in range(v - len(List)):
                        List.append(0)
                List.append(1)
                Dics[NewLine[0]] = List
        elif (len(NewLine)) == 3:

            if NewLine[0] not in Dics:
                if v == 0:
                    Dics[NewLine[0]] = NewLine[1]
                elif v > 0:
                    List = []
                    for k in range(v):
                        List.append(0)
                    List.append(NewLine[1])
                    Dics[NewLine[0]] = List
            elif NewLine[0] in Dics:
                List = Dics[NewLine[0]]
                if len(List) < v:
                    for k in range(v - len(List)):
                        List.append(0)
                    List.append(NewLine[1])
                else:
                    List.append(NewLine[1])
                Dics[NewLine[0]] = List

for word in Dics:
    if len(Dics[word]) < len(DicFiles):
        for j in range(len(DicFiles) - len(Dics[word])):
            Dics[word].append(0)
if WDicsN > 0:
    for word in Dics:
        for j in range(DicsN - WDicsN, DicsN):
            Dics[word][j] = .5 * (float(Dics[word][j]) + 1)

os.chdir('..')

for v in range(len(TxtFiles)):
    open(WRDFiles[v], 'w')
    open(SMTFiles[v], 'w')
    open(TTRFiles[v], 'w')
    print('TurnNo,Word,Spkr', end=',', file=open(WRDFiles[v], 'a'))
    StartSwitch = 0
    CatSwitch = 0
    c9Check = 0
    xCheck = 0
    tCheck = 0
    dCheck = 0
    NewSpkr = 0
    TurnN = 0
    ERRORS1 = 0
    FileTTList = {}
    TempCATS = {}
    print('We are now reading ', TxtFiles[v])
    print('\nWe are now reading ', TxtFiles[v], file=open(LOGFile, 'a'))
    print('\nWe are now reading ', TxtFiles[v], file=open(MTTFile, 'a'))
    LnDAT = []

    for Oldline in open(TxtFiles[v], errors='ignore'):  # permits non-ascii characters
        line = remove_non_ascii_1(Oldline)  # Removes non-ascii characters
        line = line.replace("o'clock", "oclock")
        line = line.replace("o-clock", "oclock")
        line = line.replace("o_clock", "oclock")
        line = line.replace('wella', 'well')
        line = line.replace('wellc', 'well')
        line = line.replace('welld', 'well')
        line = line.replace('wellw', 'well')
        line = line.replace('likec', 'like')
        line = line.replace('likev', 'like')
        line = line.replace('kindf', 'kind')
        line = line.replace('meanf', 'mean')
        line = line.replace('knowd', 'know')
        line = line.replace("'em", 'them (em)')
        line = line.replace('gonna', 'going to (gonna)')
        line = line.replace('hafta', 'have to (hafta)')
        line = line.replace('wanna', 'want to (wanna)')
        line = line.replace('gotta', 'got to (gotta)')
        line = line.replace('woulda', 'would have (woulda)')
        line = line.replace('coulda', 'could have (coulda)')
        line = line.replace('shoulda', 'should have (shoulda)')
        line = line.replace('kinda', 'kind of (kinda)')
        line = line.replace('outta', 'out of (outta)')
        line = line.replace('sorta', 'sort of (sorta)')
        line = line.replace('lotta', 'lot of (lotta)')
        line = line.replace('lotsa', 'lots of (lotsa)')
        line = line.replace('dunno', "don't know (dunno)")
        line = line.replace('uh huh', 'uhhuh')
        line = line.replace('_', '-')
        line = line.replace("'cause", 'because')
        line = line.replace("'til", 'until')
        line = line.replace(' ya', ' you (ya)')
        line = line.replace('#', '(Number sign)')

        if re.search(r'.*\S+\\.*', line) is not None:
            print('ERROR 1: Backslash not at first character in Line:\n', line)
            print('ERROR 1: Backslash not at first character in Line:\n', line, file=open(LOGFile, 'a'))
            ERRORS1 += 1
        if re.match(r'\\c9', line) is not None:
            c9Check += 1
            LineProp = ['L', '\\c9']
            LnDAT.append(LineProp)
            break

        elif re.match(r'\s?\\t(.*)$', line) is not None:
            CatSwitch = 1
            Cat = ''
            Inst = ''
            Match = re.match(r'\s?\\t(.*)', line)
            Remain = Match.group(1)
            if re.search(r'\s?(\w+)\s?:\s?(\w+)\s?$', Remain) is not None:
                TentCat = re.search(r'\s?(\w+)\s?:\s?(\w+)\s?$', Remain)
                Cat = TentCat.group(1)
                Inst = TentCat.group(2)

                if v == 0 and StartSwitch == 0:
                    if Cat in CATS:
                        print('ERROR 11: Same category ', cat, 'appears twice at beginning of file, ', TxtFiles[v])
                        print('ERROR 11: Same category ', cat, 'appears twice at beginning of file, ', TxtFiles[v],
                              file=open('DATA/LOGFile.txt', 'a'))
                        ERRORS1 += 1
                    else:
                        CATS[Cat] = Inst
                        LineProp = ['T', Cat, Inst]
                        LnDAT.append(LineProp)
                        CATList.append(Cat)
                elif v > 0 and StartSwitch == 0:
                    if Cat in TempCATS:
                        print('ERROR 11: Same category ', cat, 'appears twice at beginning of file, ', TxtFiles[v])
                        print('ERROR 11: Same category ', cat, 'appears twice at beginning of file, ', TxtFiles[v],
                              file=open('DATA/LOGFile.txt', 'a'))
                        ERRORS1 += 1
                    else:
                        TempCATS[Cat] = Inst
                        LineProp = ['T', Cat, Inst]
                        LnDAT.append(LineProp)
                elif StartSwitch > 0:
                    if Cat not in CATS:
                        print('ERROR 10: category ', cat, 'not listed at top of first file: ', TxtFiles[0])
                        print('ERROR 10: category ', cat, 'not listed at top of first file: ', TxtFiles[0],
                              file=open('DATA/LOGFile.txt', 'a'))
                        ERRORS1 += 1
                    else:
                        CATS[Cat] = Inst
                        LineProp = ['T', Cat, Inst]
                        LnDAT.append(LineProp)

            else:
                print('ERROR 8: Improper \\t line:', line)
                print('ERROR 8: Improper \\t line:', line, file=open('DATA/LOGFile.txt', 'a'))
                ERRORS1 += 1
            continue
        else:
            line = line.lower()
            if re.search(r'\s?\\op', line) is not None:
                NewBalance = re.search(r'\s?\\op\s+?(\d+)\s?(.*)$', line)
                if NewBalance is not None:
                    Marker = 'P'
                    Speaker = NewBalance.group(1)
                    CurrentSpkr = Speaker
                    Words = NewBalance.group(2)
                    LineProp = ['P', Speaker, Words]
                    LnDAT.append(LineProp)

            elif re.search(r'\s?\\ox', line) is not None:  # \x with override
                NewBalance = re.search(r'\s?\\ox\s+?(\d+)\s?(.*)$', line)
                if NewBalance is not None:
                    Marker = 'X'
                    Speaker = NewBalance.group(1)
                    Words = NewBalance.group(2)
                    CurrentSpkr = Speaker
                    LineProp = ['X', Speaker, Words]
                    LnDAT.append(LineProp)

            elif re.search(r'\s?\\os', line) is not None:  # \s with override, not to be changed to \x or \p
                NewBalance = re.search(r'\s?\\os\s+?(\d+)\s?(.*)', line)
                StartSwitch += 1
                if NewBalance is not None:
                    Marker = 'O'
                    Speaker = NewBalance.group(1)
                    Words = NewBalance.group(2)
                    CurrentSpkr = Speaker
                    LineProp = [Marker, Speaker, Words]
                    LnDAT.append(LineProp)

            elif re.search(r'\s?\\s.*', line) is not None:  # backslash s is present otherwise
                if StartSwitch == 0 and v == 0 and CatSwitch > 0:
                    print('For each of the following categories, please respond to the category name by typing')
                    print('"d" to indicate that you wish this category to be used to make a density function')
                    print('(There must be a dictionary with the category name in your text files folder)')
                    print('or type "a" to indicate that you wish data to be amalgamated across this category')
                    print('or just hit RETURN if you do not want to use this category in either of these ways.')

                    for cat in CATList:
                        print(cat)
                        response = input()
                        if response == 'a' or response == 'A':
                            ACATS.append(cat)
                            OCATS.append(cat)
                        elif response == 'd' or response == 'D':
                            DCATS.append(cat)
                        else:
                            OCATS.append(cat)
                    for cat in DCATS:
                        DCATSDic[cat] = {}
                        for dline in open(cat):
                            Weight = re.split('\s', dline)
                            DCATSDic[cat][Weight[0]] = float(Weight[1])
                    OCATS = sorted(OCATS)
                    CATList = sorted(CATList)
                for i in range(len(DicFiles)):
                    NewDic = re.split('\.', DicFiles[i])
                    if len(NewDic) > 1 and NewDic[1] == 'Wt':
                        DicFiles[i] = NewDic[0]
                if len(DCATS) > 0:
                    TDics = DCATS + DicFiles
                else:
                    TDics = DicFiles
                if StartSwitch == 0 and v == 0:
                    print('File, Speaker, Words, Turns', end=',', file=open(SMTAG0File, 'a'))
                    print('File, Speaker', end=',', file=open(SMTAG1File, 'a'))
                    print('File,Speaker', end=',', file=open(RAWAG1File, 'a'))
                    print('File,Speaker', end=',', file=open(SMTAG2File, 'a'))
                    print('File,Speaker', end=',', file=open(RAWAG2File, 'a'))

                    for cat in OCATS:
                        print(cat, end=',', file=open(SMTAG1File, 'a'))
                        print(cat, end=',', file=open(RAWAG1File, 'a'))
                        print(cat, end=',', file=open(SMTAG2File, 'a'))
                        print(cat, end=',', file=open(RAWAG2File, 'a'))

                    print('Words,Turns,', end='', file=open(SMTAG1File, 'a'))
                    print('Words,Turns,', end='', file=open(RAWAG1File, 'a'))
                    print('Words,Turns,', end='', file=open(SMTAG2File, 'a'))
                    print('Words,Turns,', end='', file=open(RAWAG2File, 'a'))

                    for i in range(len(TDics)):
                        print(TDics[i], 'Mean,', TDics[i], 'SD,', end='', file=open(SMTAG1File, 'a'))
                        print(TDics[i], 'Mean,', TDics[i], 'SD,', end='', file=open(SMTAG2File, 'a'))

                    for i in range(len(WDic)):
                        print(WDic[i], 'MHigh,', WDic[i], 'HighProp,', end='', file=open(SMTAG1File, 'a'))
                        print(WDic[i], 'MHigh,', WDic[i], 'HighProp,', end='', file=open(SMTAG2File, 'a'))

                    for i in range(len(TDics)):
                        for j in range(i + 1, len(TDics)):
                            print(TDics[i], '_', TDics[j], end=',', file=open(SMTAG1File, 'a'))
                            print(TDics[i], '_', TDics[j], end=',', file=open(SMTAG2File, 'a'))
                    print('', file=open(SMTAG1File, 'a'))
                    print('', file=open(SMTAG2File, 'a'))

                    for i in range(len(DicFiles)):
                        if DicFiles[i] not in WDic:
                            print(DicFiles[i], 'Match,', DicFiles[i], 'Coverage,', DicFiles[i], 'ODDS,', end='',
                                  file=open(RAWAG1File, 'a'))
                            print(DicFiles[i], 'Match,', DicFiles[i], 'Coverage,', DicFiles[i], 'ODDS,', end='',
                                  file=open(RAWAG2File, 'a'))

                        elif DicFiles[i] in WDic:
                            print(DicFiles[i], 'Match,', DicFiles[i], 'Coverage,', end='',
                                  file=open(RAWAG1File, 'a'))
                            print(DicFiles[i], 'Pos Match,', DicFiles[i], 'Pos Prop,', end='',
                                  file=open(RAWAG1File, 'a'))
                            print(DicFiles[i], 'Match,', DicFiles[i], 'Coverage,', end='',
                                  file=open(RAWAG2File, 'a'))
                            print(DicFiles[i], 'Pos Match,', DicFiles[i], 'Pos Prop,', end='',
                                  file=open(RAWAG2File, 'a'))
                    print('\n', file=open(RAWAG1File, 'a'))
                    print('\n', file=open(RAWAG2File, 'a'))
                    for i in range(len(TDics)):
                        print(TDics[i], 'Mean,', TDics[i], 'SD,', end='', file=open(SMTAG0File, 'a'))
                    for i in range(len(WDic)):
                        print(WDic[i], 'MHigh,', WDic[i], 'HighProp,', end='', file=open(SMTAG0File, 'a'))
                    for i in range(len(TDics)):
                        for j in range(i + 1, len(TDics)):
                            print(TDics[i], '_', TDics[j], end=',', file=open(SMTAG0File, 'a'))
                    print('\n', file=open(SMTAG0File, 'a'))
                    print('File,Speaker,Words,Turns,TurnL1stQ,TurnLMed,TurnL3rdQ,TurnLMean,TurnLMAX,TurnLMIN',
                          end=',', file=open(RAWAG0File, 'a'))
                    for i in range(len(DicFiles) - WDicsN):
                        print(DicFiles[i], 'Match,', DicFiles[i], 'Coverage,', DicFiles[i], 'ODDS,', end='',
                              file=open(RAWAG0File, 'a'))
                    for i in range(len(WDic)):
                        print(WDic[i], 'Match,', WDic[i], 'Coverage,', end='', file=open(RAWAG0File, 'a'))
                        print(WDic[i], 'Pos Match,', WDic[i], 'Pos Prop,', end='', file=open(RAWAG0File, 'a'))
                    print('', file=open(RAWAG0File, 'a'))

                StartSwitch += 1

                Balance = re.search(r'\s?\\(s\w?\w?)\s?(\d+)(.*)$', line)
                if Balance is not None:  # Good case of \s line
                    Marker = 'S'
                    TurnN += 1
                    NewSpkr = int(Balance.group(2))
                    CurrentSpkr = NewSpkr
                    Content = Balance.group(3)
                    LineProp = [Marker, NewSpkr, Content]
                    StartSw = 1
                    LnDAT.append(LineProp)

                else:
                    print('ERROR 12: Improper \\s syntax at TxtFiles,line: ', TxtFiles[v], line)
                    print('ERROR 12: Improper \\s syntax at line: ', line, file=open(LOGFile, 'a'))
                    ERRORS1 += 1

            elif re.search(r'\s?\\x.*', line) is not None:  # backslash x is present without override
                Balance = re.search(r"\s?\\x\s?(\d+)(.*)$", line)
                if Balance is not None:  # Good case of \x line
                    Marker = 'S'
                    NewSpkr = int(Balance.group(1))
                    Content = Balance.group(2)
                    LineProp = [Marker, NewSpkr, Content]
                    CurrentSpkr = NewSpkr
                    StartSwitch += 1
                LnDAT.append(LineProp)

            elif re.search(r'\s?\\p.*', line) is not None:  # backslash p is present, but not overridden
                StartSwitch += 1
                Balance = re.search(r'\s?\\p\s?(\d+)(.*)$', line)
                if Balance is not None:  # Good case of \p line
                    Marker = 'S'
                    NewSpkr = int(Balance.group(1))
                    CurrentSpkr = NewSpkr
                    Content = Balance.group(2)
                    LineProp = [Marker, NewSpkr, Content]
                    LnDAT.append(LineProp)

                else:
                    print('ERROR 12: Improper \\p syntax at line: ', line)
                    print('ERROR 12: Improper \\p syntax at line: ', line, file=open(LOGFile, 'a'))
                    ERRORS1 += 1

            else:  # not \t or \n or \no or \s or \p or \po or \x or \xo

                if re.search(r'\\', line) is not None:  # Other line containing a backslash
                    print('ERROR 12 Improper line containing a backslash', line)
                    print('ERROR 12 Improper line containing a backslash', line, file=open(LOGFile, 'a'))
                    ERRORS1 += 1

                elif re.search(r'\\', line) is None:  # Other line not containing a backslash
                    if TurnN == 0:
                        LineProp = ['F', line]
                        LnDAT.append(LineProp)

                    elif TurnN > 0:
                        Balance = re.search(r'^(.+)$', line)
                        if Balance is not None:  # Line contains something

                            Content = Balance.group(1)
                            LineProp = ['C', CurrentSpkr, Content]
                            LnDAT.append(LineProp)

                        elif Balance is None:  # No backslash and no content
                            LineProp = ['Z', line]
                            LnDAT.append(LineProp)

    if v > 0 and len(CATS) != len(TempCATS):
        print('ERROR 12: File', TxtFiles[v], 'has incorrect number of \\t lines at head of file: len(TempCATS) = ',
              len(TempCATS), 'len(CATS = ', len(CATS))
        print('ERROR 12: File', TxtFiles[v], 'has incorrect number of \\t lines at head of file',
              file=open(LOGFile, 'a'))
        ERRORS1 += 1
    if v > 0:
        for Cat in CATS:
            if Cat not in TempCATS:
                print('ERROR 12: The list of Categories at head of file ', TxtFiles[v], 'does not match the list of '
                      'categories at head of file', TxtFiles[0])
                ERRORS1 += 1

    if c9Check == 0:
        print('ERROR 14: Missing \\c9')
        print('ERROR 14: Missing \\c9', file=open(LOGFile, 'a'))
        ERRORS1 += 1
    CurrSpkr = 0
    cat = ''
    inst = ''

    for i in range(len(LnDAT)):  # correct for 'categories into densities'
        if LnDAT[i][0] == 'T':
            cat = LnDAT[i][1]
            inst = LnDAT[i][2]
            if cat in DCATS:
                LnDAT[i][0] = 'D'
                Wt = DCATSDic[cat][inst]
                LnDAT[i].append(Wt)

    for i in range(len(LnDAT)):  # adjoin immediately following 'C' lines to 'S' line; re-mark 'C' as 'Y'
        if LnDAT[i][0] == 'F' or LnDAT[i][0] == 'T' or LnDAT[i][0] == 'D':
            continue
        elif LnDAT[i][0] == 'X' or LnDAT[i][0] == 'P':
            continue
        elif LnDAT[i][0] == 'S':
            Words = LnDAT[i][2]
            for j in range(i + 1, len(LnDAT)):
                if LnDAT[j][0] == 'Z':
                    continue
                elif LnDAT[j][0] == 'C':
                    if LnDAT[j][1] != LnDAT[i][1]:
                        print("Strange Error, line marked 'C' after line marked 'S' with different spkr:", LnDAT[i])
                    elif LnDAT[j][1] == LnDAT[i][1]:
                        Words = Words + ' ' + LnDAT[j][2]
                        LnDAT[i][2] = Words
                        LnDAT[j][0] = 'Y'
                else:
                    break

    for i in range(len(LnDAT)):  # where correct, change 'S' to 'X' or 'P'; change 'O' to 'S'
        if LnDAT[i][0] == 'S':
            LocSplit = wordcount(LnDAT[i][2])
            if LocSplit[0] > 0:
                ERRORS1 += LocSplit[0]
                for k in range(1, len(LocSplit)):
                    print('ERROR 2 or 3, parentheses error, in line ', LnDAT[i][2], LocSplit[k])
                    print('ERROR 2 or 3, parentheses error, in line ', LnDAT[i][2], LocSplit[k],
                          file=open(LOGFile, 'a'))
            elif LocSplit[0] == 0:
                if LocSplit[1] == 0:
                    LnDAT[i][0] = 'X'
                elif 0 < LocSplit[1] < 3:
                    NewMark = smallturns(LocSplit[1], LnDAT[i][2])
                    if NewMark == 'X' or NewMark == 'P':
                        LnDAT[i][0] = NewMark
                    else:
                        LnDAT[i].append(LocSplit[1])
                else:
                    LnDAT[i].append(LocSplit[1])

        elif LnDAT[i][0] == 'O':
            LnDAT[i][0] = 'S'
            LocSplit = wordcount(LnDAT[i][2])
            if LocSplit[0] > 0:
                ERRORS1 += LocSplit[0]
                for k in range(1, len(LocSplit)):
                    print('ERROR 2 or 3, parentheses error, in line ', LnDAT[i][2], LocSplit[k])
                    print('ERROR 2 or 3, parentheses error, in line ', LnDAT[i][2], LocSplit[k],
                          file=open(LOGFile, 'a'))
            elif LocSplit[0] == 0:
                LnDAT[i].append(LocSplit[1])
    tCheck = 0
    for i in range (len(LnDAT)):
        if LnDAT[i][0] == 'T' or LnDAT[i][0] == 'D':
            tCheck = 1
            for j in range(i + 1, len(LnDAT)):
                if LnDAT[j][0] == 'T' or LnDAT[j][0] == 'D' or LnDAT[j][0] == 'P' or LnDAT[j][0] == 'X':
                    continue
                elif LnDAT[j][0] == 'S':
                    break
                    tCheck = 0
                elif LnDAT[j][0] == 'C':
                    print('ERROR 13: There is no speaker ID after a \\t line\n', LnDAT[i][1], ':', LnDAT[i][2], '\n',
                          LnDAT[j][2])
                    print('ERROR 13: There is no speaker ID after a \\t line\n', LnDAT[i][1], ':', LnDAT[i][2], '\n',
                          LnDAT[j][2], file=open(LOGFile,'a'))
    MDAT = []
    WordN = 0
    sx = {}
    sp = {}
    CurrentSpkr = 0
    CurrentTurn = 0
    TurnStor = ''
    TurnSw = 0
    GWordN = 0
    for i in range(len(LnDAT)):
        if LnDAT[i][0] == 'F' or LnDAT[i][0] == 'T' or LnDAT[i][0] == 'L':
            MDAT.append(LnDAT[i])
        elif CurrentTurn == 0 and LnDAT[i][0] == 'D':
            MDAT.append(LnDAT[i])
        elif LnDAT[i][0] == 'S':
            CurrentTurn += 1
            Words = LnDAT[i][2]
            WordsN = LnDAT[i][3]

            for j in range(i + 1, len(LnDAT)):
                if LnDAT[j][0] == 'T' or LnDAT[j][0] == 'L' or LnDAT[j][0] == 'D':
                    break
                elif LnDAT[j][0] == 'X':
                    Words = Words + ' (' + str(LnDAT[j]) + ')'
                    if LnDAT[j][1] in sx:
                        sx[LnDAT[j][1]] += 1
                    elif LnDAT[j][1] not in sx:
                        sx[LnDAT[j][1]] = 1
                elif LnDAT[j][0] == 'P':
                    Words = Words + ' (' + str(LnDAT[j]) + ')'
                    if LnDAT[j][1] in sp:
                        sp[LnDAT[j][1]] += 1
                    elif LnDAT[j][1] not in sp:
                        sp[LnDAT[j][1]] = 1
                elif LnDAT[j][0] == 'Z' or LnDAT[j][0] == 'Y':
                    continue
                elif LnDAT[j][0] == 'S' or LnDAT[j][0] == 'C':
                    if LnDAT[j][1] == LnDAT[i][1]:
                        Words = Words + ' ' + LnDAT[j][2]
                        LnDAT[j][0] = 'Y'
                    else:
                        break
            LnDAT[i][2] = Words
            MDAT.append(LnDAT[i])
    WordCt = 0
    TurnN = 0
    for i in range(len(MDAT)):
        if MDAT[i][0] == 'F':
            print(MDAT[i][1], file=open(MTTFile, 'a'))
        elif MDAT[i][0] == 'T':
            print('\\T ', MDAT[i][1], ':', MDAT[i][2], file=open(MTTFile, 'a'))
        elif MDAT[i][0] == 'D' and TurnN == 0:
            print(MDAT[i], file=open(MTTFile, 'a'))
        elif MDAT[i][0] == 'S':
            TurnN += 1
            Old = [MDAT[i][2], WordCt]
            New = mttwords(Old)
            WordCt = New[2]
            TurnMark = '[Turn ' + str(TurnN) + ']'
            print('\\s ', MDAT[i][1], TurnMark, New[1], file=open(MTTFile, 'a'))
        elif MDAT[i][0] == 'C':
            print('Strange Error at MDAT[i]')
        elif MDAT[i][0] == 'L':
            print('\\c9', file=open(MTTFile, 'a'))
        else:
            continue

    print('\nThe total number of words in file', TxtFiles[v], 'is', WordCt, file=open(MTTFile, 'a'))
    for Spkr in sp:
        print('\nThe number of positive NTVs by Speaker', Spkr, 'is', sp[Spkr], file=open(MTTFile, 'a'))
    for Spkr in sx:
        print('\nThe number of neutral NTVs by Speaker', Spkr, 'is', sx[Spkr], file=open(MTTFile, 'a'))

    PDAT = []
    Start = 0
    for i in range(len(LnDAT)):  # Close up blank lines and 'C' lines; and apply wordcound
        if LnDAT[i][0] == 'T':
            PDAT.append(LnDAT[i])
        elif LnDAT[i][0] == 'D':
            PDAT.append(LnDAT[i])
        elif LnDAT[i][0] == 'Z' or LnDAT == 'X' or LnDAT == 'F' or LnDAT == 'P':
            continue
        elif LnDAT[i][0] == 'L':
            PDAT.append(LnDAT[i])
        elif LnDAT[i][0] == 'S':
            Start += 1
            Words = LnDAT[i][2]
            for j in range(i + 1, len(LnDAT)):
                if LnDAT[j][0] == 'Z' or LnDAT[j][0] == 'X' or LnDAT[j][0] == 'P' or LnDAT[j][0] == 'Y':
                    continue
                elif LnDAT[j][0] == 'T' or LnDAT[j][0] == 'D':
                    break
                elif LnDAT[j][0] == 'S' or LnDAT[j][0] == 'C':
                    if LnDAT[j][1] == LnDAT[i][1]:
                        Words = Words + ' ' + LnDAT[j][2]
                        LnDAT[j][0] = 'Y'
                    else:
                        break
            LocSplit = wordcount(LnDAT[i][2])
            if LocSplit[0] > 0:
                ERRORS1 += LocSplit[0]
                for k in range(1, len(LocSplit)):
                    print('ERROR 2 or 3, parentheses error, in line ', LnDAT[i][2], LocSplit[k])
                    print('ERROR 2 or 3, parentheses error, in line ', LnDAT[i][2], LocSplit[k],
                          file=open(LOGFile, 'a'))
            elif LocSplit[0] == 0:
                LnDAT[i][3] = LocSplit[1]
                LnDAT[i].append(LocSplit[2])
                PDAT.append(LnDAT[i])

    Speakers = []
    for List in PDAT:
        if List[0] == 'S':
            if List[1] in Speakers:
                continue
            elif List[1] not in Speakers:
                Speakers.append(int(List[1]))
    Speakers = sorted(Speakers)
    for i in range(len(Speakers)):
        if Speakers[i] != i + 1:
            print('ERROR 5. The list of Speakers has impermissable gaps\n', 'Speakers = ', Speakers)
    SpeakersN = len(Speakers)
    if SpeakersN > len(GSpeakers):
        GSpeakers = Speakers

    if ERRORS1 > 0:
        print('First Pass complete: There are', ERRORS1,
              'errors, listed in the LogFile; these must be corrected and DAAP10 rerun to complete second pass')
        print('First Pass complete: There are', ERRORS1,
              'errors, listed above; these must be corrected and DAAP10 rerun to complete second pass',
              file=open(LOGFile, 'a'))

    elif ERRORS1 == 0:
        CurrTurn = 0
        CurrSpkr = 0
        Spkr = []
        SpkrID = 0
        Words = 0
        PreWdBank = ''
        RAW = []
        SMTH = []
        TurnWts = []
        TurnWords = []
        CurrDCATWts = {}

        for q in range(len(OCATS)):
            print(OCATS[q], '(CAT)', end=',', file=open(WRDFiles[v], 'a'))
        for q in range(len(DCATS)):
            print(DCATS[q], '(D)', end=',', file=open(WRDFiles[v], 'a'))
        for q in range(DicsN):
            print(DicFiles[q], end=',', file=open(WRDFiles[v], 'a'))
        print('', file=open(WRDFiles[v], 'a'))
        print('Word', end=',', file=open(SMTFiles[v], 'a'))
        for m in range(len(Speakers)):
            for q in range(len(DCATS)):
                print(DCATS[q], ' S', Speakers[m], end=',', file=open(SMTFiles[v], 'a'))
            for y in range(DicsN):
                print(DicFiles[y], ' S', Speakers[m], end=',', file=open(SMTFiles[v], 'a'))

        print('', file=open(SMTFiles[v], 'a'))

        for i in range(len(PDAT)):  # T and D data
            if PDAT[i][0] == 'T':
                CurrOCAT[PDAT[i][1]] = PDAT[i][2]
            elif PDAT[i][0] == 'D':
                CurrDCAT = PDAT[i][1]
                CurrWt = PDAT[i][3]
                if CurrDCAT in CurrDCATWts:
                    CurrDCATWts[CurrDCAT] = CurrWt
                else:
                    CurrDCATWts[CurrDCAT] = CurrWt

            elif PDAT[i][0] == 'S' or PDAT[i][0] == 'C':
                for CAT in OCATS:
                    CurrCAT = [CAT, CurrOCAT[CAT]]
                    PDAT[i].append(CurrCAT)
                for CAT in CurrDCATWts:
                    CurrCAT = [CAT, CurrDCATWts[CAT]]
                    PDAT[i].append(CurrCAT)
            elif PDAT[i][0] == 'L':
                for CAT in CurrDCATWts:
                    CurrCAT = [CAT, CurrDCATWts[CAT]]
                    PDAT[i].append(CurrCAT)

        TDATA = []
        CompWord = []
        TTList = []
        for i in range(1, SpeakersN + 1):
            STTList = {}
            LSTTList = []
            for j in range(len(PDAT)):
                if PDAT[j][0] == 'S' or PDAT[j][0] == 'C':
                    if PDAT[j][1] == i:
                        Words = re.split('\s', PDAT[j][4])
                        for word in Words:
                            if word in STTList:
                                STTList[word] += 1
                            else:
                                STTList[word] = 1

            for word in STTList:
                ListItem = (word, STTList[word])
                LSTTList.append(ListItem)
            LSTTList = sorted(LSTTList, key=itemgetter(0))
            TTList.append(LSTTList)
            print('\nSpeaker = ', i, '\n', file=open(TTRFiles[v], 'a'))
            Types = len(LSTTList)
            Tokens = 0
            TTR = 0
            for j in range(len(LSTTList)):
                print(LSTTList[j][0], ',', LSTTList[j][1], file=open(TTRFiles[v], 'a'))
                Tokens += LSTTList[j][1]
            if Tokens > 0:
                TTR = Types / Tokens
            print('Types = ', Types, '; ', 'Tokens = ', Tokens, '; Ratio = ', TTR, file=open(TTRFiles[v], 'a'))

            if len(TTGList) < i:
                TTGList.append(LSTTList)
            else:
                TTGList[i - 1] = TTGList[i - 1] + LSTTList

        for i in range(len(PDAT)):  # Here we make the TDATA (TurnDATA) file

            if PDAT[i][0] == 'T':
                CurrOCAT[PDAT[i][1]] = PDAT[i][2]
            elif PDAT[i][0] == 'D':
                continue
            elif PDAT[i][0] == 'S':
                preTT = []
                WordN = PDAT[i][3]
                CurrSpkr = PDAT[i][1]
                CurrTurn += 1
                PDAT[i].append(CurrTurn)
                PreWdBank = PDAT[i][4]
                TurnWords = re.split('\s', PreWdBank)
                for j in range(len(TurnWords)):
                    WdFileData = [CurrTurn, TurnWords[j], CurrSpkr]
                    for m in range(len(CATList)):
                        for k in range(5, len(PDAT[i]) - 1):
                            if PDAT[i][k][0] == CATList[m]:
                                WdFileData.append(PDAT[i][k])
                    TDATA.append(WdFileData)
            elif PDAT[i][0] == 'C':
                PreWdBank = PreWdBank + ' ' + PDAT[i][4]
                WordN += PDAT[i][3]
                NewPreWdBank = PDAT[i][4]
                NewTurnWords = re.split('\s', NewPreWdBank)
                for j in range(len(NewTurnWords)):
                    WdFileData = [CurrTurn, NewTurnWords[j], CurrSpkr]
                    for m in range(len(CATList)):
                        for k in range(6, len(PDAT[i])):
                            if LnDAT[i][k][0] == CATList[m]:
                                WdFileData.append(PDAT[i][k])

                    TDATA.append(WdFileData)

            elif PDAT[i][0] == 'L':
                break

        CompWord.append('zero')
        for q in range(len(TDATA)):
            CompWord.append(TDATA[q][1])

        for i in range(len(TDATA)):
            DicWts = []
            CWord = CompWord[i] + '$'
            if re.match(CWord, TDATA[i][1]) is None:
                if TDATA[i][1] in Dics:
                    DicWts = Dics[TDATA[i][1]]
                else:
                    for j in range(DicsN - WDicsN):
                        DicWts.append(0)
                    for j in range(DicsN - WDicsN, DicsN):
                        DicWts.append(.5)

            else:
                if TDATA[i][1] in Dics:
                    for j in range(DicsN):
                        if j == DFDic:
                            DicWts.append(1)
                        elif j != DFDic:
                            DicWts.append(Dics[TDATA[i][1]][j])
                else:
                    for j in range(DicsN - WDicsN):
                        if j != DFDic:
                            DicWts.append(0)
                        else:
                            DicWts.append(1)
                    for j in range(WDicsN):
                        DicWts.append(.5)

            if re.search('\w+-$', TDATA[i][1]) is not None:
                Weights = []
                if DFDic > -1:
                    for j in range(DicsN - WDicsN):
                        if j != DFDic:
                            Weights.append(0)
                        else:
                            Weights.append(1)
                    for j in range(DicsN - WDicsN, DicsN):
                        Weights.append(.5)
                else:
                    for j in range(DicsN - WDicsN):
                        Weights.append(0)

                    for j in range(DicsN - WDicsN, DicsN):
                        Weights.append(.5)
                DicWts = Weights

            TDATA[i] = TDATA[i] + DicWts

        OCATDic = []
        Index = 0
        for Line in TDATA:
            LineDic = [Line[0], Line[2]]
            if Line[0] == Index:
                continue
            else:
                Index = Line[0]
                for i in range(3, 3 + len(DCATS) + len(OCATS)):
                    for j in range(len(OCATS)):
                        if OCATS[j] == Line[i][0]:
                            LineDic.append(Line[i][0])
                            LineDic.append(Line[i][1])
                OCATDic.append(LineDic)

        for i in range(len(TDATA)):
            print(TDATA[i][0], ',', TDATA[i][1], ',', TDATA[i][2], end=',', file=open(WRDFiles[v], 'a'))

            for j in range(3, 3 + len(CATList)):
                if TDATA[i][j][0] in OCATS:
                    print(TDATA[i][j][1], end=',', file=open(WRDFiles[v], 'a'))
            for j in range(3, 3 + len(CATList)):
                if TDATA[i][j][0] in DCATS:
                    print(TDATA[i][j][1], end=',', file=open(WRDFiles[v], 'a'))
            for j in range(3 + len(CATList), len(TDATA[i])):
                print(TDATA[i][j], end=',', file=open(WRDFiles[v], 'a'))
            print('', file=open(WRDFiles[v], 'a'))

        SMTFDATA = []
        for i in range(1, TurnN + 1):
            for j in range(len(DCATS)):
                SMTDATA = [i, DCATS[j]]
                Switch = 0
                TSpkr = 0
                for m in range(len(TDATA)):
                    if TDATA[m][0] < i:
                        continue
                    elif TDATA[m][0] == i:
                        if Switch == 0:
                            TSpkr = TDATA[m][2]
                            SMTDATA.append(TSpkr)
                            Switch = 1
                        if Switch == 1:
                            if TDATA[m][2] != TSpkr:
                                print('Inconsistent Speakers at TDATA[', m, ']')
                            elif TDATA[m][2] == TSpkr:
                                for q in range(3, 3 + len(CATList)):
                                    if DCATS[j] in TDATA[m][q]:
                                        SMTDATA.append(TDATA[m][q][1])
                    elif TDATA[m][0] > i:
                        break
                SMTFDATA.append(SMTDATA)

            for j in range(len(DicFiles)):
                SMTDATA = [i, DicFiles[j]]
                Switch = 0
                TSpkr = 0
                for m in range(len(TDATA)):
                    if TDATA[m][0] < i:
                        continue
                    elif TDATA[m][0] == i:
                        if Switch == 0:
                            TSpkr = TDATA[m][2]
                            SMTDATA.append(TSpkr)
                            SMTDATA.append(TDATA[m][3 + len(DCATS) + len(OCATS) + j])
                            Switch = 1
                        elif Switch == 1:
                            if TDATA[m][2] != TSpkr:
                                print('Inconsistent Speakers at TDATA[', m, ']')
                            elif TDATA[m][2] == TSpkr:
                                SMTDATA.append(TDATA[m][3 + len(DCATS) + len(OCATS) + j])
                    elif TDATA[m][0] > i:
                        break
                SMTFDATA.append(SMTDATA)

        SMT = []
        for i in range(len(SMTFDATA)):
            SMTDAT = [SMTFDATA[i][0], SMTFDATA[i][2], SMTFDATA[i][1]]
            NewList = SMTFDATA[i][3:]
            SMTD = smth(NewList)
            SMTDAT = SMTDAT + SMTD
            SMT.append(SMTDAT)
        SMTT = []
        LocWd = 0

        for i in range(len(TDATA)):
            Row = [TDATA[i][0], TDATA[i][1], TDATA[i][2]]
            if i > 0:
                if TDATA[i][0] > TDATA[i - 1][0]:
                    LocWd = 0
                else:
                    LocWd += 1
            for j in range(len(TDics)):
                for k in range(len(SMT)):

                    if SMT[k][0] < TDATA[i][0]:
                        continue
                    elif SMT[k][0] == TDATA[i][0]:
                        if SMT[k][2] == TDics[j]:
                            Row.append(SMT[k][3 + LocWd])
                    elif SMT[k][0] > TDATA[i][0]:
                        break
            SMTT.append(Row)

        LocSpkr = 0
        Turn = 1
        for i in range(len(SMTT)):
            if SMTT[i][0] != Turn:
                if SMTT[i][2] == LocSpkr:
                    print('', file=open(SMTFiles[v], 'a'))
                    Turn == SMTT[i][0]
            Turn = SMTT[i][0]
            LocSpkr = int(SMTT[i][2])
            print(SMTT[i][1], end=',', file=open(SMTFiles[v], 'a'))
            for j in range(LocSpkr - 1):
                for k in range(len(TDics)):
                    print(',', end='', file=open(SMTFiles[v], 'a'))
            for j in range(3, len(SMTT[i])):
                print(SMTT[i][j], end=',', file=open(SMTFiles[v], 'a'))
            print('', file=open(SMTFiles[v], 'a'))

        print('File,Turn,Spkr', end=',', file=open(RAWTRNFile, 'a'))
        print('File,Turn,Spkr', end=',', file=open(SMTTRNFile, 'a'))
        for cat in OCATS:
            print(cat, end=',', file=open(RAWTRNFile, 'a'))
            print(cat, end=',', file=open(SMTTRNFile, 'a'))
        print('Words', end=',', file=open(RAWTRNFile, 'a'))
        print('Words', end=',', file=open(SMTTRNFile, 'a'))
        for i in range(len(DicFiles)):
            if DicFiles[i] not in WDic:
                print(DicFiles[i], 'Match,', DicFiles[i], 'Coverage,', DicFiles[i], 'ODDS', end=',',
                      file=open(RAWTRNFile, 'a'))
            else:
                print(DicFiles[i], 'Match,', DicFiles[i], 'Coverage', end=',', file=open(RAWTRNFile, 'a'))
                print(DicFiles[i], 'Pos Match,', DicFiles[i], 'Pos Prop', end=',', file=open(RAWTRNFile, 'a'))
        for i in range(len(TDics)):
            print(TDics[i], 'Mean,', TDics[i], 'SD', end=',', file=open(SMTTRNFile, 'a'))
        for i in range(len(WDic)):
            print(WDic[i], 'MHigh,', WDic[i], 'HighProp', end=',', file=open(SMTTRNFile, 'a'))
        for i in range(len(TDics)):
            for j in range(i + 1, len(TDics)):
                print(TDics[i], '_', TDics[j], end=',', file=open(SMTTRNFile, 'a'))

        print('\n', file=open(RAWTRNFile, 'a'))
        print('\n', file=open(SMTTRNFile, 'a'))

        TurnProp = []
        for i in range(1, TurnN + 1):
            Check = 0
            print(TxtFiles[v], ',', i, end=',', file=open(RAWTRNFile, 'a'))
            Words = 0
            for j in range(len(TDATA)):
                if TDATA[j][0] < i:
                    continue
                elif TDATA[j][0] == i:
                    if Check == 0:
                        print(TDATA[j][2], end=',', file=open(RAWTRNFile, 'a'))  # Speaker
                        for cat in OCATS:
                            for m in range(3, 3 + len(OCATS) + len(DCATS)):
                                if TDATA[j][m][0] == cat:
                                    print(TDATA[j][m][1], end=',', file=open(RAWTRNFile, 'a'))  # Category instance
                        Check = 1
                    else:
                        break
                else:
                    break
            for j in range(len(TDATA)):
                if TDATA[j][0] < i:
                    continue
                elif TDATA[j][0] == i:
                    Words += 1
                elif TDATA[j][0] > i:
                    break
            print(Words, end=',', file=open(RAWTRNFile, 'a'))
            for m in range(DicsN):
                Mat = 0
                PosMat = 0
                for j in range(len(TDATA)):
                    if TDATA[j][0] < i:
                        continue
                    elif TDATA[j][0] == i:
                        if TDATA[j][3 + len(OCATS) + len(DCATS) + m] != 0:
                            Mat += 1
                        if re.match('\w+.Wt', DicFiles[m]) is not None:
                            if TDATA[j][3 + len(OCATS) + len(DCATS) + m] > 0:
                                PosMat += 1
                    elif TDATA[j][0] > i:
                        break
                print(Mat, end=',', file=open(RAWTRNFile, 'a'))
                if Words > 0:
                    Cov = Mat / Words
                    NonMat = Words - Mat
                    if NonMat != 0:
                        Odds = Mat / NonMat
                    else:
                        Odds = '--'
                    if DicFiles[m] not in WDic:
                        print(Cov, ',', Odds, end=',', file=open(RAWTRNFile, 'a'))
                    else:
                        print(Cov, end=',', file=open(RAWTRNFile, 'a'))

                        if Mat != 0:
                            Prop = PosMat / Mat
                        else:
                            Prop = '--'
                        print(PosMat, ',', Prop, end=',', file=open(RAWTRNFile, 'a'))
            print('', file=open(RAWTRNFile, 'a'))

        for i in range(1, TurnN + 1):
            Check = 0
            print(TxtFiles[v], ',', i, end=',', file=open(SMTTRNFile, 'a'))

            Words = 0
            for j in range(len(TDATA)):
                if TDATA[j][0] < i:
                    continue
                elif TDATA[j][0] == i:
                    if Check == 0:
                        print(TDATA[j][2], end=',', file=open(SMTTRNFile, 'a'))
                        for cat in OCATS:
                            for m in range(3, 3 + len(OCATS) + len(DCATS)):
                                if TDATA[j][m][0] == cat:
                                    print(TDATA[j][m][1], end=',', file=open(SMTTRNFile, 'a'))
                        Check = 1
                    else:
                        break
                else:
                    break
            for j in range(len(TDATA)):
                if TDATA[j][0] < i:
                    continue
                elif TDATA[j][0] == i:
                    Words += 1
                elif TDATA[j][0] > i:
                    break
            print(Words, end=',', file=open(SMTTRNFile, 'a'))
            for j in range(len(SMT)):
                if SMT[j][0] < i:
                    continue
                elif SMT[j][0] == i:
                    for m in range(len(TDics)):
                        if SMT[j][2] == TDics[m]:
                            List = SMT[j][3:]
                            ListM = statistics.mean(List)
                            ListSD = statistics.pstdev(List)
                            print(ListM, ',', ListSD, end=',', file=open(SMTTRNFile, 'a'))
                            if TDics[m] in WDic:
                                HighN = 0
                                HighP = 0
                                HighV = 0
                                MHigh = 0
                                for q in List:
                                    if q > .5:
                                        HighN += 1
                                        HighV += q - .5
                                if HighN > 0:
                                    MHigh = HighV / HighN
                                if len(List) > 0:
                                    HighP = HighN / len(List)
                                print(MHigh, ',', HighP, end=',', file=open(SMTTRNFile, 'a'))

                else:
                    break
            for j in range(len(SMT)):
                if SMT[j][0] < i:
                    continue
                elif SMT[j][0] == i:
                    List1 = SMT[j][3:]
                    for k in range(j + 1, len(SMT)):
                        if SMT[k][0] < i:
                            continue
                        elif SMT[k][0] == i:
                            List2 = SMT[k][3:]
                            CV = covar(List1, List2)
                            print(CV, end=',', file=open(SMTTRNFile, 'a'))
                        else:
                            break
                else:
                    break

            print('', file=open(SMTTRNFile, 'a'))

        for i in range(1, 1 + len(Speakers)):
            WordNList = []
            WordN = 0
            SpkrTurnN = 0
            print(TxtFiles[v], ',', i, end=',', file=open(SMTAG0File, 'a'))
            print(TxtFiles[v], ',', i, end=',', file=open(RAWAG0File, 'a'))
            for Line in SMT:
                if Line[1] != i:
                    continue
                elif Line[1] == i:
                    if Line[2] == TDics[0]:
                        SpkrTurnN += 1
                        Wds = len(Line) - 3
                        WordNList.append(Wds)
                        WordN += Wds
            print(WordN, ',', SpkrTurnN, end=',', file=open(SMTAG0File, 'a'))
            print(WordN, ',', SpkrTurnN, end=',', file=open(RAWAG0File, 'a'))
            FirstQuartile = firstquartile(WordNList)
            Median = statistics.median(WordNList)
            ThirdQuartile = thirdquartile(WordNList)
            Mean = statistics.mean(WordNList)
            Max = max(WordNList)
            Min = min(WordNList)
            print(FirstQuartile, ',', Median, ',', ThirdQuartile, ',', Mean, ',', Max, ',', Min,
                  end=',', file=open(RAWAG0File, 'a'))

            for Dic in TDics:
                DATA = []
                HighN = 0
                HighP = 0
                HighV = 0
                MHigh = 0
                AVG = 0
                SD = 0
                for Line in SMT:
                    if Line[1] != i:
                        continue
                    elif Line[1] == i:
                        if Line[2] != Dic:
                            continue
                        elif Line[2] == Dic:
                            DATA = DATA + Line[3:]
                if Dic in WDic:
                    for q in DATA:
                        if q > .5:
                            HighN += 1
                            HighV += q - .5
                    if HighN > 0:
                        MHigh = HighV / HighN
                if len(DATA) > 0:
                    HighP = HighN / len(DATA)
                    AVG = statistics.mean(DATA)
                    SD = statistics.pstdev(DATA)

                print(AVG, ',', SD, end=',', file=open(SMTAG0File, 'a'))
                if Dic in WDic:
                    print(MHigh, ',', HighP, end=',', file=open(SMTAG0File, 'a'))
            for j in range(len(TDics)):
                for k in range(j + 1, len(TDics)):
                    DATA1 = []
                    DATA2 = []
                    CV = 0
                    for Line in SMT:
                        if Line[1] != i:
                            continue
                        elif Line[1] == i:
                            if Line[2] == TDics[j]:
                                DATA1 = DATA1 + Line[3:]
                            elif Line[2] == TDics[k]:
                                DATA2 = DATA2 + Line[3:]
                            else:
                                continue
                    if len(DATA1) != len(DATA2):
                        print('Problem with AG0 file; DATA1 and DATA2 have unequal length')
                    if len(DATA1) > 1:
                        CV = covar(DATA1, DATA2)
                    print(CV, end=',', file=open(SMTAG0File, 'a'))
            print('', file=open(SMTAG0File, 'a'))
            Prop = 0
            for m in range(DicsN - len(WDic)):
                Mat = 0
                PosMat = 0
                for j in range(len(TDATA)):
                    if TDATA[j][2] != i:
                        continue
                    elif TDATA[j][2] == i:
                        if TDATA[j][3 + len(OCATS) + len(DCATS) + m] != 0:
                            Mat += 1

                    if WordN > 0:
                        Cov = Mat / WordN
                        NonMat = WordN - Mat
                        if NonMat != 0:
                            Odds = Mat / NonMat
                        else:
                            Odds = '--'
                print(Mat, ',', Cov, ',', Odds, end=',', file=open(RAWAG0File, 'a'))

            for m in range(len(WDic)):
                for j in range(len(TDATA)):
                    if TDATA[j][2] == i:
                        if TDATA[j][3 + len(OCATS) + len(DCATS) + DicsN - len(WDic) + m] != .5:
                            Mat += 1
                        if TDATA[j][3 + len(OCATS) + len(DCATS) + DicsN - len(WDic) + m] > .5:
                            PosMat += 1
                if WordN > 0:
                    Cov = Mat / WordN
                if Mat != 0:
                    Prop = PosMat / Mat
                else:
                    Prop = '--'
                print(Mat, ',', Cov, ',', PosMat, ',', Prop, end=',', file=open(RAWAG0File, 'a'))

            print('', file=open(RAWAG0File, 'a'))

        ListIndx = []
        for i in range(1, TurnN + 1):
            ListIndx.append(0)
        for i in range(len(ListIndx)):
            NewIndx = i + 1
            if ListIndx[i] == 1:
                continue
            elif ListIndx[i] == 0:
                CVDATA = []
                CVIndex = []
                ListIndx[i] = 1
                AG1Turn = [NewIndx]
                Spkr = OCATDic[i][1]
                Wd = len(SMT[i]) - 3
                Turns = 1
                Words = Wd
                print(TxtFiles[v], ',', Spkr, end=',', file=open(SMTAG1File, 'a'))
                print(TxtFiles[v], ',', Spkr, end=',', file=open(RAWAG1File, 'a'))
                CatComp = OCATDic[i][2:]
                for j in range(len(CatComp)):
                    if j % 2 == 1:
                        print(CatComp[j], end=',', file=open(SMTAG1File, 'a'))
                        print(CatComp[j], end=',', file=open(RAWAG1File, 'a'))

                for j in range(i + 1, len(OCATDic)):
                    if ListIndx[j] == 1:
                        continue
                    elif ListIndx[j] == 0:
                        if OCATDic[j][1] == Spkr:
                            NewComp = OCATDic[j][2:]
                            if NewComp == CatComp:
                                Indx = j + 1
                                AG1Turn.append(Indx)
                                ListIndx[j] = 1
                Words = 0
                for m in range(len(AG1Turn)):
                    Turn = AG1Turn[m]
                    for q in range(len(TDATA)):
                        if TDATA[q][0] == Turn:
                            Words += 1
                print(Words, ',', len(AG1Turn), end=',', file=open(SMTAG1File, 'a'))
                print(Words, ',', len(AG1Turn), end=',', file=open(RAWAG1File, 'a'))

                for s in range(DicsN):

                    Mat = 0
                    PosMat = 0
                    PosProp = 0
                    for m in range(len(AG1Turn)):
                        Turn = AG1Turn[m]
                        for q in range(len(TDATA)):
                            if TDATA[q][0] == Turn:
                                if DicFiles[s] not in WDic:
                                    if TDATA[q][3 + len(OCATS) + len(DCATS) + s] != 0:
                                        Mat += 1
                                elif DicFiles[s] in WDic:
                                    if TDATA[q][3 + len(OCATS) + len(DCATS) + s] != .5:
                                        Mat += 1
                                    if float(TDATA[q][3 + len(OCATS) + len(DCATS) + s]) > .5:
                                        PosMat += 1
                    Coverage = 0
                    Odds = 0
                    if Words > 0:
                        Coverage = Mat / Words
                    NonMat = Words - Mat
                    if NonMat != 0:
                        Odds = Mat / NonMat
                    else:
                        Odds = '--'
                    if DicFiles[s] not in WDic:
                        print(Mat, ',', Coverage, ',', Odds, end=',', file=open(RAWAG1File, 'a'))
                    else:
                        print(Mat, ',', Coverage, end=',', file=open(RAWAG1File, 'a'))
                        PosProp = 0
                        if Mat > 0:
                            PosProp = PosMat / Mat
                        else:
                            PosProp = '--'
                        print(PosMat, ',', PosProp, end=',', file=open(RAWAG1File, 'a'))
                print('', file=open(RAWAG1File, 'a'))

                for k in range(len(TDics)):
                    SDATA = []
                    HighN = 0
                    HighV = 0
                    MHigh = 0
                    HighP = 0
                    for m in range(len(AG1Turn)):
                        for q in range(len(SMT)):
                            if SMT[q][0] < AG1Turn[m]:
                                continue
                            elif SMT[q][0] == AG1Turn[m]:
                                if SMT[q][2] == TDics[k]:
                                    SMTs = SMT[q][3:]
                                    SDATA = SDATA + SMTs

                    Mean = statistics.mean(SDATA)
                    SD = statistics.pstdev(SDATA)
                    CVDATA.append(SDATA)
                    print(Mean, ',', SD, end=',', file=open(SMTAG1File, 'a'))
                    if TDics[k] in WDic:
                        for q in SDATA:
                            if q > .5:
                                HighN += 1
                                HighV += q - .5
                        if HighN > 0:
                            MHigh = HighV / HighN
                        if len(SDATA) > 0:
                            HighP = HighN / len(SDATA)
                        print(MHigh, ',', HighP, end=',', file=open(SMTAG1File, 'a'))
                for k in range(len(CVDATA)):
                    for m in range(k + 1, len(CVDATA)):
                        CoVar = covar(CVDATA[k], CVDATA[m])
                        print(CoVar, end=',', file=open(SMTAG1File, 'a'))
                print('', file=open(SMTAG1File, 'a'))

        ListIndx = []
        for i in range(1, TurnN + 1):
            ListIndx.append(0)
        for i in range(len(ListIndx)):
            NewIndx = i + 1
            if ListIndx[i] == 1:
                continue
            elif ListIndx[i] == 0:
                CVDATA = []
                CVIndex = []
                ListIndx[i] = 1
                AG2Turn = [NewIndx]
                Spkr = OCATDic[i][1]
                Wd = len(SMT[i]) - 3
                Turns = 1
                Words = Wd
                print(TxtFiles[v], ',', Spkr, end=',', file=open(SMTAG2File, 'a'))
                print(TxtFiles[v], ',', Spkr, end=',', file=open(RAWAG2File, 'a'))
                CatComp = OCATDic[i][2:]
                NewCatComp = []
                for j in range(len(CatComp)):
                    if j % 2 == 0:
                        NewCatComp.append(CatComp[j])
                        if CatComp[j] in ACATS:
                            NewCatComp.append('--')
                        else:
                            NewCatComp.append(CatComp[j + 1])
                for j in range(len(NewCatComp)):
                    if j % 2 == 1:
                        print(NewCatComp[j], end=',', file=open(SMTAG2File, 'a'))
                        print(NewCatComp[j], end=',', file=open(RAWAG2File, 'a'))
                for j in range(i + 1, len(OCATDic)):
                    if ListIndx[j] == 1:
                        continue
                    elif ListIndx[j] == 0:
                        if OCATDic[j][1] == Spkr:
                            NextCatComp = OCATDic[j][2:]
                            NewNewCatComp = []
                            for k in range(len(NextCatComp)):
                                if k % 2 == 0:
                                    NewNewCatComp.append(NextCatComp[k])
                                    if NextCatComp[k] in ACATS:
                                        NewNewCatComp.append('--')
                                    else:
                                        NewNewCatComp.append(NextCatComp[k + 1])

                            if NewNewCatComp == NewCatComp:
                                Indx = j + 1
                                AG2Turn.append(Indx)
                                ListIndx[j] = 1
                Words = 0
                for m in range(len(AG2Turn)):
                    Turn = AG2Turn[m]
                    for q in range(len(TDATA)):
                        if TDATA[q][0] == Turn:
                            Words += 1
                print(Words, ',', len(AG2Turn), end=',', file=open(SMTAG2File, 'a'))
                print(Words, ',', len(AG2Turn), end=',', file=open(RAWAG2File, 'a'))

                for s in range(len(TDics) - len(DCATS)):
                    Mat = 0
                    PosMat = 0
                    PosProp = 0
                    for m in range(len(AG2Turn)):
                        Turn = AG2Turn[m]
                        for q in range(len(TDATA)):
                            if TDATA[q][0] == Turn:
                                if DicFiles[s] not in WDic:
                                    if TDATA[q][3 + len(OCATS) + len(DCATS) + s] != 0:
                                        Mat += 1
                                elif DicFiles[s] in WDic:
                                    if TDATA[q][3 + len(OCATS) + len(DCATS) + s] != .5:
                                        Mat += 1
                                    if float(TDATA[q][3 + len(OCATS) + len(DCATS) + s]) > .5:
                                        PosMat += 1
                    Coverage = 0
                    Odds = 0
                    if Words > 0:
                        Coverage = Mat / Words
                    NonMat = Words - Mat
                    if NonMat != 0:
                        Odds = Mat / NonMat
                    else:
                        Odds = '--'
                    if DicFiles[s] not in WDic:
                        print(Mat, ',', Coverage, ',', Odds, end=',', file=open(RAWAG2File, 'a'))
                    else:
                        print(Mat, ',', Coverage, end=',', file=open(RAWAG2File, 'a'))
                        PosProp = 0
                        if Mat > 0:
                            PosProp = PosMat / Mat
                        else:
                            PosProp = '--'
                        print(PosMat, ',', PosProp, end=',', file=open(RAWAG2File, 'a'))
                print('', file=open(RAWAG2File, 'a'))

                for k in range(len(TDics)):
                    SDATA = []
                    HighN = 0
                    HighV = 0
                    HighP = 0
                    MHigh = 0
                    for m in range(len(AG2Turn)):
                        for q in range(len(SMT)):
                            if SMT[q][0] < AG2Turn[m]:
                                continue
                            elif SMT[q][0] == AG2Turn[m]:
                                if SMT[q][2] == TDics[k]:
                                    SMTs = SMT[q][3:]
                                    SDATA = SDATA + SMTs

                    Mean = statistics.mean(SDATA)
                    SD = statistics.pstdev(SDATA)
                    CVDATA.append(SDATA)
                    print(Mean, ',', SD, end=',', file=open(SMTAG2File, 'a'))

                    if TDics[k] in WDic:
                        for q in SDATA:
                            if q > .5:
                                HighN += 1
                                HighV += q - .5
                        if HighN > 0:
                            MHigh = HighV / HighN
                        if len(SDATA) > 0:
                            HighP = HighN / len(SDATA)
                        print(MHigh, ',', HighP, end=',', file=open(SMTAG2File, 'a'))

                for k in range(len(CVDATA)):
                    for m in range(k + 1, len(CVDATA)):
                        CoVar = covar(CVDATA[k], CVDATA[m])
                        print(CoVar, end=',', file=open(SMTAG2File, 'a'))
                print('', file=open(SMTAG2File, 'a'))

GTypes = []
for i in range(len(GSpeakers)):
        GTTList = {}
        GLTTList = []
        for item in TTGList[i]:
            word = item[0]
            freq = item[1]
            if word in GTTList:
                GTTList[word] += freq
            else:
                GTTList[word] = freq
        for word in GTTList:
            ListItem = (word, GTTList[word])
            GLTTList.append(ListItem)
            if word not in GTypes and word not in Dics and word not in ListLOL:
                if re.match('\w+-', word) is None:
                    GTypes.append(word)

        GLSTTList = sorted(GLTTList, key=itemgetter(0))
        Spkr = i + 1
        print('\nSpeaker = ', Spkr, '\n', file=open(TTGFile, 'a'))
        Types = len(GLSTTList)
        Tokens = 0
        TTR = 0
        for j in range(len(GLSTTList)):
            print(GLSTTList[j][0], ',', GLSTTList[j][1], file=open(TTGFile, 'a'))
            Tokens += GLSTTList[j][1]
        if Tokens > 0:
            TTR = Types / Tokens
        print('Types = ', Types, '; ', ' Tokens = ', Tokens, '; ' 'Ratio = ', TTR, file=open(TTGFile, 'a'))

GTypes = sorted(GTypes)
for word in GTypes:
    print(word, file=open(LOLFile, 'a'))
