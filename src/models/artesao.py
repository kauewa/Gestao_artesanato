from src.db import Db
from src.models.vendas import Vendas

class Artesao:

    def __init__(self, db:Db, id:int=None, nome:str=None, novo=None) -> None:
        self.nome_tabela = 'Artesao'
        self.db = db
        if novo:
            exists = self.db.select(self.nome_tabela, {'CPF_CNPJ': novo['CPF_CNPJ']})
            if not exists:
                self.id = self.db.insert(self.nome_tabela, novo)
                self.dados = self.db.select(self.nome_tabela, {'ID': self.id})
                vendas = Vendas(self.db, self.dados['ID'])
                self.dados['vendas'] = vendas.dados
                self.dados['valor_vendas'] = 0
                for venda in self.dados['vendas']:
                    self.dados['valor_vendas'] += (venda['Valor'] * venda['parcelas']) + venda['primeira_parcela']
            else:
                return None
        elif nome:
            self.dados = self.db.select(self.nome_tabela, {'Nome': nome})
            vendas = Vendas(self.db, self.dados['ID'])
            self.id = self.dados['ID']
            self.dados['vendas'] = vendas.dados
            self.dados['valor_vendas'] = 0
            for venda in self.dados['vendas']:
                self.dados['valor_vendas'] += (venda['Valor'] * venda['parcelas']) + venda['primeira_parcela']
        elif id:
            self.id = id
            self.dados = self.db.select(self.nome_tabela, {'ID': self.id})
            vendas = Vendas(self.db, self.dados['ID'])
            self.dados['vendas'] = vendas.dados
            self.dados['valor_vendas'] = 0
            for venda in self.dados['vendas']:
                self.dados['valor_vendas'] += (venda['Valor'] * venda['parcelas']) + venda['primeira_parcela']
        

    def update(self):
        print('Update')

    def delete(self):
        print('Delete')


    @staticmethod
    def get_artesaos(db):
        artesao_db = db.select_all('Artesao')
        return [Artesao(db, id=artesao['ID']) for artesao in artesao_db]