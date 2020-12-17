from flask_restful import Resource, reqparse
from models.usuario import UsuarioModelo
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required,get_raw_jwt
from blacklist import BLACKLIST
import traceback

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True,
                       help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True,
                       help="The field 'senha' cannot be left blank")
atributos.add_argument('ativado', type=bool)
atributos.add_argument('email', type=str)

# Endpoint para CRUD do hotel
class Usuario(Resource):

    def get(self, user_id):
        user = UsuarioModelo.find_user(user_id)
        if user:
            return user.json()
        # status code 404 - not found
        return {'message': 'User not found'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UsuarioModelo.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user'}, 500
            return {'menssage': 'User deleted'}

        # status code 404 - not found
        return {'message': 'User not found'}, 404

# Endpoint para CRUD do hotel
class RegistroUsuario(Resource):
    def post(self):
        dados = atributos.parse_args()

        if not dados.get('email') or dados.get('email') is None:
            return {"message":"The field 'email' cannot be left blank"}, 400

        if UsuarioModelo.find_by_email(dados['email']):
            # Bad Request
            return {"message": "The email '{}' already exists".format(dados['email'])}, 400

        if UsuarioModelo.find_by_login(dados['login']):
            # Bad Request
            return {"message": "The login '{}' already exists".format(dados['login'])}, 400

        user = UsuarioModelo(**dados)
        user.ativado = False

        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return {"message":"An internal server error has ocurred"},500
            
        return {"message": "User created sucessfully"}, 201  # Created


class LoginUsuario(Resource):

    def post(self):
        dados = atributos.parse_args()

        user = UsuarioModelo.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'access_token': token_de_acesso}, 200
            return {"message": "User not confirmed"}, 400    
        # Unauthorize
        return {"message": "The username or password is incorrect"}, 401

class LogoutUsuario(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully"}, 200

class ConfirmaUsuario(Resource):

    @classmethod
    def get(cls, user_id):
        user = UsuarioModelo.find_user(user_id)

        if not user:
            return {"message":"User id '{}' not found".format(user_id)},404

        user.ativado = True
        user.save_user()
        return {"message":"User id '{}' confirmed sucessfully".format(user_id)},200        