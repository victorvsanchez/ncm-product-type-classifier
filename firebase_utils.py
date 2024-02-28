

from firebase_admin import credentials, firestore, initialize_app, get_app

class FireBaseConn():
    def __init__(self):
        self.cred = credentials.Certificate("./hvar-dufry-dev-46f2154886a2.json")
        try:
            self.default_app = initialize_app(self.cred)
            self.client = firestore.Client()

        except ValueError:
            self.default_app = get_app()
            self.client = firestore.Client()

    def update_doc_by_id(self, id, ncm):

        #Upadte data on firestore
        doc_ref = self.client.collection(u'Classificacoes').document(id)

        doc_ref.update({
            'result':'WRONG',
            'correct_ncm': ncm
        })

        return 'Para o Id ' + str(id) + ' foi atualizado a NCM com o valor: ' + str(ncm) + '.'

    def get_doc_by_id(self, id):
        #Search data on firestore
        doc_ref = self.client.collection(u'Classificacoes').document(id)
        doc = doc_ref.get()
        data = doc.to_dict()

        return data

    def save_to_firestore(self, id, payload):
        #save a new document to firestore
        doc_ref = self.client.collection(u'Classificacoes')
       
        doc_ref.document(id).set(payload)