import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("projeto_4/fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Copiar o dataframe limpo
    df_plot = df.copy()

    # Criar figura e gráfico
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_plot.index, df_plot['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Salvar figura
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Preparar os dados
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar['month_name'] = df_bar.index.strftime('%B')

    # Agrupar por ano e mês e calcular média
    df_grouped = df_bar.groupby(['year', 'month_name'])['value'].mean().unstack()

    # Garantir ordem correta dos meses
    ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
    df_grouped = df_grouped[ordered_months]

    # Criar gráfico de barras
    fig = df_grouped.plot(kind='bar', figsize=(15, 7)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.tight_layout()

    # Salvar figura
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['month_num'] = df_box['date'].dt.month

    # Ordenar meses corretamente
    df_box = df_box.sort_values('month_num')

    # Criar figura e subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))

    # Boxplot por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])  # Correto
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Boxplot por mês
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Salvar figura
    fig.savefig('box_plot.png')
    return fig
