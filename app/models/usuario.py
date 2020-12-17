from sql_alchemy import banco
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = 'sandboxf1653b0ae43147649365d91dcb4063c0.mailgun.org'
MAILGUNA_API_KEY = '2693303c14f8430795244e1f895a843a-95f6ca46-1b2b2ad3'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@testeapi.com'
# Classe modelo do hotel


class UsuarioModelo(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    ativado = banco.Column(banco.Boolean, default=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)

    def __init__(self, login, senha, ativado, email):
        self.login = login
        self.senha = senha
        self.ativado = ativado
        self.email = email

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'ativado': self.ativado,
            'email': self.email
        }

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + \
            url_for('confirmausuario', user_id=self.user_id)
        return post("https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
                    auth=("api", MAILGUNA_API_KEY),
                    data={"from": '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                          "to": self.email,
                          "subject": "Confirmação de Cadastro",
                          "text": "Confirme seu cadastro clicando no link a seguir: {}".format(link),
                          "html": "<html><p>\
                              Confirme seu cadastro clicando no link a seguir: <a href='{}'>CONFIRMAR EMAIL</a></p></html>".format(link)
                        }
                    )

    #  Função para auxiliar a busca do hotel pelo ID
    @ classmethod
    def find_user(cls, hotel_id):
        # SELECT * FROM usuarios WHERE hotel_id = hotel_id LIMIT 1
        user = cls.query.filter_by(user_id=hotel_id).first()
        if user:
            return user
        return None

    # Função para auxiliar a busca do hotel pelo ID
    @ classmethod
    def find_by_login(cls, login):
        # SELECT * FROM usuarios WHERE login = login LIMIT 1
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    # Função para auxiliar a busca do hotel pelo ID
    @ classmethod
    def find_by_email(cls, email):
        # SELECT * FROM usuarios WHERE login = login LIMIT 1
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None
