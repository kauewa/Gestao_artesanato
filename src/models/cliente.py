from src.db import Db

class Cliente:
    def __init__(self, db:Db, nome:str=None, id:int=None, novo=None) -> None:
        self.nome_tabela = 'Clientes'
        self.db = db
        if novo:
            exists = self.db.select(self.nome_tabela, {'CPF': novo['CPF']})
            if not exists:
                self.id = self.db.insert(self.nome_tabela, novo)
            else:
                return None
            self.dados = self.db.select(self.nome_tabela, {'ID': self.id})
        elif nome:
            self.dados = self.db.select(self.nome_tabela, {'Nome': nome})
        elif id:
            self.id = id
            self.dados = self.db.select(self.nome_tabela, {'ID': self.id})
        
    def update(self):
        print('Update')

    def delete(self):
        print('Delete')


    @staticmethod
    def get_clientes(db):
        cliente_db = db.select_all('Clientes')
        return [Cliente(db, id=cliente['ID']) for cliente in cliente_db]