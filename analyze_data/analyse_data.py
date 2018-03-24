import json

import unidecode

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
