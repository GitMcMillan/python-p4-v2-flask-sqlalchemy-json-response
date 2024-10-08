# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from sqlalchemy import func

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)



@app.route('/demo_json')
def demo_json():
    pet_dict = {'id': 1,
                'name': 'Fido',
                'species': 'Dog'
                }
    return make_response(pet_dict, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        body = {'id': pet.id,
                'name': pet.name,
                'species': pet.species}
        status = 200
    else:
        body = {'mesasage:': f'Pet {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/species/<string:species>')
def get_by_species(species):
    pets = []#array to store pet objects
    #loop over list of pets in Pets
    #filter by id and grab all 
    for pet in Pet.query.filter_by(species=species).all():
        #format the pet object and store
        pet_dict = {'id': pet.id,
                    'name': pet.name,
                    }
        #append the object to the list
        pets.append(pet_dict)
    #make a body object    
    body = {'count':len(pets),
            'pets': pets
            }
    #return the body object using make_response and add error code
    return make_response(body, 200)
    
    #if exists, return object

    #format object
    pass

if __name__ == '__main__':
    app.run(port=5554, debug=True)
