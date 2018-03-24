import json
import numpy as np
import unidecode
import random as random

data = json.load(open('data.txt', encoding='utf8'))



tags=["arts de la rue","autres","chansons / variétés","cirque / magie","danse","humour / café-théâtre","musique classique / opéra"
    "musique du monde","musique hip-hop / rnb / soul","musique jazz / blues / reggae","musique pop / rock / electro",
    "pluridisciplinaire","spectacle jeunesse","spectacle musical / cabaret / opérette","théâtre",
    "cinéma","livre","musée","exposition","conférence","visite"]


tags_sec=["asiatique","france","anglo-saxon","hispanique","germanique","africain","classique",
    "baroque","impressionniste","moderne","photographie"]


tags_related_p=[["rue","tag","bansky","graffiti","street"],["autre"],["chant","chanson","variete","populaire","hallyday","gainsbourg","voix"],
["cirque","magie","carte","clown","acrobate","elephant"],["danse","ballet","tango","salsa","danseur","danseuse","bastille","garnier"],
["humour","cafe","virgule","drole","amusant"],["classique","opera","orchestre","bastille","garnier","chatelet","sonate","concerto","symphonie"],
["monde","musique"],["hip","hop","rnb","soul","musique","rap"],["jazz","blues","reggae","musique","jams"],
["pop","rock","electro","techno","guitare","idole","acid"],
["pluridisciplinaire"],["spectacle" ,"jeune","jeunesse","enfant","petit","educatif"],
["spectacle","musique","cabaret","operette","moulin"],
["theatre","piece","acteur","actrice","planche"],
["cinema","écran","film","directeur"],["livre","librairie","poeme","poesie","ecriture"],
["musee","peintre","peinture","sculpteur","sculpture","louvre","orsay","guimet","branly","beaubourg","pompidou"],
["exposition","peintre","peinture","sculpteur","sculpture","louvre","orsay","guimet","branly","beaubourg","pompidou"],
["conference","ted"],["visite"]]

tags_related_s=[["asiatique","asie","chine","japon","corée","calligraphie","guimet"],[],["londres","anglais","angleterre","irlande","ecosse","etats-unis","usa","us","britannique","anglo-saxon"],
["hispanique","espagne","portugal","italie","hiberique"],["germanique","allemagne","autriche","allemand","berlin"],["africain","afrique","branly"],
["classique","classiscisme"],["baroque","velasquez","clair-obscur","caravage","cortona"],["impressionniste","impressionnisme","monet","renoir","degas","manet","cezanne"],
["moderne","pop-art","picasso","dali","warhol"],["photographie"]]


def normalize(u):
    norme = 0
    n = len(u)
    m = len(u[0])
    for i in range(n):
        for j in range(m):
            norme += u[i][j]
    for i in range(n):
        for j in range(m):
            if(norme !=0):
                u[i][j] *= (1/norme)
    return u


def normalize_offer(n):
    words=data['offers'][str(n)]["title"].replace("'"," ").replace("."," ").lower().split()+\
    data['offers'][str(n)]["description"].replace("'"," ").replace("."," ").lower().split()+\
    data['offers'][str(n)]["location"].replace("'"," ").replace("."," ").lower().split()
    words_clean=[]
    for i  in range(len(words)):
        words[i] = unidecode.unidecode(words[i])
        w=""
        for j in words[i]:
            if 97<=ord(j) and ord(j)<=122:
                w+=j
        if(len(w)>2):
            words_clean.append(w)

    return words_clean

def analyze_offer_princ(n):
    words=normalize_offer(n)
    pref=[0]*len(tags)
    for i in range(len(tags)):
        for w in words:
            pref[i]+=tags_related_p[i].count(w)
    return pref

def analyze_offer_sec(n):
    words=normalize_offer(n)
    pref=[0]*len(tags_sec)
    for i in range(len(tags_sec)):
        for w in words:
            pref[i]+=tags_related_s[i].count(w)
    return pref

def verif():
    r=0
    i=0
    while i<400:
        if analyze_offer_princ(i)!=[0]*20:
            r+=1
        i+=1
        
    print(r)

def matrice_pref(n):
    tagsP = analyze_offer_princ(n)
    tagsS = analyze_offer_sec(n)
    #nombre de colonnes
    N = len(tags)
    #nombre de lignes
    M = len(tags_sec)
    matrice = np.zeros((M,N))
    for i in range(N):
        if (tagsP[i] != 0):
            for j in range(M):
                if (tagsS[j] != 0):
                    matrice[j][i] = tagsS[j] + tagsP[i]
                else:
                    matrice[1][i] = tagsP[i]
    return normalize(matrice)


def update_data(n):
    mat=matrice_pref(n).tolist()
    data['offers'][str(n)]['preference']=mat

def update_all_data():
    for i in range(len(data['offers'])):
        update_data(i)

def update_json():
    with open('data_mat.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    
