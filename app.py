
import base64
from datetime import datetime
import io
import os
import pandas as pd
import webview
from flask import Flask, redirect, render_template, request, flash, session
from src.models.vendas import Vendas
from src.db import Db
from src.models.produtos import Produto
from src.models.artesao import Artesao
from src.models.cliente import Cliente
from src import utils
from dotenv import load_dotenv



load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


webview.create_window('Mãos criativas artesanatos', app)

@app.route('/', methods=['GET'])
def init():
    return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        db = Db()
        artesaos = Artesao.get_artesaos(db)
        vendas_artesao = []
        valor_total_vendas = 0.0
        for artesao in artesaos:
            valor_venda = 0.0
            for venda in artesao.dados['vendas']:
                if utils.esta_no_mes_atual(venda['Data']):
                    valor_venda += (venda['Valor'] * venda['parcelas']) + venda['primeira_parcela']
            dados_venda = {
                'artesao': artesao.dados['Nome'],
                'valor': valor_venda
            }
            vendas_artesao.append(dados_venda)
            valor_total_vendas += valor_venda

        produtos = Produto.get_produtos(db)
        vendas_produto = db.select_all('produto_venda')
        tabela_produtos = []
        for produto in produtos:
            quantidade_venda_produto = 0
            valor_venda_produto = 0.0
            for venda in vendas_produto:
                if produto.dados['ID'] == venda['produto']:
                    total = produto.dados['preco'] * venda['Quantidade']
                    valor_venda_produto += total
                    quantidade_venda_produto += venda['Quantidade']
            dados_produto = {
                'nome': produto.dados['Nome_produto'],
                'estoque': produto.dados['Estoque'],
                'valor': valor_venda_produto, 
                'quantidade': quantidade_venda_produto
            }
            tabela_produtos.append(dados_produto)

        produto_maior_venda = max(tabela_produtos, key=lambda produto: produto['quantidade'])
        nome_produto_maior_venda = produto_maior_venda['nome']
    except:
        print('sem cadastros')

    return render_template('home.html', vendas_ = vendas_artesao, valor_total=valor_total_vendas, tabela_produtos=tabela_produtos, produto_mais_vendido=nome_produto_maior_venda)

@app.route('/venda/<id>')
def venda(id):
    db = Db()
    venda = Vendas(db, id=int(id))
    print(venda.dado)

    return render_template('venda.html', venda=venda)

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    db = Db()
    artesaos = Artesao.get_artesaos(db)

    return render_template('vendas.html', artesaos=artesaos)

@app.route('/cliente/<id>', methods=['GET', 'POST'])
def cliente(id):
    db = Db()
    cliente = Cliente(db, id=id)

    return render_template('cliente.html', cliente=cliente)

@app.route('/artesao', methods=['GET', 'POST'])
def artesaos():
    db = Db()
    artesao = Artesao.get_artesaos(db)

    return render_template('artesaos.html', artesaos=artesao)

@app.route('/artesao/<id>', methods=['GET', 'POST'])
def artesao(id):
    db = Db()
    artesao = Artesao(db, id=id)

    return render_template('artesao.html', artesao=artesao)

@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    db = Db()
    produtos = Produto.get_produtos(db)

    return render_template('estoque.html', produtos=produtos)

@app.route('/produto/<id>', methods=['GET', 'POST'])
def produto(id):
    db = Db()
    produto = Produto(db, id=int(id))
    
    if request.method == 'POST':
        estoque = int(request.form.get('estoque'))
        quantidade = {
                'produto': id,
                'data': utils.dia_hoje(),
                'Quantidade': estoque
            }
        db.insert('produto_estoque', quantidade)
        return redirect(f'/produto/{id}')

    return render_template('produto.html', produto=produto)

@app.route('/cadastro-produto', methods=['GET', 'POST'])
def cadastro_produto():
    db = Db()
    artesaos = db.select_all('Artesao', 'ID, Nome')
    categorias = db.select_all('Categoria')

    if request.method == 'POST':
        btn = request.form.get('verificacao')
        print(btn)
        if btn == '1':
            nome_categoria = request.form.get('nomeCategoria')
            if nome_categoria == '':
                btn = '0'
            else:
                existe = db.select('Categoria', {'nome_categoria': nome_categoria})
                if not existe:
                    db.insert('Categoria', {'nome_categoria': nome_categoria})
                    flash(f'Categoria {nome_categoria} cadastrado')
                    categorias = db.select_all('Categoria')
                else:
                    flash(f'Ja existe a categoria {nome_categoria}')

        if btn == '0':
            nome_produto = request.form.get('Nome_produto')
            preco = float(request.form.get('preco'))
            artesao = int(request.form.get('Artesao'))
            estoque = int(request.form.get('Estoque'))
            categoria = int(request.form.get('categoria'))
            descricao = request.form.get('descricao')

            #Verificação dos dados

            dados = {
                'produto': {
                    'Nome_produto': nome_produto,
                    'preco': preco,
                    'Artesao': artesao,
                    'categoria': categoria,
                    'descricao': descricao
                } ,
                'estoque': estoque
            }
            print(dados)
            produto = Produto(db, nome_produto, novo=dados)
            flash(f'Produto {produto.dados['Nome_produto']} criado com sucesso!')

        
    return render_template('cadastro_produto.html', categorias=categorias, artesaos=artesaos)


@app.route('/cadastro-venda', methods=['GET', 'POST'])
def cadastro_venda():
    db = Db()
    produtos = Produto.get_produtos(db)
    artesaos = Artesao.get_artesaos(db)
    clientes = Cliente.get_clientes(db)

    if request.method == 'POST':
        print('post')
        produto_vendido = request.form.getlist('produto[]')
        quantidades = request.form.getlist('quantidade[]')
        valores = []
        for id_produto, quantidade in zip(produto_vendido, quantidades):
            for produto in produtos:
                if int(id_produto) == produto.id:
                    valor = produto.dados['preco'] * int(quantidade)
                    valores.append(valor)
        
        valor_venda = sum(valores)
        artesao = int(request.form.get('Artesao'))
        cliente = int(request.form.get('Cliente'))
        dia = utils.dia_hoje()
        qtd_parcelas = int(request.form.get('qtd_parcelas'))
        entrada = request.form.get('entrada')
        forma_pagamento = request.form.get('forma_pagamento')
        
        if entrada == '':
            entrada = 0.0
        if qtd_parcelas >= 2:
            valor_venda = valor_venda - float(entrada)
            valor_venda = valor_venda / qtd_parcelas

        dados = {
            'artesao': artesao,
            'Forma_pagamento': forma_pagamento,
            'Valor': valor_venda,
            'primeira_parcela': entrada,
            'parcelas': qtd_parcelas,
            'Data': dia,
            'Cliente': cliente
        }
        print(dados)
        venda = Vendas(db, novo=dados)

        for id, quantidade in zip(produto_vendido, quantidades):
            dados_produto = {
                    'produto': int(id),
                    'venda': int(venda.dado['ID']),
                    'Quantidade': int(quantidade),
                }
            db.insert('produto_venda', dados_produto)

        flash('Venda cadastrada!')

    return render_template('cadastro_venda.html', produtos=produtos, artesaos=artesaos, clientes=clientes)

@app.route('/cadastro-cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    db = Db()

    if request.method == 'POST':
        nome = request.form.get('Nome')
        dt_nasc = request.form.get('dt_nasc')
        dt_nasc = datetime.strptime(dt_nasc, "%Y-%m-%d")
        dt_nasc = dt_nasc.strftime("%d/%m/%Y")
        email = request.form.get('email')
        endereco = request.form.get('Endereco')
        telefone = request.form.get('Telefone')
        cpf = request.form.get('CPF')

        dados = {
            'Nome': nome,
            'dt_nasc': dt_nasc,
            'email': email,
            'endereco': endereco,
            'telefone': telefone,
            'CPF': cpf
        }

        cliente = Cliente(db, nome, novo=dados)
        flash(f'Cliente {cliente.dados['Nome']} criado com Sucesso')
    
    return render_template('cadastro_cliente.html')



@app.route('/cadastro-artesao', methods=['GET', 'POST'])
def cadastro_artesao():
    db = Db()

    if request.method == 'POST':
        nome = request.form.get('Nome')
        dt_nasc = request.form.get('dt_nasc')
        dt_nasc = datetime.strptime(dt_nasc, "%Y-%m-%d")
        dt_nasc = dt_nasc.strftime("%d/%m/%Y")
        email = request.form.get('email')
        telefone = request.form.get('Telefone')
        cpf = request.form.get('CPF')

        dados = {
            'Nome': nome,
            'dt_nasc': dt_nasc,
            'email': email,
            'telefone': telefone,
            'CPF_CNPJ': cpf
        }

        artesao = Artesao(db, nome, novo=dados)
        flash(f'Artesao {artesao.dados['Nome']} criado com Sucesso')

    return render_template('cadastro_artesao.html')

@app.route('/relatorio', methods=['GET', 'POST'])
def relatorio():
    db = Db()
    if request.method == 'POST':
        tipo = request.form.get('relatorio')
        dt_inicio = request.form.get('dataInicio')
        dt_fim = request.form.get('dataFim')
        try:
            if tipo == "1":
                vendas = Vendas.get_vendas(db)
                vendas_por_data = [] 
                if not dt_inicio or not dt_fim:
                    flash('Por favor, forneça as datas de início e fim.')
                    return render_template('relatorios.html')

                try:
                    dt_inicio = datetime.strptime(dt_inicio, '%Y-%m-%d')
                    dt_fim = datetime.strptime(dt_fim, '%Y-%m-%d')

                    # Verifica se a data de início é anterior à data de fim
                    if dt_inicio > dt_fim:
                        flash('A data de início não pode ser posterior à data de fim.')
                        return render_template('relatorios.html')

                    # Restante do seu código...
                except ValueError:
                    flash('Formato de data inválido. Por favor, use o formato YYYY-MM-DD.')
                    return render_template('relatorios.html')
                for venda in vendas:
                    data_venda = datetime.strptime(venda.dado['Data'], '%d/%m/%Y')
                    if dt_inicio <= data_venda <= dt_fim:
                        vendas_por_data.append(venda.dado)
                df = pd.DataFrame(vendas_por_data)
                df['Produtos'] = df['Produtos'].apply(lambda x: [produto['Nome_produto'] for produto in x])
            elif tipo == "2":
                produtos = Produto.get_produtos(db)
                lista_produtos = []
                for produto in produtos:
                    lista_produtos.append(produto.dados)
                df = pd.DataFrame(lista_produtos)
                df['Artesao'] = df['Artesao'].apply(lambda x: x['Nome'])
                df['categoria'] = df['categoria'].apply(lambda x: x['nome_categoria'])
            else:
                df = pd.DataFrame()
        except Exception as e:
            df = pd.DataFrame()
            flash(f'ERRO ao buscar tabela: {e}')
        tabela = df.to_html()
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        excel_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

        return render_template('relatorios.html', table=tabela, excel_base64=excel_base64)


    return render_template('relatorios.html')

if __name__ == '__main__':
    webview.start()
    # app.run(debug=True)