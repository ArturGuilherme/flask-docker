from sql_alchemy import banco

#Classe modelo do hotel
class HotelModelo(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String,primary_key=True)
    nome = banco.Column(banco.String(80))
    diaria = banco.Column(banco.Float(precision=2))
    estrela = banco.Column(banco.Float(precision=1))
    site_id = banco.Column(banco.Integer,banco.ForeignKey('sites.site_id'))

    def __init__(self, hotel_id, nome, diaria, estrela,site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.diaria = diaria
        self.estrela = estrela
        self.site_id = site_id
    
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'diaria': self.diaria,
            'estrela': self.estrela,
            'site_id': self.site_id
        }

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()


    def update_hotel(self, nome, diaria, estrela,site_id):
        self.nome = nome
        self.diaria = diaria
        self.estrela = estrela
        self.site_id = site_id

    
    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

    #Função para auxiliar a busca do hotel pelo ID
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() #SELECT * FROM hoteis WHERE hotel_id = hotel_id LIMIT 1
        if hotel:
            return hotel
        return None
