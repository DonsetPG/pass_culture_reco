import bcrypt
from flask import current_app as app

db = app.db
amount_user = 1
alpha = 1
alphaBis = 1
betaBis = 1

class User(app.model.PcObject,
            db.Model,
            app.model.HasThumbMixin
        ):
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.Binary(60), nullable=False)

    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))

    userOfferers = db.relationship(app.model.UserOfferer,
                                   back_populates="user")

    account = db.Column(db.Numeric(10,2))

    preferences=[1]*Offer.tags.length

    #What the users liked (type Offer)
    accepted=[]

    #What the user disliked (type Offer)
    rejected=[]

    #The offers the user has already seen
    seen=accepted+rejected




    #When a user likes an offer
    def chooseOffer(offer, liked):
        n=seen.length
        if(liked):
            accepted.append(offer)

            for i in range(Offer.tags.length):
                preferences[i] += alpha * ((n/(n+1))*preferences[i] + (1/(n+1))*offer.preferences[i])
                offer.preferences[i] += beta * ((n/(n+1))*offer.preferences[i] + (1/(n+1))*preferences[i]) * (V(preferences,offer.preferences)/amount_user)
        else:
            rejected.append(offer)
            for i in range(Offer.tags.length):
                preferences[i]+= alphaBis* ((n/(n+1))*preferences[i] + (1/(n+1))*(1-offer.preferences[i]))
                offer.preferences[i] += (betaBis/amount_user)* ((n/(n+1))*offer.preferences[i] + (1/(n+1))*(1-preferences[i]))

        seen.append(offer)






    def checkPassword(self, passwordToCheck):
        return bcrypt.hashpw(passwordToCheck.encode('utf-8'), self.password) == self.password

    def errors(self):
        errors = super(User, self).errors()
        if self.email:
            errors.checkEmail('email', self.email)
        if self.firstname:
            errors.checkMinLength('firstname', self.firstname, 2)
        if self.lastname:
            errors.checkMinLength('lastname', self.lastname, 2)
        # TODO: check password length >=8
        return errors

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def populateFromDict(self, dct):
        super(User, self).populateFromDict(dct)
        if dct.__contains__('password') and dct['password']:
            self.setPassword(dct['password'])

    def setPassword(self, newpass):
        self.password = bcrypt.hashpw(newpass.encode('utf-8'),
                                      bcrypt.gensalt())


app.model.User = User
