import json

import unidecode

data = json.load(open('data.txt', encoding='utf8'))


#returns the occurence of the word "word" in the title, the description or the location of the nth offer
def word_in_offer(word, n):
    r=0
    words=data['offers'][str(n)]["title"].replace("'"," ").lower().split()+\
    data['offers'][str(n)]["description"].replace("'"," ").lower().split()+\
    data['offers'][str(n)]["location"].replace("'"," ").lower().split()
    words_clean=[]
    for i  in range(len(words)):
        words[i] = unidecode.unidecode(words[i])
        w=""
        for j in words[i]:
            if 97<=ord(j) and ord(j)<=122:
                w+=j
        if(len(w)>2):
            words_clean.append(w)

    return words_clean.count(word)
                
