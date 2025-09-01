import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 Importa os dados do arquivo medical_examination.csv e atribue ao DataFrame df.
df = pd.read_csv('projeto_3/medical_examination.csv')

# 2 Adiciona uma coluna chamada overweight ao DataFrame. Para determinar se uma pessoa está com sobrepeso com base no IMC
df['overweight'] = ((df['weight'] / ((df['height'] / 100) ** 2)) > 25).astype(int)

# 3 Normaliza os dados das colunas cholesterol e gluc, 0 (Normal) e 1 (Fora do normal)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4 Cria um gráfico categórico parecido com o exemplo examples/Figure_1.png
def draw_cat_plot():
    # 5. Criar DataFrame no formato longo (long format)
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )

    # 6. Agrupar os dados e contar as ocorrências
    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="total")

    # 7. Criar o gráfico categórico com seaborn
    fig = sns.catplot(
        data=df_cat,
        kind="bar",
        x="variable",
        y="total",
        hue="value",
        col="cardio"
    ).fig

    # 8. Salvar a figura
    fig.savefig('catplot.png')
    return fig

# 10 Cria um mapa de calor com a matriz de correlação (parecido com o exemplo examples/Figure_2.png)
def draw_heat_map():
    # 11. Limpeza dos dados
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12. Calcular a matriz de correlação
    corr = df_heat.corr(numeric_only=True)

    # 13. Criar a máscara para o triângulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14. Configurar a figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15. Plotar o heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5}
    )

    # 16. Salvar a figura
    fig.savefig('heatmap.png')
    return fig
