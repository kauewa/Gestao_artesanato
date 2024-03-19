from src.db import Db

class Vendas:

    def __init__(self, db:Db, artesao:int=None, id:int=None, novo=None) -> None:
        self.nome_tabela = 'Vendas'
        self.db = db
        
        if novo:
            id = self.db.insert(self.nome_tabela, novo)
            self.dado = self.db.select(self.nome_tabela, {'ID': id})
            self.dado['Produtos'] = self.db.select_all('produto_venda', where={'venda': int(self.dado['ID'])})
            lista_produtos = []
            for produto in self.dado['Produtos']:
                dado = self.db.select('Produtos', {'ID': produto['produto']})
                dado['quantidade'] = produto['Quantidade']
                dado['categoria'] = self.db.select('Categoria', {'ID': dado['categoria']})
                dado['categoria'] = dado['categoria']['nome_categoria']
                lista_produtos.append(dado)
            self.dado['Produtos'] = lista_produtos
            self.dado['nome_cliente'] = self.db.select('Clientes', {'ID': self.dado['Cliente']})['Nome']
            self.dado['artesao'] = self.db.select('Artesao', {'ID': self.dado['artesao']})
            self.dado['artesao'] = self.dado['artesao']['Nome']
            self.dado['valor_total'] = (self.dado['Valor'] * self.dado['parcelas']) + self.dado['primeira_parcela']
        
        elif artesao:
            self.artesao = artesao
            self.dados = self.db.select_all(self.nome_tabela, where={'artesao': artesao})
            nova_lista = []
            for dados in self.dados:
                dados['Produtos'] = self.db.select_all('produto_venda', where={'venda': int(dados['ID'])})
                lista_produtos = []
                for produto in dados['Produtos']:
                    dado = self.db.select('Produtos', {'ID': produto['produto']})
                    dado['quantidade'] = produto['Quantidade']
                    dado['categoria'] = self.db.select('Categoria', {'ID': dado['categoria']})
                    dado['categoria'] = dado['categoria']['nome_categoria']
                    lista_produtos.append(dado)
                dados['Produtos'] = lista_produtos
                dados['nome_cliente'] = self.db.select('Clientes', {'ID': dados['Cliente']})['Nome']
                dados['artesao'] = self.db.select('Artesao', {'ID': dados['artesao']})
                dados['artesao'] = dados['artesao']['Nome']
                dados['valor_total'] = (dados['Valor'] * dados['parcelas']) + dados['primeira_parcela']
                nova_lista.append(dados)
            
            self.dados = nova_lista
        
        elif id:
            self.dado = self.db.select(self.nome_tabela, {'ID': id})
            self.dado['Produtos'] = self.db.select_all('produto_venda', where={'venda': int(self.dado['ID'])})
            lista_produtos = []
            for produto in self.dado['Produtos']:
                dado = self.db.select('Produtos', {'ID': produto['produto']})
                dado['quantidade'] = produto['Quantidade']
                dado['categoria'] = self.db.select('Categoria', {'ID': dado['categoria']})
                dado['categoria'] = dado['categoria']['nome_categoria']
                lista_produtos.append(dado)
            self.dado['Produtos'] = lista_produtos
            self.dado['nome_cliente'] = self.db.select('Clientes', {'ID': self.dado['Cliente']})['Nome']
            self.dado['artesao'] = self.db.select('Artesao', {'ID': self.dado['artesao']})
            self.dado['artesao'] = self.dado['artesao']['Nome']
            self.dado['valor_total'] = (self.dado['Valor'] * self.dado['parcelas']) + self.dado['primeira_parcela']
        else:
            print('Nenhuma referência de vendas')

    @staticmethod
    def get_vendas(db:Db):
        vendas_db = db.select_all('Vendas')
        return [Vendas(db, id=venda['ID']) for venda in vendas_db]
