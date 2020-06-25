import pandas as pd
import math
import time
import sys

#df is the dataframe of tweets
def makeStringArrFromDF(df):
    temp = []
    for tw in df['Tweet']:
        temp.append(tw.replace(' ','').lower())
    return temp

#s is the empty string to create the concatenated tweet string
#arr is the array of tweet strings
def makeStringFromArr(s, arr):
    return s.join(arr)

#arr is the string arr
#s is the string of all tweets concatenated
def makePlaceArrfromArr(arr, s):
    placeArr = [0] * len(s)
    placeInd = 0
    for i in range(len(arr)):
        holdLength = len(arr[i])
        for j in range(holdLength):
            placeArr[placeInd] = i
            placeInd += 1
    
    return placeArr

#s is the string of all tweets concatenated
def convertLetters(s):
    keys = [chr(l) for l in range(97, 123)]
    keys.append('other')
    keys.insert(0, '$')
    vals = [i for i in range(0,28)]
    conv = dict(zip(keys,vals))
    convS = []
    for lett in s:
        try:
            convS.append(conv[lett.lower()])
        except:
            convS.append(conv['other'])
    return convS

#s is an array of converted characters
def convertBack(s):
    keys = [chr(l) for l in range(97, 123)]
    keys.append('other')
    keys.insert(0, '$')
    vals = [i for i in range(0,28)]
    conv = dict(zip(vals, keys))
    convS = []
    for lett in s:
        try:
            convS.append(conv[lett])
        except:
            convS.append(conv['other'])
    return convS

#s is an array of converted characters
def suffixArray(s):
    iters = math.ceil(math.log(len(s), 2))
    places = [i for i in range(len(s))]
    comp = [0] * len(s)
    
    for i in range(iters):
        print(i)
        places.sort(key = lambda n: s[n])
        s.sort()
        comp[places[0]] = 0
        
        for j in range(1, len(s)):
            comp[places[j]] = comp[places[j - 1]]
            if s[j-1] != s[j]:
                comp[places[j]] += 1
    
        for k in range(len(s)):
            s[k] = (comp[k], comp[(k + 2**i) % len(s)])

    return places

#sa is a suffix array
def makeBWT(sa):
    bwt = []
    for i in range(len(sa)):
        bwt.append((sa[i] - 1) % len(sa))
    return bwt

#s is an array of converted characters
def findUniqueChars(s):
    sets = set(s)
    uniqueChars = list(sets)
    uniqueChars.sort()
    return uniqueChars
    
#ns is a bwt or sa
#ogs is the array of originally converted characters
def sabwtToIntStr(ns, ogs):
    new = []
    for i in range(len(ns)):
        
        new.append(ogs[ns[i]])
    return new

#bwt is the bwt array
#uniqueChars is the array unique characters in the original s
def computeC(bwt, uniqueChars):
    cPrev = [0] * len(uniqueChars)
    inds = [i for i in range(len(uniqueChars))]
    charToInd = dict(zip(uniqueChars, inds))
    for ch in bwt:
        cPrev[charToInd[ch]] += 1
    c = [0] * len(uniqueChars)
    for i in range(1, len(uniqueChars)):
        c[i] = sum(cPrev[0:i])
    return c

#bwt is the bwt array
#uniqueChars is the array of unique characters in the original s
def computeOcc(bwt, uniqueChars):
    currIter = [0] * len(uniqueChars)
    occ = []
    
    inds = [i for i in range(len(uniqueChars))]
    charToInd = dict(zip(uniqueChars, inds))
    occ.append([0] * len(uniqueChars))
    for i in range(len(bwt)):
        currIter[charToInd[bwt[i]]] += 1
        occ.append(list(currIter))
    return occ

#bwt is the bwt array
#p is the pattern array
#c is the c array
#occ is the occ array
#uniqueChars is the array of unique characters in the original s
def findPattern(bwt, p, c, occ, uniqueChars):
    i = 0
    j = len(bwt) - 1
    k = len(p) - 1
    inds = [i for i in range(len(uniqueChars))]
    charToInd = dict(zip(uniqueChars, inds))
    while k >= 0:
        i = c[charToInd[p[k]]] + occ[i][charToInd[p[k]]] #extractFromOcc(occ, i, p[k]) - 1
        j = c[charToInd[p[k]]] + occ[j][charToInd[p[k]]] #extractFromOcc(occ, j, p[k]) - 1
        if i > j:
            return None
        else:
            k -= 1
    return (i, j - 1)

#tweetNums is the placement of each character of a tweet
#places is the sa placement change from the suffix array function
def tweetNumber(tweetNums, places):
    #remember places includes $
    mapPlaces = [0] * len(tweetNums)
    for i in range(len(places)):
        mapPlaces[i] = tweetNums[places[i]]
    
    return mapPlaces

def findWhichTweetSearch(rearTweets, bwt, c, occ, unique):
    repeat = input("Do you want to search for a term? (True or False):")
    if repeat == 'True':
        repeat = True
    else:
        repeat = False
    while repeat == True:
        pat = input("Which phrase would you like to search for? ")
        prim = time.perf_counter()
        pat = convertLetters(pat)
        location = findPattern(bwt, pat, c, occ, unique)
        sec = time.perf_counter()
        if location == None:
            print("Couldn't find term")
        else:
            whereTweets = []
            for i in range(location[0], location[1] + 1):
                whereTweets.append(rearTweets[i])

            print("Found instances of phrase in the following tweets...")
            print(whereTweets)
            print(str(len(whereTweets)) + " tweets were found in " + str((sec - prim)) + " seconds")
        repeat = input("Would you like to search for another term? (True or False):")
        if repeat == 'True':
            repeat = True
        else:
            repeat = False

def main():
    #first we'll download the data and preprocess it
    data = pd.read_csv('training1600000processednoemoticon.csv', encoding = 'latin-1')
    data = data.rename(columns = {'0' : 'Sentiment', "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D" : 'Tweet'})
    data = data[['Sentiment', 'Tweet']]
    sentGroup = input("Which sentiment group would you like to search in?(Negative or Positive) ")

    if sentGroup == 'Negative':
        sentDf = data.loc[data['Sentiment'] == 0]
    elif sentGroup == 'Positive':
        sentDf = data.loc[data['Sentiment'] == 4]
    else:
        return "Couldn't recognize input, please submit one of the valid options and try again."

    #create sents, the string of all tweets of a sentiment and sentPlace, the array of positions for all characters
    sents = ''
    sentsArr = makeStringArrFromDF(sentDf)
    sents = makeStringFromArr(sents, sentsArr)
    sentPlace = makePlaceArrfromArr(sentsArr, sents)
    convSent = convertLetters(sents)
    convSentCopy = convSent.copy()
    unique = findUniqueChars(convSent)

    #now we'll create the sa, bwt, and bwt supplements to enable constant lookups
    #uncomment this block if you would like to run the algorithm and create the suffix array from scratch. The block also records the found suffix array as a .txt for future use
    """
    sentSAPlaces = suffixArray(convSent)
    
    with open('sa.txt', 'w') as filehandle:
        for listitem in sentSAPlaces:
            filehandle.write('%s\n' % listitem)
    
    """
    #uncomment this block if you have the suffix array from a text file and want to load it from there instead of calculating it
    sentSAPlaces = []
    with open('sa.txt', 'r') as filePlace:
        for line in filePlace:
            currentPlace = line[:-1]
            sentSAPlaces.append(int(currentPlace))
    
    rearTweets = tweetNumber(sentPlace, sentSAPlaces)
    sentBWTPlaces = makeBWT(sentSAPlaces)
    bwt = sabwtToIntStr(sentBWTPlaces, convSentCopy)
    c = computeC(bwt, unique)
    occ = computeOcc(bwt, unique)
    findWhichTweetSearch(rearTweets, bwt, c, occ, unique)

main()

