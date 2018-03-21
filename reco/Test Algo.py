import random as rd

tags=["Théâtre", "Cinéma", "Classique", "Musique", "Opéra", "Concert", "Exposition", "Musée", "Science-fiction","Livre"]



def db_alea(n,nbtags):
    dba=[[]]*n
    for i in range(n):
        dba[i]=gen_alea(nbtags)
    return dba


def gen_alea(nbtags):
    res=[0]*nbtags
    for i in range(nbtags):
        res[i]=rd.random()
    return [normalize(res)]

def normalize(u):
    norme = sum(u)
    return [u[i]/norme for i in range(len(u))]
