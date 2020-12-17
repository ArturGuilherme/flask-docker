from flask_restful import Resource
from models.site import SiteModelo

class Sites(Resource):

    def get(self):
        return {'sites': [site.json() for site in SiteModelo.query.all()]}

class Site(Resource):

    def get(self,url):
        site = SiteModelo.find_site(url)
        if site:
            return site.json()
        return {"message": "Site not found"}, 404

    def post(self,url):
        site = SiteModelo.find_site(url)
        if site:
            return {"message": "The site '{}' already registered".format(url)},400 #bad request
        
        site = SiteModelo(url)
        try:
            site.save_site()
        except:
            return {"message": "An internal error ocurred trying to save site".format(url)},400 #bad request

        return site.json()

    def delete(self,url):
        site = SiteModelo.find_site(url)
        if site:
            try:
                site.delete_site()
                return {'menssage': 'site deleted'}
            except:
                 return {"message": "An internal error ocurred trying to delete site".format(url)},400 #bad request
        return {"message": "Site not found"}, 404