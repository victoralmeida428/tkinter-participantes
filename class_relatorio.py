import pandas as pd
import re


class GerarRelatorio:

    def __init__(self, anos, modulo: int):
        '''modulo: Número do modulo a ser puxado da API'''
        self.__anos = anos
        self.__modulo = modulo
        self.__dfs = [pd.read_csv(URL_API,
                # acrescentando &cache=0 força atualização do link
                sep='|', low_memory=False) for ano in self.__anos]

        self.__df = pd.concat(self.__dfs)

    def gerar_nomes_items(self):
        '''Retorna uma lista única dos nomes dos itens'''
        return list(self.__df.NOME_ITEM.unique())

    def relatorio_por_analito(self, *itens):
        '''itens = ['ITEM01', 'ITEM02']
        Buscar relatório unicamente pelo analito'''
        print(itens[0])
        df = self.__filtrar_item(itens[0])
        group_rodada = df.groupby(['ANALITO'])['PART']\
                        .count().sort_values(ascending=False)\
                            .reset_index()
        group_rodada['média'] = round(group_rodada['PART']/len(df.NOME_ENVIO.unique()),2)
        return group_rodada

    def relatorio_por_rodada(self, *itens):
        '''itens = ['ITEM01', 'ITEM02']
        Gerar o relatório por rodada e por analito'''
        df = self.__filtrar_item(itens[0])            
        group_rodada = df.groupby(['ANALITO', 'NOME_ENVIO'])['PART']\
            .count()\
                .sort_values(ascending=False).reset_index()
        group_rodada.NOME_ENVIO = group_rodada.NOME_ENVIO\
            .apply(lambda x: self.__replace_mes(x))
        group_rodada['data'] = pd.to_datetime(group_rodada.NOME_ENVIO)       
        return group_rodada

    def salvar_relatorio(self, path, *item, relatorio='rodada'):
        '''path = caminho onde será armazenado os csv 
        item= itens,
        relatorio = literal['rodada', 'analito']

        Salva os relatórios no formato csv
        salvar_relatorio(r'pasta/subpasta', ['ITEM01', 'ITEM02'], 'analito')'''

        if relatorio == 'analito':
            df = self.relatorio_por_analito(item[0])
        elif relatorio == 'rodada':
            df = self.relatorio_por_rodada(item[0])
        else:
            raise Exception("Relatório Inválido")

        return df.to_csv(path)

    def __filtrar_item(self, *item):
        if item[0]:
            return self.__df.loc[self.__df.NOME_ITEM.isin(item[0])].copy()
        else:
            return self.__df

    def lista_rodadas(self, analito):
        '''Retorna uma lista com todos os analitos'''
        df = self.__df.loc[self.__df.ANALITO==analito].copy()
        return list(df.NOME_ENVIO.unique())

    def __correcao_mes(self, x: str):
        x = x.capitalize()
        x = x[:3]
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        mes = {mes: num for mes, num in zip(meses, range(1,13))}
        try:
            return (mes[x])
        except:
            raise Exception("Mês digitado de forma incorreta")

    def __replace_mes(self, x):
        padrao = re.compile('[A-Za-z]{3}')
        key = padrao.findall(x)[0]
        sub =  self.__correcao_mes(key)
        return x.replace(key, str(sub))
