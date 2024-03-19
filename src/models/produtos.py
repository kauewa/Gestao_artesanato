from src.db import Db
from src.utils import dia_hoje

class Produto:
    def __init__(self, db:Db, nome:str=None, id:int=None, novo=None) -> None:
        self.nome_tabela = 'Produtos'
        self.db = db
        if novo:
            self.id = self.db.insert(self.nome_tabela, novo['produto'])
            print('id: ' + str(self.id))
            quantidade = {
                'produto': self.id,
                'data': dia_hoje(),
                'Quantidade': novo['estoque']
            }
            print(quantidade)
            id = self.db.insert('produto_estoque', quantidade)
            self.dados = self.db.select(self.nome_tabela, {'ID': self.id})
            self.dados['Artesao'] = self.db.select('Artesao', {'ID': self.dados['Artesao']})
            self.dados['categoria'] = self.db.select('Categoria', {'ID': self.dados['categoria']})
            self.dados['Estoque'] = 0
            for estoque in self.db.select_all('produto_estoque', where={'produto': self.id}):
                self.dados['Estoque'] += estoque['Quantidade']
            for estoque in self.db.select_all('produto_venda', where={'produto': self.id}):
                self.dados['Estoque'] -= estoque['Quantidade']
        elif nome:
            self.dados = self.db.select(self.nome_tabela, {'Nome_produto': nome})
            self.id = self.dados['ID']
            self.dados['Artesao'] = self.db.select('Artesao', {'ID': self.dados['Artesao']})
            self.dados['categoria'] = self.db.select('Categoria', {'ID': self.dados['categoria']})
            self.dados['Estoque'] = 0
            for estoque in self.db.select_all('produto_estoque', where={'produto': self.id}):
                self.dados['Estoque'] += estoque['Quantidade']
            for estoque in self.db.select_all('produto_venda', where={'produto': self.id}):
                self.dados['Estoque'] -= estoque['Quantidade']
        elif id:
            self.id = id
            self.dados = self.db.select(self.nome_tabela, {'ID': self.id})
            self.dados['Estoque'] = 0
            self.dados['Artesao'] = self.db.select('Artesao', {'ID': self.dados['Artesao']})
            self.dados['categoria'] = self.db.select('Categoria', {'ID': self.dados['categoria']})
            self.dados['Estoque'] = 0
            for estoque in self.db.select_all('produto_estoque', where={'produto': self.id}):
                self.dados['Estoque'] += estoque['Quantidade']
            for estoque in self.db.select_all('produto_venda', where={'produto': self.id}):
                self.dados['Estoque'] -= estoque['Quantidade']
        else:
            print('Produto não especificado')
        

        
        

    def update(self):
        print('Update')

    def delete(self):
        print('Delete')


    @staticmethod
    def get_produtos(db):
        produtos_db = db.select_all('Produtos')
        return [Produto(db, produto['Nome_produto']) for produto in produtos_db]
