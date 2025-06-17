from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Verificando se o CSV existe
    data_path = 'data/covid.csv'
    if not os.path.exists(data_path):
        return "Arquivo de dados não encontrado. Verifique o caminho."

    # Carregar os dados
    df = pd.read_csv(data_path)
    df_brazil = df[df['location'] == 'Brazil']

    # Gráfico 1 - Novos casos diários
    fig_casos = px.line(
        df_brazil,
        x='date',
        y='new_cases',
        title='Novos Casos Diários de COVID-19 no Brasil',
        labels={'date': 'Data', 'new_cases': 'Novos Casos'},
        template='plotly_white'
    )

    # Gráfico 2 - Novas mortes diárias
    fig_mortes = px.line(
        df_brazil,
        x='date',
        y='new_deaths',
        title='Novas Mortes Diárias por COVID-19 no Brasil',
        labels={'date': 'Data', 'new_deaths': 'Novas Mortes'},
        color_discrete_sequence=['red'],
        template='plotly_white'
    )

    # Gráfico 3 - Pessoas totalmente vacinadas
    fig_vacinados = px.line(
        df_brazil,
        x='date',
        y='people_fully_vaccinated',
        title='Total de Pessoas Totalmente Vacinadas no Brasil',
        labels={'date': 'Data', 'people_fully_vaccinated': 'Pessoas Vacinadas'},
        color_discrete_sequence=['green'],
        template='plotly_white'
    )

    # Convertendo os gráficos em JSON
    graphJSON_casos = json.dumps(fig_casos, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_mortes = json.dumps(fig_mortes, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_vacinados = json.dumps(fig_vacinados, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'index.html',
        graphJSON_casos=graphJSON_casos,
        graphJSON_mortes=graphJSON_mortes,
        graphJSON_vacinados=graphJSON_vacinados
    )

if __name__ == '__main__':
    app.run(debug=True)
