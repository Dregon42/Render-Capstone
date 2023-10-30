from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, Rsvp, rsvp_schema, rsvps_schema, Messages, message_schema, messages_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/rsvps', methods=['POST'])
@token_required
def create_rsvp(current_user_token):
    guest_1 = request.json['guest_1']
    guest_2 = request.json['guest_2']
    message = request.json['message']
    

    print(f'BIG TESTER: {current_user_token.token}')

    rsvp = Rsvp(guest_1=guest_1, guest_2=guest_2, message=message)

    db.session.add(rsvp)
    db.session.commit()

    response = rsvp_schema.dump(rsvp)
    return jsonify(response)

@api.route('/rsvps', methods=['GET'])
@token_required
def get_rsvps(current_user_token):
    rsvps = Rsvp.query.all()
    response = rsvps_schema.dump(rsvps)
    return jsonify(response)

@api.route('/rsvps/<id>', methods=['GET'])
@token_required
def get_single_rsvp(current_user_token,id):
    rsvp = Rsvp.query.get(id)
    
    if rsvp:
        response = rsvp_schema.dump(rsvp)
        return jsonify(response)
    else:
        return jsonify({'message': 'Rsvp not found'}, 404)

@api.route('/rsvps/<id>', methods=['POST', 'PUT'])
@token_required
def update_rsvp(current_user_token, id):
    rsvp = Rsvp.query.get(id)


    if rsvp:
        rsvp.guest_1 = request.json['guest_1']
        rsvp.guest_2 = request.json['guest_2']
        rsvp.message = request.json['message']
        
        db.session.commit()
        response = rsvp_schema.dump(rsvp)
        return jsonify(response)
    else:
        return jsonify({'message': 'Rsvp not found'}, 404)

@api.route('/rsvps/<id>', methods=['DELETE'])
@token_required
def delete_rsvp(current_user_token, id):
    rsvp = Rsvp.query.get(id)

    if rsvp:
        db.session.delete(rsvp)
        db.session.commit()
        response = rsvp_schema.dump(rsvp)
        return jsonify(response)
    else:
        return jsonify({'message': 'Rsvp not found'}, 404)