import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Buscando e arrumando os dados ---
try:
    print("Buscando os dados no portal do ISP...")
    endereco_dados = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_geral = pd.read_csv(endereco_dados, sep=';', encoding='iso-8859-1')

    df_por_municipio = df_geral.groupby('munic', as_index=False)['hom_doloso'].sum()
    df_por_ano = df_geral.groupby('ano', as_index=False)['hom_doloso'].sum()

    print("Dados na mão! Preparando para a análise e os gráficos...")

except Exception as e:
    print(f"Opa, deu erro ao buscar os dados: {e}")
    print("O script não pode continuar sem os dados. Verifique sua conexão ou se o site do ISP está no ar.")
    exit()

# --- 2. Análise Estatística Detalhada (Quartis) ---
print("\n--- Análise Estatística da Distribuição por Município ---")
# Usando o método .describe() para obter as principais estatísticas de uma vez
estatisticas = df_por_municipio['hom_doloso'].describe()

Q1 = estatisticas['25%']
mediana = estatisticas['50%']
Q3 = estatisticas['75%']
IQR = Q3 - Q1

# Contando quantos municípios estão em cada faixa de quartil
total_municipios = int(estatisticas['count'])
count_abaixo_q1 = df_por_municipio[df_por_municipio['hom_doloso'] <= Q1].shape[0]
count_entre_q1_q2 = df_por_municipio[(df_por_municipio['hom_doloso'] > Q1) & (df_por_municipio['hom_doloso'] <= mediana)].shape[0]
count_entre_q2_q3 = df_por_municipio[(df_por_municipio['hom_doloso'] > mediana) & (df_por_municipio['hom_doloso'] <= Q3)].shape[0]
count_acima_q3 = df_por_municipio[df_por_municipio['hom_doloso'] > Q3].shape[0]

print(f"Total de Municípios Analisados: {total_municipios}")
print("-" * 50)
print(f"Primeiro Quartil (Q1): {Q1:.2f}")
print(f"-> Interpretação: 25% dos municípios ({count_abaixo_q1} cidades) tiveram ATÉ {Q1:.0f} homicídios.")
print("-" * 50)
print(f"Mediana (Q2): {mediana:.2f}")
print(f"-> Interpretação: Metade dos municípios ({count_abaixo_q1 + count_entre_q1_q2} cidades) teve MENOS de {mediana:.0f} homicídios.")
print("-" * 50)
print(f"Terceiro Quartil (Q3): {Q3:.2f}")
print(f"-> Interpretação: 75% dos municípios tiveram até {Q3:.0f} homicídios. Os 25% mais violentos ({count_acima_q3} cidades) tiveram MAIS que esse valor.")
print("-" * 50)
print(f"Amplitude Interquartil (IQR = Q3 - Q1): {IQR:.2f}")
print(f"-> Interpretação: Os 50% centrais dos municípios variam em até {IQR:.0f} homicídios entre si, mostrando grande dispersão.")
print("-" * 50)


# --- 3. Montando o painel de gráficos (o "dashboard") ---
fig, graficos = plt.subplots(2, 2, figsize=(20, 15))

fig.suptitle('Raio-X dos Homicídios Dolosos no RJ', fontsize=22, weight='bold')

# --- Gráfico 1: Histograma  ---
graficos[0, 0].hist(df_por_municipio['hom_doloso'], bins=30, edgecolor='black', color='royalblue')
graficos[0, 0].set_title('Gráfico 1: Onde se Concentram os Casos?', fontsize=16)
graficos[0, 0].set_xlabel('Total de Homicídios')
graficos[0, 0].set_ylabel('Quantidade de Cidades')
graficos[0, 0].grid(axis='y', linestyle='--', alpha=0.5)


# --- Gráfico 2: Barras  ---
top_15_cidades = df_por_municipio.sort_values(by='hom_doloso', ascending=False).head(15)
graficos[0, 1].barh(top_15_cidades['munic'], top_15_cidades['hom_doloso'], color='firebrick')
graficos[0, 1].set_title('Gráfico 2: O Ranking das Cidades', fontsize=16)
graficos[0, 1].set_xlabel('Total de Homicídios')
graficos[0, 1].invert_yaxis()

# --- Gráfico 3: Linha do Tempo ---
graficos[1, 0].plot(df_por_ano['ano'], df_por_ano['hom_doloso'], marker='o', linestyle='-', color='forestgreen')
graficos[1, 0].set_title('Gráfico 3: A Violência Aumentou ou Diminuiu?', fontsize=16)
graficos[1, 0].set_xlabel('Ano')
graficos[1, 0].set_ylabel('Total de Homicídios no Estado')
graficos[1, 0].grid(True, linestyle='--', alpha=0.5)
graficos[1, 0].set_xticks(df_por_ano['ano'])

for label in graficos[1, 0].get_xticklabels():
    label.set_rotation(45)

# --- Gráfico 4: Boxplot ---
caixa = graficos[1, 1].boxplot(df_por_municipio['hom_doloso'], vert=False, patch_artist=True)

caixa['boxes'][0].set_facecolor('gold')
caixa['medians'][0].set_color('black')
caixa['whiskers'][0].set_color('black')
caixa['whiskers'][1].set_color('black')
caixa['caps'][0].set_color('black')
caixa['caps'][1].set_color('black')

graficos[1, 1].set_title('Gráfico 4: Resumo Estatístico da Distribuição', fontsize=16)
graficos[1, 1].set_xlabel('Total de Homicídios')
graficos[1, 1].set_yticks([])
graficos[1, 1].grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.show() # Opcional: descomente esta linha se quiser que o gráfico apareça na tela também.