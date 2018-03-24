import json

import unidecode

data = json.load(open('data.txt', encoding='utf8'))



tags=["arts de la rue","autres","chansons / variétés","cirque / magie","danse","humour / café-théâtre","musique classique / opéra"
    "musique du monde","musique hip-hop / rnb / soul","musique jazz / blues / reggae","musique pop / rock / electro",
    "pluridisciplinaire","spectacle jeunesse","spectacle musical / cabaret / opérette","théâtre",
    "cinéma","livre","musée","exposition","conférence","visite"]


tags_sec=["asiatique","france","anglo-saxon","hispanique","germanique","africain","classique",
    "baroque","impressionniste","moderne","photographie"]


tags_related_p=[["rue"],["autre"],["chant","chanson","variete"],["cirque","magie"],["danse"],["humour","cafe"],["classique","opera"],
    ["monde","musique"],["hip","hop","rnb","soul","musique"],["jazz","blues","reggae","musique"],["pop","rock","electro"],
    ["pluridisciplinaire"],["spectacle" ,"jeune"],["spectacle","musique","cabaret","operette"],["theatre"],
    ["cinema"],["livre"],["musee"],["exposition"],["conference"],["visite"]]

tags_related_s=[["asiatique","asie","chine","japon","corée","caligraphie","guimet"],[],["londres","anglais","angleterre","irlande","ecosse","etats-unis","usa","us","britannique","anglo-saxon"],
["hispanique","espagne","portugal","italie","hiberique"],["germanique","allemagne","autriche","allemand","berlin"],["africain","afrique","branly"],
["classique","classiscisme"],["baroque","velasquez","clair-obscur","caravage","cortona"],["impressionniste","impressionnisme","monet","renoir","degas","manet","cezanne"],
["moderne","pop-art","picasso","dali","warhol"],["photographie"]]



def normalize_offer(n):
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
    pref=[0]*len(tags)
    for i in range(len(tags)):
        for w in words:
            pref[i]+=tags_related_s[i].count(w)
    return pref
