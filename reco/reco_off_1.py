
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




def attraction(L1,L2):
    n1 = L1.length
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
            n = query.length
            L1 = user.preferences
            for i in range(n):
                L2 = offer.preferences
                if best < attraction(L1,L2):
                    best = attraction(L1,L2)
                    index = i
            Proposition = query.get(index)
            query.delete(index)
            return Proposition



#lien
