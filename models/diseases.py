from dbinfo import db

class tbdiseases(db.Model):
    
    did = db.Column("did", db.Integer, primary_key = True)
    disease = db.Column(db.String)
    cause = db.Column(db.String)
    treatment = db.Column(db.String)
    
    def __init__(self, did=None, disease=None, cause=None, treatment=None):
        self.did = did
        self.disease = disease
        self.cause = cause
        self.treatment = treatment
        
    @classmethod
    def find_by_did(cls, did) -> "tbdiseases":
        return cls.query.filter_by(did=did).first()
    
    @classmethod
    def insert(cls, disease, cause, treatment):
        obj = cls(disease=disease, cause=cause, treatment=treatment)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def delete_by_did(cls, did):
        obj = cls.query.filter_by(did=did).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()

    @classmethod
    def update_by_did(cls, did, disease, cause, treatment):
        obj = cls.query.filter_by(did=did).first()
        if obj:
            obj.disease = disease
            obj.cause = cause
            obj.treatment = treatment
            db.session.commit()  
            return obj     
   