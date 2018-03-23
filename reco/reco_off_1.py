
from flask import current_app as app
from flask_login import current_user
from sqlalchemy.sql.expression import func

Event = app.model.Event
EventOccurence = app.model.EventOccurence
Mediation = app.model.Mediation
Offer = app.model.Offer
UserMediation = app.model.UserMediation
UserMediationOffer = app.model.UserMediationOffer
Thing = app.model.Thing

### ICI POUR DES VECTEURS

def attraction(L1,L2):
    n1 = len(L1)
    attractivite = 0
    for i in range(n1):
        attractivite += L1[i]*L2[i]
    return attractivite

def get_reco_offers(user,limit=1):
    query = Offer.query
    # REMOVE OFFERS FOR WHICH THERE IS ALREADY A MEDIATION FOR THIS USER
    print('before userMediation offers.count', query.count())
    if user.is_authenticated:
        query = query.filter(
            ~Offer.userMediationOffers.any() |\
            Offer.userMediationOffers.any(UserMediation.user != user)
        )

    # REMOVE OFFERS WITHOUT THUMBS
    print('after userMediation offers.count', query.count())
    query = query.outerjoin(Thing)\
                 .outerjoin(EventOccurence)\
                 .outerjoin(Event)\
                 .filter((Thing.thumbCount > 0) |
                         (Event.thumbCount > 0))
    print('before tri offers.count', query.count())
        if user.is_authenticated:
            best = 0
            index = 0
            n = len(query)
            L1 = user.preferences
            for i in range(n):
                L2 = offer.preferences
                if best < attraction(L1,L2):
                    best = attraction(L1,L2)
                    index = i
            Proposition = query.get(index)
            query.delete(index)
            return Proposition



### ICI POUR DES MATRICES

# def fonction phi

def attraction(M1,M2):
    n = len(M1)
    m = len(M1[0])
    Attraction = 0
    for i in range(n):
        for j in range(m):
            Attraction += M1[i][j]*M2[i][j]
    return Attraction

#def fonction Theta : pour le moment, on ne considère qu'une fonction attraction.
# on va donc la réutiliser directement

def Theta(M1,M2):
    n = len(M1)
    m = len(M1[0])
    Attraction = 0
    for i in range(n):
        for j in range(m):
            Attraction += M1[i][j]*M2[i][j]
    return Attraction

#idem pour theta:

def theta(M1,M2):
    n = len(M1)
    m = len(M1[0])
    Attraction = 0
    for i in range(n):
        for j in range(m):
            Attraction += M1[i][j]*M2[i][j]
    return Attraction

#idem pour V

def V(M1,M2):
    n = len(M1)
    m = len(M1[0])
    Attraction = 0
    for i in range(n):
        for j in range(m):
            Attraction += M1[i][j]*M2[i][j]
    return Attraction

#calcul des k plus proches

def KNU(user,k):
    KNU = []
    ensemble = []
    query = User.query
    for i in query:
        ensemble.append(attraction(user.preferences,i.preferences))
    sorted(ensemble)
    n = len(ensemble)
    for i in range(k):
        KNU.append(ensemble[n-1-i])
    return KNU

#def fonction psi (attraction 2)

def attraction2(user,offer,k):
    attraction = 0
    somme1 = 0
    somme2 = 0
    for i in KNU(user,k):
        somme1 += Theta(user.preferences,i.preferences) * attraction(i.preferences,offer.preferences)
        somme2 += Theta(user.preferences,i.preferences)
    return (somme1/somme2)

#def de la fonction delta

def Delta(user,offer,k):
    a1 = attraction(user.preferences,offer.preferences)
    a2 = attraction2(user,offer,k)
    return 1/2 * Math.abs(a1-a2)


#def ensemble I

def I(user,offer,taille):
    returnI = []
    I = []
    n = len(user.preferences)
    m = len(user.preferences[0])
    compte = -1
    for i in range(n):
        for i in range(m):
            compte += 1
            a = user.preferences[i][j] * offer.preferences[i][j]
            while compte < taille:
                I.append([a,i,j])
            I.sorted()
            if a > I[0][0]:
                I.pop(0)
                I.append([a,i,j])
            I.sorted()
    for i in range(taille):
        returnI.append([I[i][1],I[i][2]])

#def de J, intersection des I

def IS_IN(elmt,vect):
    n = len(vect)
    for i in range(n):
        if vect[i] == elmt:
            return True
    return False


def J(user,offer,j,taille):
    KNU = KNU(user,taille)
    J = I(KNU[0],offer,taille)
    n = len(KNU)
    for j in range(1,n):
        I = I(KNU[i],offer,taille)
        p = len(I)
        for k in range(p):
            if IS_IN(I[k],J) == False:
                I.pop(k)
    return J


def IS_EMPTY(vect):
    return (len(vect) == 0)

### Comment faire evoluer la matrice des preferences d'une nouvelle façon

def modif_pref(user):
    query = Offer.query
    # REMOVE OFFERS FOR WHICH THERE IS ALREADY A MEDIATION FOR THIS USER
    print('before userMediation offers.count', query.count())
    if user.is_authenticated:
        query = query.filter(
            ~Offer.userMediationOffers.any() |\
            Offer.userMediationOffers.any(UserMediation.user != user)
        )

    # REMOVE OFFERS WITHOUT THUMBS
    print('after userMediation offers.count', query.count())
    query = query.outerjoin(Thing)\
                 .outerjoin(EventOccurence)\
                 .outerjoin(Event)\
                 .filter((Thing.thumbCount > 0) |
                         (Event.thumbCount > 0))
    n = len(query)
    for i in range(n):
        J = J(user,query[i],10)
        p = len(J)
        delta = Delta(user,query[i])
        for j in range(p):
            if (delta + user.preferences[J[p][0]][J[p][1]]) < 1):
                user.preferences[J[p][0]][J[p][1]] += delta/2
            else:
                user.preferences[J[p][0]][J[p][1]] = (user.preferences[J[p][0]][J[p][1]] +1)/2

### Seconde manière de get des offer avec l'autre  fonction attraction
def get_reco_offers2(user,limit=1):
    query = Offer.query
    # REMOVE OFFERS FOR WHICH THERE IS ALREADY A MEDIATION FOR THIS USER
    print('before userMediation offers.count', query.count())
    if user.is_authenticated:
        query = query.filter(
            ~Offer.userMediationOffers.any() |\
            Offer.userMediationOffers.any(UserMediation.user != user)
        )

    # REMOVE OFFERS WITHOUT THUMBS
    print('after userMediation offers.count', query.count())
    query = query.outerjoin(Thing)\
                 .outerjoin(EventOccurence)\
                 .outerjoin(Event)\
                 .filter((Thing.thumbCount > 0) |
                         (Event.thumbCount > 0))
    print('before tri offers.count', query.count())
        if user.is_authenticated:
            best = 0
            index = 0
            n = len(query)
            L1 = user.preferences
            for i in range(n):
                L2 = offer.preferences
                if best < attraction2(L1,L2):
                    best = attraction2(L1,L2)
                    index = i
            Proposition = query.get(index)
            query.delete(index)
            return Proposition


 ###TODo LATEX PARTIE 4
