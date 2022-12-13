import pandas as pd
from datetime import datetime, date
import time
import numpy as np
import matplotlib.pyplot as plt

def main():
    #Config Geral dos Gráficos
    plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = 12,9
    plt.tight_layout()

    #DataFrame de Horários e Tempos
    df = pd.read_excel('Horários de Estudo.xlsx', index_col='Dia')

    #Grupos
    estudo, prog = [df[df['Tipo'] == 'Estudo'], df[df['Tipo'] == 'Prog']]

    #---------------------------------------------------------------------ESTUDO---------------------------------------------------------------------#
    #Definição das Horas do Dia
    horarios = np.arange(-1, 24)
    to_string = np.vectorize(lambda x : str(x)+'h')
    horarios_str = to_string(horarios[1:])

    #Frequência de Cada Horário de Estudo
    freq_horarios_estudo = estudo.groupby(pd.cut(estudo['Início'].map(lambda x : (time.strptime(x, '%H:%M:%S')).tm_hour), bins=horarios, labels=horarios_str)).size().reset_index(name='Count')

    #Gráfico Frequência de Cada Horário de Estudo
    plt.bar(horarios_str, freq_horarios_estudo['Count'])
    plt.xticks(horarios_str, freq_horarios_estudo['Início'], rotation=45)
    plt.xlabel('Horário de Início')
    plt.ylabel('Ocorrências')
    plt.title('Frequência de cada Horário de Início')
    plt.savefig('Freq Horário de Início Estudo')

    #Definiçao de Faixas de Tempo de Estudo Corrido
    tempo = np.arange(-1, 6)
    tempo_str = to_string(tempo[1:])

    #Frequência de Tempo de Duração de Estudo Corrido
    freq_tempo_estudo = estudo.groupby(pd.cut(estudo['Delta (hh:min:seg)'].map(lambda x : (time.strptime(x, '%H:%M:%S')).tm_hour), bins=tempo, labels=tempo_str)).size().reset_index(name='Count')

    #Gráfico Frequência de Tempo de Duração de Estudo 
    plt.bar(tempo_str, freq_tempo_estudo['Count'])
    plt.xticks(tempo_str, freq_tempo_estudo['Delta (hh:min:seg)'], rotation=45)
    plt.xlabel('Tempo de Estudo Corrido')
    plt.ylabel('Ocorrências')
    plt.title('Frequência de Tempo de Estudo Corrido')
    plt.savefig('Freq Tempo de Estudo Corrido')

    #----------------------------------------------------------------------PROG----------------------------------------------------------------------#
    #Frequência de Cada Horário de Programação
    freq_horarios_prog = prog.groupby(pd.cut(prog['Início'].map(lambda x : (time.strptime(x, '%H:%M:%S')).tm_hour), bins=horarios, labels=horarios_str)).size().reset_index(name='Count')

    #Gráfico Frequência de Cada Horário de Programação
    plt.bar(horarios_str, freq_horarios_prog['Count'])
    plt.xticks(horarios_str, freq_horarios_prog['Início'], rotation=45)
    plt.xlabel('Horário de Início')
    plt.ylabel('Ocorrências')
    plt.title('Frequência de cada Horário de Início')
    plt.savefig('Freq Horário de Início Prog')

    #Frequência de Tempo de Duração de Programação Corrido
    freq_tempo_prog = prog.groupby(pd.cut(prog['Delta (hh:min:seg)'].map(lambda x : (time.strptime(x, '%H:%M:%S')).tm_hour), bins=tempo, labels=tempo_str)).size().reset_index(name='Count')

    #Gráfico Frequência de Tempo de Duração de Programação 
    plt.bar(tempo_str, freq_tempo_prog['Count'])
    plt.xticks(tempo_str, freq_tempo_prog['Delta (hh:min:seg)'], rotation=45)
    plt.xlabel('Tempo de Programação Corrido')
    plt.ylabel('Ocorrências')
    plt.title('Frequência de Tempo de Programação Corrido')
    plt.savefig('Freq Tempo de Prog Corrido')

if __name__ == '__main__':
    main()