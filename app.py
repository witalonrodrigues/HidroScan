# RM559023 - WITALON ANTONIO RODRIGUES

import pandas as pd
import matplotlib.pyplot as plt

def carregar_dados(caminho_arquivo):
    try:
        df = pd.read_csv(
            caminho_arquivo,
            sep=';',
            encoding='latin1',
            skiprows=4
        )
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        return df
    except Exception as e:
        print(f'Erro ao carregar o arquivo: {e}')
        return None

df = carregar_dados("mdr_sedec_dados_informados_2022.csv")

def forca_opcao(lista, msg, msg_erro):
    while True:
        opcao = input(msg)
        if opcao in lista:
            return opcao
        print(msg_erro)
        return forca_opcao(lista, msg, msg_erro)


# função para filtrar vitimas por estado
def filtrar_vitimas(df):
    uf_opcao = df['uf'].unique()
    uf = forca_opcao(uf_opcao, 'Digite o UF que deseja filtrar\n-> ', 'UF Inválido, Tente Novamente!')
    
    df_filtrado = df[df['uf'] == uf]

    mortos = pd.to_numeric(df_filtrado['dh_mortos'], errors='coerce').sum()
    feridos = pd.to_numeric(df_filtrado['dh_feridos'], errors='coerce').sum()
    desabrigados = pd.to_numeric(df_filtrado['dh_desabrigados'], errors='coerce').sum()
    desaparecidos = pd.to_numeric(df_filtrado['dh_desaparecidos'], errors='coerce').sum()

    print(f"\nAnálise de Vítimas no Estado {uf}")
    print(f"Mortos: {mortos}")
    print(f"Feridos: {feridos}")
    print(f"Desabrigados: {desabrigados}")
    print(f"Desaparecidos: {desaparecidos}")
    return

# função para filtrar municipios com maior destruição habitacional
def destruicao(df):
    # Substitui valores ausentes por 0
    df['dm_unidades_habitacionais_destruídas'] = df['dm_unidades_habitacionais_destruídas'].fillna(0)

    # Garante que a coluna está numérica
    df['dm_unidades_habitacionais_destruídas'] = pd.to_numeric(df['dm_unidades_habitacionais_destruídas'], errors='coerce').fillna(0)

    # Agrupa por município e UF
    destruicao_total = df.groupby(['uf', 'município'])['dm_unidades_habitacionais_destruídas'].sum()

    # Ordena do maior para o menor
    destruicao_ordenada = destruicao_total.sort_values(ascending=False)

    # Exibe os 10 primeiros
    print("\nMUNICÍPIOS COM MAIS UNIDADES HABITACIONAIS DESTRUÍDAS")
    print(destruicao_ordenada.head(10))

    return
# função para filtrar municipio que tiveram poluição ambiental
def poluicao_ambiental(df):
    colunas_poluicao = [
        'da_poluição_ou_contaminação_da_água',
        'da_poluição_ou_contaminação_do_ar',
        'da_poluição_ou_contaminação_do_solo',
        'da_diminuição_ou_exaurimento_hídrico',
        "da_incêndios_em_parques,_apa's_ou_app's"
    ]

    registros = []

    for i in range(len(df)):
        municipio = df.iloc[i]['município']
        uf = df.iloc[i]['uf']
        for coluna in colunas_poluicao:
            valor = df.iloc[i][coluna]
            if pd.notna(valor) and str(valor).strip() != "":
                registros.append({
                    'Município': municipio,
                    'UF': uf,
                    'Tipo de Poluição': coluna.replace('da_', '').replace('_', ' ').capitalize()
                })

    df_exportar = pd.DataFrame(registros)

    try:
        df_exportar.to_excel("poluicoes_municipios.xlsx", index=False)
        print("Arquivo exportado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# função para gerar gráfico de pessoas desabrigadas
def grafico_desabrigados(df):
    dados = df.groupby('uf')[['dh_desabrigados', 'dh_desalojados']].sum()
    dados['moradia_comprometida'] = dados['dh_desabrigados'] + dados['dh_desalojados']

    plt.figure(figsize=(14,6))
    plt.bar(dados.index, dados['moradia_comprometida'], color='blue')
    plt.title('Total de Pessoas Desabrigadas e Desalojadas por UF')
    plt.xlabel('UF')
    plt.ylabel('Número de Pessoas')
    plt.show()
    print(dados)
    return
# calcular indice de risco por municipio
def indice_risco(df):
    indicadores = [
        'dh_mortos',
        'dh_feridos',
        'dh_desabrigados',
        'dh_desalojados',
        'dm_unidades_habitacionais_destruídas'
    ]

    df[indicadores] = df[indicadores].fillna(0)
    df['indice_bruto'] = df[indicadores].sum(axis=1)
    df_uf = df.groupby('uf')['indice_bruto'].sum().reset_index()    
    valor = ''
    # função pra classifcar o risco
    def classificar_risco(valor):
        if valor >= 10000:
            return 'Alto'
        elif valor >= 2000:
            return 'Médio'
        else:
            return 'Baixo'

    df_uf["Nível de Risco"] = df_uf['indice_bruto'].apply(classificar_risco)
    

    print("\nÍndice de Risco por Estado (UF):\n")
    print(df_uf[['uf', 'Nível de Risco']])
# Simular cenarios onde ocorre aumento de chuva.
def simular_cenario(df):

    try:
        aumento = float(input("Digite o percentual de aumento da chuva (ex: 20 para 20%): "))
    except ValueError:
        print("Entrada inválida. Digite apenas números.")
        return

    fator = 1 + (aumento / 100)

    colunas_afetadas = [
        'dh_mortos',
        'dh_feridos',
        'dh_desabrigados',
        'dh_desalojados',
        'dm_unidades_habitacionais_destruídas'
    ]

    df[colunas_afetadas] = df[colunas_afetadas].fillna(0)

    df_original = df.groupby('uf')[colunas_afetadas].sum()

    df_simulado = df_original * fator

    # comparar valores originais e projetados em um gráfico
    print("\nComparativo entre valores atuais e simulados (Desabrigados):")
    print(df_simulado[['dh_mortos', 'dh_desabrigados', 'dh_feridos', 'dm_unidades_habitacionais_destruídas', 'dh_desalojados']].round(0))
    return



def menu():
    # Mostra o menu de opções para o usuário."
    print("\nANALISADOR DE IMPACTO DE ENCHENTES")
    print("1. Análise rápida: vítimas por UF (mortos, feridos, desabrigados, desalojados)")
    print("2. Municípios com mais unidades habitacionais destruídas")
    print("3. Exportar Planilha de Municípios com registro de poluição ambiental")
    print("4. Exibir gráfico: desalojados vs desabrigados por UF")
    print("5. Calcular indíce de risco por UF (alto, médio ou baixo)")
    print("6. Simular cenários de aumento de chuva.")
    print("0. Sair")

    escolha = forca_opcao(['1','2','3','4','5','6','0'], 'Digite o número correspondente para escolher a função \n-> ', 'Opção Inválida. Tente Novamente!')
    return escolha

def main():
    while True:
        opcao = menu()
        if opcao == '1':
            filtrar_vitimas(df)
        elif opcao == '2':
            destruicao(df)
        elif opcao == '3':
            poluicao_ambiental(df)
        elif opcao == '4':
            grafico_desabrigados(df)
        elif opcao == '5':
            indice_risco(df)
        elif opcao == '6':
            simular_cenario(df)
        else:
            print('Saindo...')
            break
            

if __name__ == "__main__":
    main()