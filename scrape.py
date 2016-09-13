from bs4 import BeautifulSoup
import urllib.request
import re
from nltk.tokenize import RegexpTokenizer
import pickle
import nltk
import random
import os
import operator

#song_failed = 0
#song_tries = 0
#url_count = 0

#jayz --> jigga --> 10:15
#kanye --> kan_west --> 10:18
#2pac --> 2_pac --> 10:15
#big --> ntr_big --> 10:17

def get_individual_song_links():
    #global url_count, song_failed, song_tries
    wordStr = ""
    url = urllib.request.urlopen('http://ohhla.com/YFA_big.html').read()
    soup = BeautifulSoup(url, "html.parser")

    #count = 0
    for link in soup.find_all('a'):
        name = str(link.get('href'))
        print(name)
        if name[-4:] == '.txt' and name[10:17] == 'ntr_big':
            #print(name)
            #url_count += 1
            url2 = 'http://ohhla.com/' + name
            wordStr += get_lyrics(url2)
            #count += 1
        #if count == 10:
            #break

    file = open("BiggieLyrics", 'a+')
    file.write(wordStr)

    #file.write("\n\n song tries:" + str(song_tries) + "songs failed:" + str(song_failed) + "url count:" + str(url_count))
    file.close


def get_lyrics(url):
    #global song_tries, song_failed
    song_url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(song_url, "html.parser")
    final = ""

    if soup.find('pre') is not None:
        #song_tries += 1
        for x in soup.find('pre'):
            if x.find(']') is None:
                #song_failed += 1
                #print(x)
                break
            else:
                ind1 = x.find('Jay-Z]')+6
                #str = x[ind1:]
                str = x.lower()
                start = re.sub("(typed by.*|artist:.*|song:.*|.*jay-z\].*|\[verse.*|\[chorus.*|song:|album:.*)", "", str).replace(',', '').replace('.', '')
                nobrac = re.sub("[\(\[\{].*?[\)\]\}]", "", start)
                final = os.linesep.join([s for s in nobrac.splitlines() if s])


                #done = re.sub("\n", "", nobrac)
                #tokenizer = RegexpTokenizer(r'\w+')
                #result = tokenizer.tokenize(start)

                #^.*(typed by.*|artist:.*|song:.*|jay-z\].*|\[verse.*|\[chorus:.*|song:)\b.*$
                #^^^^ Get rid of bad stuff
                #"[\(\[\{].*?[\)\]\}]"
                #^^^^^ Get rid of stuff in parentheses


    return final

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, -1)

def generate_model2(rapper, word):
    dictList = load_object(rapper + " List and Dicts")
    gramDict = dictList[1][1]
    wordList = sorted(gramDict.items(), key=operator.itemgetter(1)) #list of [ ( (word1, word2), count = 10), ((word4,word5), count=9)) ]

    start = word
    add = ""
    lwCount = 0
    for j in range(10):

        for i in range(10):
            lastWord = start
            count = 1

            for tup in wordList:
                count += 1

                if start == tup[0][0]:
                    add += " " + tup[0][1]
                    start = tup[0][1]
                    break
                if count == len(wordList):
                    rand = random.randint(0,len(wordList)-1)
                    add += " " +  wordList[rand][0][0]
                    start = wordList[rand][0][1]
                    break

        add += write_bar2(lastWord, wordList) + "\n"

    final = word + " " + add
    print(final)


def write_bar2(x, wordList):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == x]
    rhymes = []

    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-1:] == syllable[-1:]]

    count = 0
    for tup in wordList:
        count += 1
        if x == tup[0][0] and tup[0][1] in rhymes:
            return tup[0][1]
        if count == len(wordList):
            print(x)
            return rhymes[random.randint(0,len(rhymes)-1)]




def create_bar(text, level=3):
    entries = nltk.corpus.cmudict.entries()
    inp = text.rsplit(None, 1)[-1] #last word to be rhymed
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]

def first_bar(word, text, dict):
    result = word

    max = dict_dict_max(dict[word])
    for i in range(0, 10):
        if max not in text:
            result += " " + max
            max = dict_dict_max(dict[max])
        else:
            # print("IN: " + max)
            max = dict_dict_max_next(dict[max])
            result += " " + max
    result += "\n"
    ret = [result, max, dict]

    return ret

def write_bar(list, dict):
    text = list[0]
    inp = list[1]
    dict = list[2]
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    result = text

    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-1:] == syllable[-1:]]

    rym = random.choice(rhymes)

    max = inp
    for i in range(0, 9):
        if max not in text:
            result += " " + max
            max = dict_dict_max(dict[max])
        else:
            # print("IN: " + max)
            max = dict_dict_max_next(dict[max])
            result += " " + max
    result += rym + "\n"

    return [result, max]

def create_rap(len, word):
    dictList = create_ngram_list_and_dict(2, "JayZLyrics")
    dict = dictList[1]
    start = word
    rap = ""
    for i in range(len):
        ret = first_bar(start, "", dict)
        result = write_bar(ret, dict)
        rap += result[0]
        start = result[1]
    print(rap)

def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)

def do_they_rhyme(word1, word2):
  # first, we don't want to report 'glue' and 'unglue' as rhyming words
  # those kind of rhymes are LAME
  if word1.find ( word2 ) == len(word1) - len ( word2 ):
      return False
  if word2.find ( word1 ) == len ( word2 ) - len ( word1 ):
      return False

  return word1 in rhyme ( word2, 1 )

def dict_dict_max(dict):
    max = 0
    word = ""
    for key, value in dict.items():
        if value > max:
            word = key

    return word

def dict_dict_max_next(dict):
    max = 0
    popWord = ""
    word = ""

    for key, value in dict.items():
        if value >= max:
            popWord = word
            word = key
    if popWord == "":
        keys = list(dict.keys())
        popWord = keys[random.randint(0,len(dict.keys())-1)]

    return popWord


def rap(len, word):
    rap = create_bar2(word)
    for i in range (len):
        line = create_bar2(rap)
        rap += create_bar2(line)

    print(rap)

def create_bar2(line):
    dictList = create_ngram_list_and_dict(2, "JayZLyrics")
    dict = dictList[1]

    lw = line.rsplit(None, 1)[-1]
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == lw]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-3:] == syllable[-3:]]
    rym = random.choice(rhymes) #could do for-loop to get most likely for this word give

    result = line
    max = dict_dict_max(dict[word])
    for i in range(9):
        if max not in result:
            result += " " + max
            max = dict_dict_max(dict[max])
        else:
            # print("IN: " + max)
            max = dict_dict_max_next(dict[max])
            result += " " + max
    result += rym + "\n"

    return result



def create_n_gram_list(num, file):
    ngramList = []
    with open(file, 'r') as text:
        for line in text:
            splitLine = line.split()
            lineList = list(nltk.ngrams(splitLine, num))
            ngramList += lineList
    text.close()

    '''
    test = open("NGRAMS YEEE", 'a')
    test.write(str(ngramList[0:500]))
    test.close()
    '''

    #save_object(ngramList, "Corpus " + str(num) + "-gram list")

    return ngramList

def create_n_gram_dict(num, gram):
    dict = {}
    for j in range(0, len(gram)):
        if gram[j] not in dict:
            dict[gram[j]] = 1
        else:
            dict[gram[j]] += 1
    return dict

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, -1)

def load_object(obj):
    file = open(obj, 'rb')
    return pickle.load(file)

def create_rapper_list_dict(rapper):
    dictList = []

    for i in range(1,10):
        lst = create_n_gram_list(i, rapper + "Lyrics")
        dict = create_n_gram_dict(i, lst)
        tempList = [lst,dict]
        dictList.append(tempList)

    save_object(dictList, rapper + " List and Dicts")


def test():
    listDict = load_object("Jayz List and Dicts")
    print(str(listDict[1][1]))

def dicts():
    rapperList = ["2Pac", "Biggie", "JayZ", "Kanye"]
    for i in rapperList:
        create_rapper_list_dict(i)

def first_bar_good(word):
    sentence = word
    rhyme = word
    start = word
    used_grams = []
    for i in range(0,3):
        next_gram = gram_list[0]


def create_list(file, num):
    with open(file, 'r') as text:
        lineList = []
        for line in text:
            splitLine = line.split()
            lst = list(nltk.ngrams(splitLine, num))
            lineList += lst
            #for x in lst:
                #lst2 = list(x)
                #lineList.append(lst2)
    text.close()

    return lineList

def create_dict_pt1(lineList, num):
    big_dict = {}
    for i in lineList:
        j = i[num-1]
        if j not in big_dict:
            tempDict = {}
            tempDict[i[:num-1]] = 1
            rapDict = make_rapDict(j, tempDict)
            big_dict[j] = rapDict
        else:
            if i[:3] not in big_dict[j].dict:
                big_dict[j].dict[i[:num-1]] = 1
            else:
                big_dict[j].dict[i[:num-1]] += 1

    save_object(big_dict, "Kanye Dictionary " + str(num))

    return True

class rapDict(object):
    word = ""
    dict = {}

    def __init__(self, word, dict):
        self.word = word
        self.dict = dict

    def append_dict(self, obj, tup):
        try:
            obj.dict[tup] += 1
        except KeyError:
            obj.dict[tup] =1


def make_rapDict(word, dict):
    x = rapDict(word, dict)

    return x

def append_rapDict(rapDict, tup):
    if tup in rapDict.dict:
        rapDict.dict[tup] += 1
    else:
        rapDict.dict[tup] = 1

    return dict

def bar_writing(word1, num):
    dic = load_object("Kanye Dictionary " + str(num))
    final = ""
    current_search = word1
    for i in range(0,4):
        tup = max(dic[current_search].dict.items(), key=operator.itemgetter(1))[0]
        strTup = " ".join(tup)
        final = strTup + " " + final
        current_search = tup[0]
    final += word1

    return final

def write_rap(lst, num):
    final = ""
    for i in lst:
        final = final + bar_writing(i, num) + "\n"
        final = final + write_rhyme_line(i, num) + "\n"
    print(final)

def write_rhyme_line(rhyme, num):
    dic = load_object("Kanye Dictionary " + str(num))
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == rhyme]
    rhymes = []

    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-2:] == syllable[-2:]]

    while True:
        rym = random.choice(rhymes)
        if rym == rhyme:
            rym = random.choice(rhymes)
        try:
            test = dic[rym]
            return bar_writing(rym, num)
        except KeyError:
            rym = random.choice(rhymes)

#for i in range(2,5):
#create_dict_pt1(create_list("KanyeLyrics", 5),5)

def user_interaction():
    word = input("Type the words you want to have rhymed: ")
    words = word.lower().split(" ")
    write_rap(words, 3)

    return True

user_interaction()