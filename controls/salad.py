from flask_restful import Resource, request
from flask import make_response, render_template, redirect, send_file, session
from models.diseases import tbdiseases
from schemas.diseaseschema import diseaseschema


class HomePage(Resource):
    @classmethod
    def get(cls):
        return {"msg": "Hello world!"}


class Disease(Resource):
    @classmethod
    def get(cls, did=None):
        try:
            data = tbdiseases.find_by_did(did)
            schema = diseaseschema(many=False)
            _data = schema.dump(data)
            return {"disease": _data}
        except Exception as err:
            return {"msg": err}

    # delete by did

    @classmethod
    def delete(cls, did=None):
        try:
            found_disease = tbdiseases.find_by_did(did)
            if found_disease:
                tbdiseases.delete_by_did(did)
                return {"message": "Disease deleted successfully"}, 200
            else:
                return {"message": "Disease not found"}, 404
        except Exception as err:
            return {"error": str(err)}, 500

    @classmethod
    def put(cls, did=None):
        try:
            data = request.get_json()
            disease = data["disease"]
            cause = data["cause"]
            treatment = data["treatment"]
            found_disease = tbdiseases.find_by_did(did) # check if disease exists in the database
            schemar = diseaseschema(many=False)
            # _data = schemar.dump(found_disease)
            if found_disease:
                data = tbdiseases.update_by_did(did, disease, cause, treatment)
                _data = schemar.dump(data)
                return {
                    "message": "Disease updated successfully",
                    "data": _data
                }, 200
        
            else:
                return {"message": f"Disease with id {did} was not found"}, 404
        except Exception as err:
            return {"error": str(err)}, 500
   

class DiseaseList(Resource):
    @classmethod
    def get(cls):
        try:
            data = tbdiseases.query.all()
            schema = diseaseschema(many=True)
            _data = schema.dump(data)
            return {"disease": _data}
        except Exception as err:
            return {"msg": err}
class AddNewDesease(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            disease = data["disease"]
            cause = data["cause"]
            treatment = data["treatment"]
            new_disease = tbdiseases.insert(disease, cause, treatment)
            schema = diseaseschema(many=False)
            _data = schema.dump(new_disease)
            return {"message": "Disease added successfully", "data": _data}, 201
        except Exception as err:
            return {"error": str(err)}, 500