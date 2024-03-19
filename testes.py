from src.models.cliente import Cliente
from src.models.produtos import Produto
from src.models.vendas import Vendas
from src.db import Db
from src.models.artesao import Artesao
from src import utils

# print(dia_hoje())
db = Db()
print(db.select_all('Produtos'))

# db.insert('Categoria', categoria)
# db = Db()
# vendas = Artesao.get_artesaos(db)

# for venda in vendas:
#     print(venda.dados)
# db = Db()

# dado = db.select('Clientes', {'Nome': 'Kauê Wandscher'})
# print(dado)

# # dados = {'Nome': 'Kauê Wandscher', 'dt_nasc': '27/12/2000', 'email': 'wandscherkaue@gmail.com', 'telefone': '49991778172', 'CPF_CNPJ': '09009138941'}

# # artesao = Artesao(db=db, nome=dados['Nome'], novo=dados)
# # print(artesao.dados)

# dados = db.select_all('Artesao', 'ID, Nome')
# print(dados)

# for dado in dados:
#     cliente = Cliente(db=db, nome=str(dado['Nome']))
#     print(cliente.dados)