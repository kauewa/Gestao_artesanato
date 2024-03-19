import sqlite3



class Db:
    def __init__(self) -> None:
        self.banco = sqlite3.connect('dados.db')
        self.cursor = self.banco.cursor()

    
    def insert(self, tabela:str, dados:dict):
        # Convertendo os valores do dicionário para uma string
        colunas = ', '.join(dados.keys())
        valores = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in dados.values()])

        query = f"""
        INSERT INTO {tabela} ({colunas}) VALUES ({valores})
        """
        self.cursor.execute(query)
        id_inserido = self.cursor.lastrowid
        self.banco.commit()
        return id_inserido

    def select_all(self, tabela:str, colunas='*', where:dict=None) -> list:
        try:
            if not where:
                query = f"""
                SELECT {colunas} from {tabela}
                """
            else:
                chave = list(where.keys())[0]
                valor = where[chave]

                query = f"""
                SELECT {colunas} from {tabela} WHERE {chave} = '{valor}'
            """
            res = self.cursor.execute(query)
            
            # Obtendo os nomes das colunas
            nomes_das_colunas = [coluna[0] for coluna in res.description]

            # Obtendo todos os resultados
            resultados = res.fetchall()

            # Criando uma lista de dicionários
            lista_de_resultados = [dict(zip(nomes_das_colunas, resultado)) for resultado in resultados]

            return lista_de_resultados
        except:
            return []

    def select(self, tabela:str, where:dict):
        try:
            # Obtendo a única chave
            chave = list(where.keys())[0]
            valor = where[chave]

            query = f"""
            SELECT * from {tabela} WHERE {chave} = '{valor}'
            """
            res = self.cursor.execute(query)
            # Obtendo os nomes das colunas
            nomes_das_colunas = [coluna[0] for coluna in res.description]

            # Obtendo o resultado
            resultado = res.fetchone()

            # Criando um dicionário com os nomes das colunas e os valores
            dict_resultado = dict(zip(nomes_das_colunas, resultado))

            return dict_resultado
        except:
            return None
        

