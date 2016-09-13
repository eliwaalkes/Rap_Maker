import urllib.request
import re
from nltk.tokenize import RegexpTokenizer
import pickle
import nltk
import random
import os
import operator
import codecs


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

def load_object(obj):
    file = open(obj, 'rb')
    return pickle.load(file)

def edit_text(name):
    bad = "\" ' ` 1 2 3 4 5 6 7 8 9 0 - = ~ ! @ # $ % ^ & * ( ) _ + { } [ ] : ; , . ? /"
    dict = {}
    for i in bad.split(" "):
        dict[i] = ""

    file = codecs.open(name, encoding="utf-8", mode="r")
    file2 = open(name + " v2", "a+")
    data = file.read()

    for i,j in dict.items():
        data = data.replace(i, j)

    file.close()
    file2.write(data)
    file2.close()

    return

def make_list(name):
    file = open(name + " v2", "r")
    data = file.read().replace("\n", "").split(" ")
    lst = []
    for i in data:
        if i not in lst:
            lst.append(i)

    file.close()

    st = set(lst)
    save_object(st, name[:-6] + " Wordset")

    return

def all_wordlists():
    for j in ["JayZLyrics", "BiggieLyrics", "2PacLyrics", "KanyeLyrics"]:
        make_list(j)

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
    #print(lineList[:20])
    return lineList

def create_dict_pt1(lineList, num, name):
    big_dict = {}
    for i in lineList:
        j = i[num-1]
        if j in big_dict:
            if i[:num - 1] not in big_dict[j].dict:
                big_dict[j].dict[i[:num - 1]] = 1
            else:
                big_dict[j].dict[i[:num - 1]] += 1
        else:
            tempDict = {}
            tempDict[i[:num - 1]] = 1
            rapDict = make_rapDict(j, tempDict)
            big_dict[j] = rapDict

    save_object(big_dict, name + "Dictionary " + str(num))

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


def bar_writing(word1, num, rapper):
    dic = load_object(rapper + "Dictionary " + str(num))
    #st = load_object(rapper + " Wordset")
    final = ""
    current_search = word1

    #change max to sorted and then go to next if it doesnt work fdsa fsafknlsdafnfdsafdsm hg gdhj
    for i in range(0,2):
        tup = max(dic[current_search].dict.items(), key=operator.itemgetter(1))[0]
        strTup = " ".join(tup)
        final = strTup + " " + final
        current_search = tup[0]

    final += word1

    return final

def write_rap(lst, num, rapper):
    final = ""
    for i in lst:
        final = final + bar_writing(i, num, rapper) + "\n"
        final = final + write_rhyme_line(i, num, rapper) + "\n"
    print(final)

def write_rhyme_line(rhyme, num, rapper):
    #dic = load_object(rapper + "Dictionary " + str(num))
    lst = load_object(rapper + " Wordset")
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == rhyme]
    rhymes = []

    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-2:] == syllable[-2:]]

    #print(str(rhymes))
    while True:
        rym = random.choice(rhymes)
        if (rym in lst) and (rym != rhyme):
            break
        else:
            rym = random.choice(rhymes)

    return bar_writing(rym, num, rapper)

def make_dicts():
    #for j in ["JayZLyrics", "BiggieLyrics", "2PacLyrics", "KanyeLyrics"]:
        for i in range(2,9):
            create_dict_pt1(create_list("KanyeLyrics v2", i), i, "Kanye")

#make_dicts()

def user_interaction():
    rapper = ""
    while True:
        choice = input("Type either Jay-Z, Biggie, 2pac, or Kanye: ")
        if (choice[0].lower() == "j"):
            rapper = "JayZ"
            break
        elif (choice[0].lower() == "b"):
            rapper = "Biggie"
            break
        elif (choice[0].lower() == "k"):
            rapper = "Kanye"
            break
        elif (choice[0].lower() == "t") or (choice[0].lower() == "2"):
            rapper = "2Pac"
            break
        else:
            print("I didn't recognize that, please try again")

    wordset = load_object(rapper + " Wordset")

    while True:
        word = input("You chose " + rapper + " now type the words you want to have rhymed: ")
        words = word.lower().split(" ")
        wrongWords = []
        for x in words:
            if x not in wordset:
                wrongWords.append(x)

        if len(wrongWords) != 0:
            print("Sorry, \"" + wrongWords[0] + "\" is not in " + rapper + "'s vocab, try again with a new word: ")
        if len(wrongWords) == 0:
            break

    print("\n\n")
    write_rap(words, 4, rapper)

    return

user_interaction()
#print("slept" in load_object("Kanye Wordset"))
#print(str(load_object("KanyeDictionary 4")["slept"].dict))

#print(len(load_object("KanyeDictionary 2")))
#user_interaction()
#nltk.download()