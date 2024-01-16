from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(_name_)
api = Api(app)

dosya_uzantisi = r'C:\Users\qwerty\Documents\AçıkKaynak\Hafta_2_Odev\users.csv'


class Users(Resource):
    def get(self):
        data = pd.read_csv(dosya_uzantisi)
        data = data.to_dict('records')
        return {'data' : data}, 200

    def post(self):
        json = request.get_json()
        req_data = pd.DataFrame({
            'name'      : [json['name']],
            'age'       : [json['age']],
            'city'      : [json['city']],
            'weight'    : [json['weight']],
            'height'    : [json['height']]
        })
        data = pd.read_csv('users.csv')
        data = pd.concat([data, req_data], ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'message' : 'Record successfully added.'}, 200

    def delete(self):
        name = request.args['name']
        data = pd.read_csv('users.csv')

        if name in data['name'].values:
            data = data[data['name'] != name]
            data.to_csv('users.csv', index=False)
            return {'message': 'Record successfully deleted.'}, 200
        else:
            return {'message': 'Record not found.'}, 404

class Cities(Resource):
    def get(self):
        data = pd.read_csv('users.csv', usecols=['city'])
        data = data.to_dict('records')
        return {'data' : data}, 200

class Name(Resource):
    def get(self, name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data': entry}, 200
        return {'message': 'No entry found with this name!'}, 404

class BMI(Resource):
    def get(self, name):
        data = pd.read_csv('users.csv')
        for entry in data.to_dict('records'):
            if entry['name'] == name:
                weight = entry.get('weight', 0)
                height = entry.get('height', 0)

                if weight > 0 and height > 0:
                    bmi = (weight / (height ** 2))*10000

                    # BMI kategorilerini belirleme
                    if bmi < 18.5:
                        category = 'Zayif'
                    elif 18.5 <= bmi < 25:
                        category = 'Normal Kilolu'
                    elif 25 <= bmi < 30:
                        category = 'Fazla Kilolu'
                    else:
                        category = 'Asiri Kilolu'

                    return {'name': name, 'bmi': bmi, 'category': category}, 200
                else:
                    return {'message': 'Weight or height is not provided for BMI calculation.'}, 400

        return {'message': 'No entry found with this name!'}, 404

# Add URL endpoints
api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/<string:name>')
api.add_resource(BMI, '/bmi/<string:name>')

if _name_ == '_main_':
    app.run()