from flask_restful import Resource, reqparse
from models.hotel import HotelModelo
from flask_jwt_extended import jwt_required
from models.site import SiteModelo

# Endpoint de listar todos os hoteis


class Hoteis(Resource):
    def get(self):
        # SELECY * FROM hoteis
        return {'hoteis': [hotel.json() for hotel in HotelModelo.query.all()]}

# Endpoint para CRUD do hotel


class Hotel(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True,
                           help="The field 'nome' cannot be left blank")
    atributos.add_argument('diaria')
    atributos.add_argument('estrela')
    atributos.add_argument('site_id')

    def get(self, hotel_id):
        hotel = HotelModelo.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        # status code 404 - not found
        return {'message': 'Hotel not found'}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModelo.find_hotel(hotel_id):
            # Bad Request
            return {"message": "Hotel ID '{}' already exists".format(hotel_id)}, 400

        dados = Hotel.atributos.parse_args()

        if not SiteModelo.find_by_id(dados['site_id']):
            return {"message": "The hotel must be associated to a valid site id".format(hotel_id)}, 400

        hotel = HotelModelo(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500

        return hotel.json()

    @jwt_required
    def put(self, hotel_id):

        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModelo.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)

            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel'}, 500

            return hotel_encontrado.json(), 200  # Ok

        hotel = HotelModelo(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500

        return hotel.json(), 201  # Created

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModelo.find_hotel(hotel_id)
        if hotel:

            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel'}, 500
            return {'menssage': 'Hotel deleted'}

        # status code 404 - not found
        return {'message': 'Hotel not found'}, 404
