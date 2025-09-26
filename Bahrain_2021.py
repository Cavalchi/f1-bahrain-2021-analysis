# rodar no terminal para instalar a biblioteca fastf1 pip install fastf1
import fastf1 as ff1
from fastf1 import plotting
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import os

cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)


# Carregando a sessão e os pilotos que queremos**
race = ff1.get_session(2021, 'Bahrain', 'R')
race.load()

# Tempos de volta de Hamilton e Verstappen
laps_ham = race.laps.pick_driver('HAM')
laps_ver = race.laps.pick_driver('VER')

#  Filtrando os dados completos, para somente os que serão analisados/trabalhados

laps_ham = race.laps.pick_driver('HAM')
laps_ver = race.laps.pick_driver('VER')

laps_ham_filtered = laps_ham[['LapNumber', 'Stint', 'LapTime', 'Compound','PitOutTime', 'PitInTime', 'TyreLife']].copy()
laps_ver_filtered = laps_ver[['LapNumber', 'Stint', 'LapTime', 'Compound','PitOutTime', 'PitInTime', 'TyreLife']].copy()

# Convertendo LapTime para segundos

laps_ham_filtered['LapTimeSeconds'] = laps_ham_filtered['LapTime'].dt.total_seconds()
laps_ver_filtered['LapTimeSeconds'] = laps_ver_filtered['LapTime'].dt.total_seconds()


print(laps_ham_filtered)
print('-' * 80)
print(laps_ver_filtered)


# CALCULANDO O TEMPO MÉDIO DOS STINTS




media_stint1_ham = laps_ham_filtered[(laps_ham_filtered['LapNumber'] >= 1) & (laps_ham_filtered['LapNumber'] <= 13)]['LapTimeSeconds'].mean()
media_stint2_ham = laps_ham_filtered[(laps_ham_filtered['LapNumber'] >= 14) & (laps_ham_filtered['LapNumber'] <= 28)]['LapTimeSeconds'].mean()
media_stint3_ham = laps_ham_filtered[(laps_ham_filtered['LapNumber'] >= 29) & (laps_ham_filtered['LapNumber'] <= 56)]['LapTimeSeconds'].mean()
# --------------------------------------------------------------------------------------------------------------------------------------------
media_stint1_ver = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 1) & (laps_ver_filtered['LapNumber'] <= 18)]['LapTimeSeconds'].mean()
media_stint2_ver = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 19) & (laps_ver_filtered['LapNumber'] <= 40)]['LapTimeSeconds'].mean()
media_stint3_ver = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 41) & (laps_ver_filtered['LapNumber'] <= 56)]['LapTimeSeconds'].mean()
# --------------------------------------------------------------------------------------------------------------------------------------------

print(f"Ritmo Médio do Hamilton primeiro stint (Voltas 1-13): {media_stint1_ham:.3f} segundos")
print(f"Ritmo Médio do Hamilton segundo stint (Voltas 14-28): {media_stint2_ham:.3f} segundos")
print(f"Ritmo Médio do Hamilton terceiro stint (Voltas 29-56): {media_stint3_ham:.3f} segundos")
print('-'* 80)
print(f"Ritmo Médio do Verstappen primeiro stint (Voltas 1-18): {media_stint1_ver:.3f} segundos")
print(f"Ritmo Médio do Verstappen segundo stint (Voltas 19-40): {media_stint2_ver:.3f} segundos")
print(f"Ritmo Médio do Verstappen terceiro stint (Voltas 41-56): {media_stint3_ver:.3f} segundos")


# **COMPARAÇÃO DE STINT ENTRE HAMILTON E VERSTAPPEN**
diferenca_stint1 = abs(media_stint1_ham - media_stint1_ver)
vencedor_stint1 = "Hamilton" if media_stint1_ham < media_stint1_ver else "Verstappen"
print(f"No Stint 1, o piloto mais rápido foi {vencedor_stint1} por uma média de {diferenca_stint1:.3f} segundos mais rápido.")
print('-'* 90)

diferenca_stint2 = abs(media_stint2_ham - media_stint2_ver)
vencedor_stint2 = "Hamilton" if media_stint2_ham < media_stint2_ver else "Verstappen"
print(f"No Stint 2, o piloto mais rápido foi {vencedor_stint2} por uma média de {diferenca_stint2:.3f} segundos mais rápido.")
print('-'* 90)

diferenca_stint3 = abs(media_stint3_ham - media_stint3_ver)
vencedor_stint3 = "Hamilton" if media_stint3_ham < media_stint3_ver else "Verstappen"
print(f"No Stint 3, o piloto mais rápido foi {vencedor_stint3} por uma média de {diferenca_stint3:.3f} segundos mais rápido.")

# ANÁLISE NOS PITSTOPS PARA ENTENDERMOS A EFICÁCIA DA PARADA E A INFLUÊNCIA NA CORRIDA

pit_entry_ham = laps_ham[laps_ham['PitInTime'].notna()].copy()
pit_exit_ham = laps_ham[laps_ham['PitOutTime'].notna()].copy()

pit_entry_ver = laps_ver[laps_ver['PitInTime'].notna()].copy()
pit_exit_ver = laps_ver[laps_ver['PitOutTime'].notna()].copy()

pit_stops_data = []

# parada do Hamilton
for i in range(len(pit_entry_ham)):
    entry_lap = pit_entry_ham.iloc[i]
    exit_lap = pit_exit_ham.iloc[i]

    pit_duration = (exit_lap['PitOutTime'] - entry_lap['PitInTime']).total_seconds()
    pit_stops_data.append({'Driver': 'HAM', 'PitStopNumber': i + 1, 'PitEntryLap': entry_lap['LapNumber'], 'PitExitLap': exit_lap['LapNumber'], 'PitDuration': pit_duration})

# parada do Verstappen
for i in range(len(pit_entry_ver)):
    entry_lap = pit_entry_ver.iloc[i]
    exit_lap = pit_exit_ver.iloc[i]

    pit_duration = (exit_lap['PitOutTime'] - entry_lap['PitInTime']).total_seconds()
    pit_stops_data.append({'Driver': 'VER', 'PitStopNumber': i + 1, 'PitEntryLap': entry_lap['LapNumber'], 'PitExitLap': exit_lap['LapNumber'], 'PitDuration': pit_duration})

pit_stops_df = pd.DataFrame(pit_stops_data)


print("-" * 80  )
#  ANÁLISE DAS PARADAS DE PIT STOP
print("Análise das Paradas de Pit Stop:")

for driver in ['HAM', 'VER']:
    driver_pit_stops = pit_stops_df[pit_stops_df['Driver'] == driver]
    if not driver_pit_stops.empty:
        print(f"\n{driver}:")
        for index, row in driver_pit_stops.iterrows():
            print(f"  Parada {int(row['PitStopNumber'])} (Volta Entrada: {int(row['PitEntryLap'])}, Volta Saída: {int(row['PitExitLap'])}): {row['PitDuration']:.3f} segundos")
    else:
        print(f"\n{driver}: Sem dados de pit stop")

print("-" * 80  )

# Comparando as durações das paradas
if len(pit_stops_df) >= 2:
    primeira_parada_ham = pit_stops_df[(pit_stops_df['Driver'] == 'HAM') & (pit_stops_df['PitStopNumber'] == 1)]
    primeira_parada_ver = pit_stops_df[(pit_stops_df['Driver'] == 'VER') & (pit_stops_df['PitStopNumber'] == 1)]

    if not primeira_parada_ham.empty and not primeira_parada_ver.empty:
        pit_duration_ham_1 = primeira_parada_ham.iloc[0]['PitDuration']
        pit_duration_ver_1 = primeira_parada_ver.iloc[0]['PitDuration']
        diferenca_pit_duration_1 = abs(pit_duration_ham_1 - pit_duration_ver_1)
        vencedor_pit_duration_1 = "Hamilton" if pit_duration_ham_1 < pit_duration_ver_1 else "Verstappen"
        print(f"Comparação da Primeira Parada: A duração do pit stop de {vencedor_pit_duration_1} foi {diferenca_pit_duration_1:.3f}s mais rápida.")
    else:
        print("Não foi possível comparar a primeira parada devido a dados ausentes para um ou ambos os pilotos.")


    segunda_parada_ham = pit_stops_df[(pit_stops_df['Driver'] == 'HAM') & (pit_stops_df['PitStopNumber'] == 2)]
    segunda_parada_ver = pit_stops_df[(pit_stops_df['Driver'] == 'VER') & (pit_stops_df['Driver'] == 'VER') & (pit_stops_df['PitStopNumber'] == 2)]

    if not segunda_parada_ham.empty and not segunda_parada_ver.empty:
        pit_duration_ham_2 = segunda_parada_ham.iloc[0]['PitDuration']
        pit_duration_ver_2 = segunda_parada_ver.iloc[0]['PitDuration']
        diferenca_pit_duration_2 = abs(pit_duration_ham_2 - pit_duration_ver_2)
        vencedor_pit_duration_2 = "Hamilton" if pit_duration_ham_2 < pit_duration_ver_2 else "Verstappen"
        print(f"Comparação da Segunda Parada: A duração do pit stop de {vencedor_pit_duration_2} foi {diferenca_pit_duration_2:.3f}s mais rápida.")
    else:
        print("Não foi possível comparar a segunda parada devido a dados ausentes para um ou ambos os pilotos.")

else:
    print("Não há dados suficientes para comparar as paradas de pit stop de ambos os pilotos.")

# CÁLCULO DE DIFERENÇA DE TEMPO TOTAL ENTRE AS DUAS VOLTAS CONSIDERANDO O TEMPO TOTAL DO BOX

pit_entry_ham = laps_ham[laps_ham['PitInTime'].notna()].copy()
pit_exit_ham = laps_ham[laps_ham['PitOutTime'].notna()].copy()
pit_entry_ver = laps_ver[laps_ver['PitInTime'].notna()].copy()
pit_exit_ver = laps_ver[laps_ver['PitOutTime'].notna()].copy()

print("-" * 80)
print("Análise da Diferença entre Tempo de Volta e Duração do Pit Stop:")


if len(pit_entry_ham) > 0 and len(pit_exit_ham) > 0:
    ham_pit1_entry_lap = pit_entry_ham.iloc[0]
    ham_pit1_exit_lap = pit_exit_ham.iloc[0]

    if pd.notna(ham_pit1_entry_lap['LapTime']) and pd.notna(ham_pit1_exit_lap['LapTime']):
        ham_lap_time_diff_pit1 = (ham_pit1_exit_lap['LapTime'] - ham_pit1_entry_lap['LapTime']).total_seconds()
        ham_pit_duration_1 = (ham_pit1_exit_lap['PitOutTime'] - ham_pit1_entry_lap['PitInTime']).total_seconds()
        ham_difference_metric_pit1 = ham_lap_time_diff_pit1 - ham_pit_duration_1

        print(f"\nHamilton Primeira Parada (Volta Entrada: {int(ham_pit1_entry_lap['LapNumber'])}, Volta Saída: {int(ham_pit1_exit_lap['LapNumber'])}):")
        print(f"  Diferença no Tempo de Volta (Saída - Entrada): {ham_lap_time_diff_pit1:.3f} segundos")
        print(f"  Duração Calculada do Pit Stop (PitOut - PitIn): {ham_pit_duration_1:.3f} segundos")
        print(f"  Diferença entre Métricas: {ham_difference_metric_pit1:.3f} segundos")
    else:
        print("\nHamilton Primeira Parada: Dados de tempo de volta ausentes para cálculo da diferença de tempo de volta.")
else:
    print("\nHamilton Primeira Parada: Dados de pit stop ausentes.")

print()
print("-" * 80)

if len(pit_entry_ver) > 0 and len(pit_exit_ver) > 0:
    ver_pit1_entry_lap = pit_entry_ver.iloc[0]
    ver_pit1_exit_lap = pit_exit_ver.iloc[0]

    if pd.notna(ver_pit1_entry_lap['LapTime']) and pd.notna(ver_pit1_exit_lap['LapTime']):
        ver_lap_time_diff_pit1 = (ver_pit1_exit_lap['LapTime'] - ver_pit1_entry_lap['LapTime']).total_seconds()
        ver_pit_duration_1 = (ver_pit1_exit_lap['PitOutTime'] - ver_pit1_entry_lap['PitInTime']).total_seconds()
        ver_difference_metric_pit1 = ver_lap_time_diff_pit1 - ver_pit_duration_1

        print(f"\nVerstappen Primeira Parada (Volta Entrada: {int(ver_pit1_entry_lap['LapNumber'])}, Volta Saída: {int(ver_pit1_exit_lap['LapNumber'])}):")
        print(f"  Diferença no Tempo de Volta (Saída - Entrada): {ver_lap_time_diff_pit1:.3f} segundos")
        print(f"  Duração Calculada do Pit Stop (PitOut - PitIn): {ver_pit_duration_1:.3f} segundos")
        print(f"  Diferença entre Métricas: {ver_difference_metric_pit1:.3f} segundos")
    else:
        print("\nVerstappen Primeira Parada: Dados de tempo de volta ausentes para cálculo da diferença de tempo de volta.")
else:
    print("\nVerstappen Primeira Parada: Dados de pit stop ausentes.")
print()
print("-" * 80)

if len(pit_entry_ham) > 1 and len(pit_exit_ham) > 1:
    ham_pit2_entry_lap = pit_entry_ham.iloc[1]
    ham_pit2_exit_lap = pit_exit_ham.iloc[1]

    if pd.notna(ham_pit2_entry_lap['LapTime']) and pd.notna(ham_pit2_exit_lap['LapTime']):
        ham_lap_time_diff_pit2 = (ham_pit2_exit_lap['LapTime'] - ham_pit2_entry_lap['LapTime']).total_seconds()
        ham_pit_duration_2 = (ham_pit2_exit_lap['PitOutTime'] - ham_pit2_entry_lap['PitInTime']).total_seconds()
        ham_difference_metric_pit2 = ham_lap_time_diff_pit2 - ham_pit_duration_2

        print(f"\nHamilton Segunda Parada (Volta Entrada: {int(ham_pit2_entry_lap['LapNumber'])}, Volta Saída: {int(ham_pit2_exit_lap['LapNumber'])}):")
        print(f"  Diferença no Tempo de Volta (Saída - Entrada): {ham_lap_time_diff_pit2:.3f} segundos")
        print(f"  Duração Calculada do Pit Stop (PitOut - PitIn): {ham_pit_duration_2:.3f} segundos")
        print(f"  Diferença entre Métricas: {ham_difference_metric_pit2:.3f} segundos")
    else:
        print("\nHamilton Segunda Parada: Dados de tempo de volta ausentes para cálculo da diferença de tempo de volta.")
else:
    print("\nHamilton Segunda Parada: Dados de pit stop ausentes.")

print()
print("-" * 80)
# Verstappen's second pit stop
if len(pit_entry_ver) > 1 and len(pit_exit_ver) > 1:
    ver_pit2_entry_lap = pit_entry_ver.iloc[1]
    ver_pit2_exit_lap = pit_exit_ver.iloc[1]

    if pd.notna(ver_pit2_entry_lap['LapTime']) and pd.notna(ver_pit2_exit_lap['LapTime']):
        ver_lap_time_diff_pit2 = (ver_pit2_exit_lap['LapTime'] - ver_pit2_entry_lap['LapTime']).total_seconds()
        ver_pit_duration_2 = (ver_pit2_exit_lap['PitOutTime'] - ver_pit2_entry_lap['PitInTime']).total_seconds()
        ver_difference_metric_pit2 = ver_lap_time_diff_pit2 - ver_pit_duration_2

        print(f"\nVerstappen Segunda Parada (Volta Entrada: {int(ver_pit2_entry_lap['LapNumber'])}, Volta Saída: {int(ver_pit2_exit_lap['LapNumber'])}):")
        print(f"  Diferença no Tempo de Volta (Saída - Entrada): {ver_lap_time_diff_pit2:.3f} segundos")
        print(f"  Duração Calculada do Pit Stop (PitOut - PitIn): {ver_pit_duration_2:.3f} segundos")
        print(f"  Diferença entre Métricas: {ver_difference_metric_pit2:.3f} segundos")
    else:
        print("\nVerstappen Segunda Parada: Dados de tempo de volta ausentes para cálculo da diferença de tempo de volta.")
else:
    print("\nVerstappen Segunda Parada: Dados de pit stop ausentes.")

# CRIANDO O GRÁFICO DE RITMO

all_laps = pd.concat([laps_ham, laps_ver]).reset_index(drop=True)

all_laps_filtered = all_laps[['Driver', 'LapNumber', 'LapTime', 'Position']].dropna(subset=['LapTime']).copy()

all_laps_filtered['LapTimeSeconds'] = all_laps_filtered['LapTime'].dt.total_seconds()

team_colors = {
    'HAM': '#00D7B6',  # Cor Mercedes
    'VER': '#0600EF'   # Cor Red-Bull
}

fig_plotly = px.line(all_laps_filtered,
                    x='LapNumber',
                    y='LapTimeSeconds',
                    color='Driver',
                    title='Análise de Ritmo de Volta por Piloto - GP do Bahrein 2021',
                    labels={'LapNumber': 'Número da Volta', 'LapTimeSeconds': 'Tempo de Volta (segundos)'},
                    color_discrete_map=team_colors)


fig_plotly.update_layout( hovermode="x unified" )
fig_plotly.show()
fig_plotly.write_html("bahrein_jp_plotly.html")

print("Gráfico interativo salvo como bahrein_jp_plotly.html")

# GRAFICO DE POSIÇÃO



fig_position = px.line( all_laps_filtered,
                       x='LapNumber',
                       y='Position',
                       color='Driver',
                       title='Evolução da Posição dos Pilotos - GP do Bahrein 2021')


fig_position.update_layout( hovermode="x unified" )
fig_position.update_layout(yaxis=dict(autorange="reversed"))
fig_position.show()
fig_position.write_html("bahrein_positions_plotly.html")
#print("Gráfico interativo de posições salvo como bahrein_positions_plotly.html")


df = laps_ham_filtered

specific_laps_by_index = df.loc[[5, 10, 15], ['LapNumber', 'LapTime']]
print("Specific laps by index (5, 10, 15):")
print(specific_laps_by_index)
laps_49_to_56_ver = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 49) & (laps_ver_filtered['LapNumber'] <= 56)]['LapTimeSeconds']

sum_laps_49_to_56_ver = laps_49_to_56_ver.sum()
# print(f"\nSoma dos tempos de volta do Verstappen (Voltas 49-56): {sum_laps_49_to_56_ver:.3f} segundos")

if not laps_49_to_56_ver.empty:
    diff_fastest_slowest_ver = laps_49_to_56_ver.max() - laps_49_to_56_ver.min()
    print(f"Diferença entre a volta mais rápida e mais lenta do Verstappen (Voltas 49-56): {diff_fastest_slowest_ver:.3f} segundos")

    # Anaisando progresso das últimas voltas
    print("\nProgressão do Tempo de Volta do Verstappen (Voltas 49-56):")
    for i in range(len(laps_49_to_56_ver) - 1):
        lap_current = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 49) & (laps_ver_filtered['LapNumber'] <= 56)]['LapNumber'].iloc[i] # Get actual lap number
        lap_next = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 49) & (laps_ver_filtered['LapNumber'] <= 56)]['LapNumber'].iloc[i+1] # Get actual lap number
        time_current = laps_49_to_56_ver.iloc[i]
        time_next = laps_49_to_56_ver.iloc[i+1]
        difference = time_next - time_current

        if difference > 0:
            print(f"Volta {int(lap_current)} para Volta {int(lap_next)}: O tempo aumentou em {difference:.3f} segundos.")
        elif difference < 0:
            print(f"Volta {int(lap_current)} para Volta {int(lap_next)}: O tempo diminuiu em {abs(difference):.3f} segundos.")
        else:
            print(f"Volta {int(lap_current)} para Volta {int(lap_next)}: O tempo permaneceu o mesmo.")

else:
    print("Não há dados de tempo de volta para o Verstappen nas voltas 49-56.")


# **VERSTAPPEN Estava constantemente fazendo tempos menores que Hamilton, por pneus mais novos e pela abertura do DRS, em 2 voltas ele conseguiria fazer uma ultrapassagem limpa**


media_finallap_ham = laps_ham_filtered[(laps_ham_filtered['LapNumber'] >= 56)]['LapTimeSeconds'].mean()

media_final_ver = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 55) & (laps_ver_filtered['LapNumber'] <= 56)]['LapTimeSeconds'].mean()


print('-'*80)

print(f"Ritmo Médio do Verstappen (Voltas 54-59): {media_final_ver:.3f} segundos")
print('-'*80)

distancia = media_finallap_ham - media_final_ver

print(f"A distância média das ultimas voltas entre os dois de segundos era de: {distancia:.3f}")


# **Na última volta, Verstappen estava a baixo por 272 milésimos de segundos**

# Considerando também  o tempo de volta de Hamilton, Verstappen estava baixando 272 milésimos por volta enquanto hamilton estava perdendo quanto por volta?



media_final_ham = laps_ham_filtered[(laps_ham_filtered['LapNumber'] >= 54) & (laps_ham_filtered['LapNumber'] <= 56)]['LapTimeSeconds'].mean()
media_final_ver = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 54) & (laps_ver_filtered['LapNumber'] <= 56)]['LapTimeSeconds'].mean()


print(f"Ritmo Médio do Hamilton final (Voltas 54-56): {media_final_ham:.3f} segundos")
print('-'*80)
print(f"Ritmo Médio do Verstappen final (Voltas 54-56): {media_final_ver:.3f} segundos")
print('-'*80)


distancia_final = media_final_ham - media_final_ver

print(f"distancia media das ultimas voltas: {distancia_final:.3f}")


print('-'*80)

laps_ham_last_laps = laps_ham_filtered[(laps_ham_filtered['LapNumber'] >= 53) & (laps_ham_filtered['LapNumber'] <= 56)]['LapTimeSeconds']

print("Diferença de tempo entre voltas consecutivas do Hamilton (Voltas 53-56):")
for i in range(len(laps_ham_last_laps) - 1):
    lap_current = laps_ham_filtered[laps_ham_filtered['LapNumber'] >= 53]['LapNumber'].iloc[i]
    lap_next = laps_ham_filtered[laps_ham_filtered['LapNumber'] >= 53]['LapNumber'].iloc[i+1]
    time_current = laps_ham_last_laps.iloc[i]
    time_next = laps_ham_last_laps.iloc[i+1]
    difference = time_next - time_current

    if difference > 0:
        print(f"Volta {int(lap_current)} para Volta {int(lap_next)}: O tempo aumentou em {difference:.3f} segundos.")
    elif difference < 0:
        print(f"Volta {int(lap_current)} para Volta {int(lap_next)}: O tempo diminuiu em {abs(difference):.3f} segundos.")
    else:
        print(f"Volta {int(lap_current)} para Volta {int(lap_next)}: O tempo permaneceu o mesmo.")

# Diferença de tempo na volta 56 (Hamilton na frente)
diferenca_volta_56 = 0.745 # segundos, conforme a sua observação de 700 milésimos

# Diferença média de ritmo por volta (Verstappen mais rápido)
diferenca_ritmo_por_volta = 0.272  # segundos, conforme a sua observação de 272 milésimos

# Quanto Hamilton perde por volta em relação a Verstappen (conforme sua observação de 104 milésimos)
perca_ritmo_hamilton = 0.104 # segundos

# Diferença líquida de tempo ganho por Verstappen por volta
ganho_por_volta_verstappen = diferenca_ritmo_por_volta + perca_ritmo_hamilton

# Calcular quantas voltas adicionais seriam necessárias para Verstappen compensar a diferença
voltas_para_ultrapassar = diferenca_volta_56 / ganho_por_volta_verstappen

print(f"Considerando a diferença de 0.745s na volta 56 e um ganho líquido de {ganho_por_volta_verstappen:.3f}s por volta para Verstappen, seriam necessárias aproximadamente {voltas_para_ultrapassar:.2f} voltas adicionais para o Verstappen ultrapassar o Hamilton.")


# **Vamos criar uma hipótese onde Verstappen reagiu mais rápido ao box antecipado de Hamilton e decidiu parar na volta 15 em vez da volta 18**

cumulative_time_ham_lap_16 = laps_ham_filtered[laps_ham_filtered['LapNumber'] <= 16]['LapTimeSeconds'].sum()

print(f"Tempo total de Hamilton até a volta 16: {cumulative_time_ham_lap_16:.3f} segundos")

## Calculando o tempo total hipotético de verstappen até a volta 16 com pit stop antecipado

# Somar o tempo das voltas 1 a 14 de Verstappen
sum_laps_1_to_14_ver = laps_ver_filtered[laps_ver_filtered['LapNumber'] <= 14]['LapTimeSeconds'].sum()

# Estimar o tempo normal de volta de Verstappen para a volta 15 (usando a média de suas voltas antes de seu primeiro pit stop)
# O primeiro pit stop de Verstappen foi na volta 17 (volta de entrada)
ritmo_medio_ver_antes_pit_original = laps_ver_filtered[laps_ver_filtered['LapNumber'] <= 16]['LapTimeSeconds'].mean()

# Obter a duração real do primeiro pit stop de Verstappen
duracao_pit_ver = pit_stops_df[(pit_stops_df['Driver'] == 'VER') & (pit_stops_df['PitStopNumber'] == 1)]['PitDuration'].iloc[0]

# Calcular o tempo hipotético de Verstappen até o final da volta 16 com um pit stop na volta 15
# Isso inclui as voltas 1-14 (normais), volta 15 (entrada no box + duração do pit stop + saída do box) e volta 16 (tempo de volta normal)
# Usaremos o tempo estimado de volta normal para a volta 15 como base para o impacto da entrada/saída do box.
# O tempo hipotético da volta 15 com pit = tempo estimado de volta normal + duração do pit - delta normal do pit
# Uma estimativa aproximada para o delta normal do pit pode ser tirada da diferença entre o tempo de volta e a duração do pit para suas voltas de pit stop reais.
# De cálculos anteriores, ver_difference_metric_pit1 foi -8.523 segundos para sua primeira volta de pit stop (entrada na volta 17, saída na volta 18)
# Isso significa que a volta do pit foi 8.523 segundos mais lenta do que uma volta 'normal' mais a duração do pit.
# Então, um tempo de volta normal é aproximadamente tempo de volta do pit - duração do pit + 8.523
# Tempo da volta de entrada no box 17 foi 99.153, tempo da volta de saída do box 18 foi 115.532. Duração do pit foi 24.902
# ver_lap_time_diff_pit1 (volta 18 - volta 17) = 16.379
# ver_difference_metric_pit1 = ver_lap_time_diff_pit1 - ver_pit_duration_1 = 16.379 - 24.902 = -8.523
# Tempo estimado para a volta 15 se fosse uma volta de pit = tempo estimado da volta normal 15 + duração do pit + o tempo perdido devido à entrada/saída do box em comparação com uma volta normal
# O tempo perdido em comparação com uma volta normal é aproximadamente a duração do pit mais a métrica de diferença.
# Tempo perdido na volta do pit em comparação com a volta normal = Duração do Pit + (Tempo da Volta do Pit - Duração do Pit) -> Isso não está correto
# Tempo perdido na volta do pit em comparação com a volta normal = Tempo da Volta do Pit - Tempo da Volta Normal
# De antes, Tempo da Volta do Pit (volta 17 para VER) = 99.153. Tempo da volta normal antes do pit (média até a volta 16) é 96.782
# Tempo perdido na volta 17 devido à entrada no box: 99.153 - 96.782 = 2.371 segundos
# O tempo da volta de saída do box 18 foi 115.532.
# O tempo total perdido durante uma sequência de pit stop (volta de entrada, pit stop, volta de saída) em comparação com duas voltas normais.
# Para o primeiro pit stop de VER (entrada na volta 17, saída na volta 18, duração do pit 24.902):
# Tempo da volta 17: 99.153
# Tempo da volta 18: 115.532
# Tempo total para as voltas 17 e 18: 99.153 + 115.532 = 214.685 segundos
# Duas voltas normais (usando a média até a volta 16, 96.782): 2 * 96.782 = 193.564 segundos
# Tempo total perdido na sequência do pit: 214.685 - 193.564 = 21.121 segundos
# Estes 21.121 segundos incluem a duração do pit de 24.902 segundos.

# Recalculando com base no tempo total:
# Tempo para as voltas 1-14 (real) + Tempo para a volta 15 (volta hipotética do pit) + Tempo para a volta 16 (real)
# O tempo para uma volta de pit é o tempo que leva desde cruzar a linha de partida/chegada até entrar no pit lane, percorrer o pit lane (duração do pit), e sair do pit lane para cruzar a linha de partida/chegada novamente.
# O tempo perdido em uma volta de pit em comparação com uma volta normal é aproximadamente a duração do pit mais o tempo perdido desacelerando e acelerando.
# Vamos usar o tempo real da volta de entrada no box (volta 17 para VER) como uma estimativa para a duração de uma volta de entrada no box.
ver_lap_17_time = laps_ver_filtered[laps_ver_filtered['LapNumber'] == 17]['LapTimeSeconds'].iloc[0]
# E o tempo real da volta de saída do box (volta 18 para VER) como uma estimativa para a duração de uma volta de saída do box.
ver_lap_18_time = laps_ver_filtered[laps_ver_filtered['LapNumber'] == 18]['LapTimeSeconds'].iloc[0]

# Tempo hipotético para a volta 15 (entrada no box + pit stop + saída do box):
# Isso é complicado porque a duração do pit stop é medida de PitIn a PitOut, o que acontece *dentro* da volta.
# O tempo total para a volta do pit (volta 15 no cenário hipotético) seria o tempo na pista antes do PitIn + Duração do Pit + tempo na pista após o PitOut.
# Uma aproximação mais simples é pegar o tempo da volta de entrada no box (tempo real da volta 17) e adicionar a duração do pit stop. Isso não está completamente certo, pois conta duas vezes o tempo do pit lane.

# Vamos voltar à ideia do tempo total perdido na sequência do pit stop.
# Tempo total para duas voltas normais = 2 * ritmo_medio_ver_antes_pit_original
# Tempo total para a volta de entrada no box (17) + volta de saída do box (18) + duração do pit = ver_lap_17_time + ver_lap_18_time + duracao_pit_ver
# Não, a duração do pit faz parte do tempo de volta.

# Vamos usar o tempo total do início até o final da volta 16 no cenário hipotético.
# Isso é a soma de:
# Voltas 1-14 (tempos reais)
# Volta 15 (tempo hipotético da volta do pit)
# Volta 16 (tempo hipotético após o pit stop)

# Tempo hipotético da volta 15 (volta do pit): Podemos aproximar isso pegando o tempo médio da volta normal antes do pit e adicionando a duração do pit, mas subtraindo o tempo economizado cortando a curva/pit lane. Uma maneira mais precisa é considerar a perda total de tempo de uma sequência de pit stop.
# O tempo total perdido ao fazer um pit stop (em comparação com duas voltas normais) é aproximadamente a duração do pit mais o tempo perdido entrando e saindo.
# Vamos usar a duração do pit e a métrica de diferença. A métrica de diferença (-8.523) é a diferença entre (Diferença do Tempo de Volta) e a Duração do Pit.
# Diferença do Tempo de Volta (Volta 18 - Volta 17) = 16.379. Duração do Pit = 24.902. Métrica de Diferença = -8.523.
# Isso significa que Volta 18 - Volta 17 = 16.379.
# Vamos usar o tempo total perdido pela sequência do pit stop em comparação com duas voltas normais.
# Tempo para a volta 17 + Tempo para a volta 18 (sequência real do pit) = 99.153 + 115.532 = 214.685
# Tempo para duas voltas normais (média até a volta 16) = 2 * 96.782 = 193.564
# Tempo total perdido na sequência do pit = 214.685 - 193.564 = 21.121 segundos ao longo de duas voltas.
# Isso não parece certo, pois a duração do pit é 24.902. Isso implicaria que houve ganho de tempo na entrada/saída.

# Vamos reavaliar a métrica de diferença:
# Diferença no Tempo de Volta (Saída - Entrada) = 16.379 (tempo da Volta 18 - tempo da Volta 17)
# Duração Calculada do Pit Stop (PitOut - PitIn) = 24.902
# Diferença entre Métricas = -8.523
# Esta métrica de diferença significa que o aumento no tempo de volta durante a sequência do pit (da volta 17 para a volta 18) foi 8.523 segundos *menor* que a duração do pit. Isso é confuso.

# Vamos simplificar e considerar o tempo perdido por pit stop. Uma aproximação comum é duração do pit + tempo perdido na entrada/saída.
# Vamos assumir que o tempo total perdido por evento de pit stop (em comparação com uma volta normal) é a duração do pit mais a métrica de diferença.
# Tempo perdido por evento de pit stop = 24.902 + (-8.523) = 16.379 segundos. Este é o tempo perdido em *uma* volta (a volta do pit) em comparação com uma volta normal, incluindo o pit stop em si. Isso parece mais razoável.

# Então, o tempo hipotético da volta 15 (volta do pit) = tempo estimado da volta normal 15 + 16.379
hypothetical_lap_15_pit_time_alt = ritmo_medio_ver_antes_pit_original + (duracao_pit_ver + ver_difference_metric_pit1) # Usando a métrica de diferença diretamente como o tempo adicional perdido

# Vamos usar a abordagem mais simples das instruções:
# Somar as voltas 1-14 (real)
# Adicionar o tempo hipotético da volta 15 (tempo estimado da volta normal + duração do pit) - Isso não está correto, pois não considera a desaceleração/aceleração.
# Adicionar o tempo real da volta 16 (já que ele estaria fora dos boxes)

# Vamos usar a duração do pit e assumir que a entrada/saída do box adiciona uma quantidade fixa de tempo em relação a uma volta normal.
# A volta de entrada no box (volta 17, 99.153s) é 99.153 - 96.782 = 2.371s mais lenta que uma volta normal.
# A volta de saída do box (volta 18, 115.532s) é 115.532 - 96.782 = 18.75s mais lenta que uma volta normal.
# Tempo extra total ao longo de duas voltas (entrada e saída) em comparação com duas voltas normais = 2.371 + 18.75 = 21.121 segundos.
# Estes 21.121 segundos são o tempo extra *além* do tempo que levaria para dirigir duas voltas normais.
# A duração do pit stop em si é 24.902 segundos.

# Vamos calcular o tempo total para as voltas 15 e 16 no cenário hipotético:
# A volta 15 é a volta do pit. Tempo para a volta 15 = tempo estimado da volta normal 15 + tempo perdido devido à entrada no box + duração do pit + tempo perdido devido à saída do box (até a linha de partida/chegada)
# Isso está ficando complicado. Vamos voltar às instruções e interpretar o passo 4 cuidadosamente:
# 4. Calcular o tempo hipotético de Verstappen até o final da volta 16, assumindo um pit stop na volta 15. Somar o tempo total das voltas 1 a 14, o tempo estimado da volta 15 (como uma volta de entrada no box), a duração do pit stop, e o tempo real da volta 16.

# Soma das voltas 1-14 (real)
# Tempo estimado da volta 15 (como uma volta de entrada no box): Usar o tempo real da volta 17 como uma estimativa para o tempo de uma volta de entrada no box.
# Duração do pit stop: Usar a duração real do primeiro pit stop dele.
# Tempo real da volta 16: Obter o tempo real da volta 16 para Verstappen.

sum_laps_1_to_14_ver = laps_ver_filtered[laps_ver_filtered['LapNumber'] <= 14]['LapTimeSeconds'].sum()
estimated_lap_15_pit_entry_time = laps_ver_filtered[laps_ver_filtered['LapNumber'] == 17]['LapTimeSeconds'].iloc[0] # Usando a volta real 17 como estimativa
real_lap_16_time_ver = laps_ver_filtered[laps_ver_filtered['LapNumber'] == 16]['LapTimeSeconds'].iloc[0]
duracao_pit_ver = pit_stops_df[(pit_stops_df['Driver'] == 'VER') & (pit_stops_df['PitStopNumber'] == 1)]['PitDuration'].iloc[0]

# Tempo hipotético total até o final da volta 16 = Soma das voltas 1-14 + Tempo Estimado da Volta de Entrada no Box 15 + Duração do Pit Stop + Tempo Real da Volta 16
# Isso ainda não parece certo. A duração do pit está *dentro* das voltas de entrada/saída.

# Vamos tentar outra abordagem baseada na perda total de tempo.
# Tempo total para as voltas 15 e 16 na corrida original = laps_ver_filtered[laps_ver_filtered['LapNumber'].isin([15, 16])]['LapTimeSeconds'].sum()
# Tempo total para as voltas 15 e 16 no cenário hipotético (Volta 15 é a volta do pit, Volta 16 é a primeira volta fora):
# Volta 15 (volta do pit): Usar o tempo real da volta de entrada no box (volta 17) + o tempo perdido na saída do box.
# Tempo perdido na volta de saída do box (volta 18) em comparação com uma volta normal = 115.532 - 96.782 = 18.75.
# Tempo hipotético da volta 15 do pit = tempo da volta 17 de ver + tempo perdido na saída do box? Não, isso não está correto.

# Vamos voltar à duração do pit e ao conceito de tempo perdido por evento de pit stop.
# Tempo perdido por evento de pit stop = duração do pit + tempo perdido entrando/saindo em relação a uma volta normal.
# Vamos usar a média dos tempos das voltas de entrada e saída do box como uma estimativa para o tempo de uma volta de pit.
# Tempo médio da volta do pit para VER = (tempo da volta 17 de ver + tempo da volta 18 de ver) / 2 = (99.153 + 115.532) / 2 = 107.3425


# Tempo acumulado até o final da volta 14 (real)
# Tempo acumulado até o final da volta 15 (pit hipotético): Tempo acumulado até o final da volta 14 + tempo hipotético da volta 15 do pit
# Tempo acumulado até o final da volta 16 (hipotético após o pit): Tempo acumulado até o final da volta 15 + tempo real da volta 16

# Calcular o tempo acumulado até o final da volta 14 (real)
cumulative_time_ver_lap_14 = laps_ver_filtered[laps_ver_filtered['LapNumber'] <= 14]['LapTimeSeconds'].sum()

# Estimar o tempo hipotético da volta 15 do pit: Vamos usar a média dos tempos reais das voltas de entrada (volta 17) e saída (volta 18) do box como uma estimativa para a duração da volta hipotética do pit (volta 15).
hypothetical_lap_15_pit_time_avg = (laps_ver_filtered[laps_ver_filtered['LapNumber'] == 17]['LapTimeSeconds'].iloc[0] + laps_ver_filtered[laps_ver_filtered['LapNumber'] == 18]['LapTimeSeconds'].iloc[0]) / 2

# Calcular o tempo acumulado até o final da volta 15 (pit hipotético)
cumulative_time_ver_lap_15_hypothetical = cumulative_time_ver_lap_14 + hypothetical_lap_15_pit_time_avg

# Obter o tempo real da volta 16 para Verstappen (esta seria sua primeira volta fora dos boxes no cenário hipotético)
real_lap_16_time_ver = laps_ver_filtered[laps_ver_filtered['LapNumber'] == 16]['LapTimeSeconds'].iloc[0]

# Calcular o tempo hipotético total até o final da volta 16
hypothetical_total_time_ver_lap_16 = cumulative_time_ver_lap_15_hypothetical + real_lap_16_time_ver

print(f"Soma dos tempos de volta de Verstappen (Voltas 1-14): {sum_laps_1_to_14_ver:.3f} segundos")
print(f"Ritmo Médio de Verstappen antes do Pit Stop (até volta 16): {ritmo_medio_ver_antes_pit_original:.3f} segundos")
print(f"Duração real da primeira parada de Pit Stop de Verstappen: {duracao_pit_ver:.3f} segundos")
print(f"Tempo real da volta 16 de Verstappen: {real_lap_16_time_ver:.3f} segundos")
print(f"Tempo hipotético da volta 15 (volta do pit) usando média de voltas 17 e 18: {hypothetical_lap_15_pit_time_avg:.3f} segundos")
print(f"Tempo cumulativo de Verstappen até o final da volta 14 (real): {cumulative_time_ver_lap_14:.3f} segundos")
print(f"Tempo cumulativo de Verstappen até o final da volta 15 (pit hipotético): {cumulative_time_ver_lap_15_hypothetical:.3f} segundos")
print(f"Tempo hipotético total de Verstappen até o final da volta 16 (pit na volta 15): {hypothetical_total_time_ver_lap_16:.3f} segundos")

# Obter o tempo total real de Hamilton até o final da volta 16 a partir do resultado da subtarefa anterior
# A variável cumulative_time_ham_lap_16 já contém este valor.

# Calcular a diferença de tempo entre o tempo hipotético de Verstappen e o tempo real de Hamilton no final da volta 16
diff_at_end_of_lap_16 = hypothetical_total_time_ver_lap_16 - cumulative_time_ham_lap_16

print(f"Tempo real total de Hamilton até o final da volta 16: {cumulative_time_ham_lap_16:.3f} segundos")
print(f"Tempo hipotético total de Verstappen até o final da volta 16 (pit na volta 15): {hypothetical_total_time_ver_lap_16:.3f} segundos")
print(f"Diferença de tempo no final da volta 16 (Verstappen - Hamilton): {diff_at_end_of_lap_16:.3f} segundos")

## Projetar a diferença de tempo para o final da corrida

# Excluir voltas de pit stop
laps_ham_post_pit1 = laps_ham_filtered[(laps_ham_filtered['LapNumber'] >= 17) & (laps_ham_filtered['LapNumber'] <= 56)].copy()
laps_ham_post_pit1 = laps_ham_post_pit1[laps_ham_post_pit1['PitInTime'].isna() & laps_ham_post_pit1['PitOutTime'].isna()].copy()
avg_lap_time_ham_post_pit1 = laps_ham_post_pit1['LapTimeSeconds'].mean()


# No cenário hipotético, o pit stop de Verstappen ocorreu na volta 15. O ritmo após a volta 16 seria similar ao ritmo real dele após o pit stop real (volta 19).
# Calcular o ritmo médio real de Verstappen das voltas 19 a 56.
laps_ver_post_pit_original = laps_ver_filtered[(laps_ver_filtered['LapNumber'] >= 19) & (laps_ver_filtered['LapNumber'] <= 56)].copy()
laps_ver_post_pit_original = laps_ver_post_pit_original[laps_ver_post_pit_original['PitInTime'].isna() & laps_ver_post_pit_original['PitOutTime'].isna()].copy()
avg_lap_time_ver_post_pit_hypothetical = laps_ver_post_pit_original['LapTimeSeconds'].mean()

# Diferença = Ritmo Verstappen - Ritmo Hamilton (para saber quanto Verstappen ganha/perde por volta)
lap_time_difference_per_lap = avg_lap_time_ver_post_pit_hypothetical - avg_lap_time_ham_post_pit1

#  Multiplicar a diferença média de ritmo pelo número de voltas restantes (56 - 16 = 40 voltas) para projetar a mudança total na diferença de tempo.
remaining_laps = 56 - 16
projected_time_change = lap_time_difference_per_lap * remaining_laps

# Adicionar a diferença de tempo projetada à diferença de tempo na volta 16 para estimar a diferença de tempo no final da corrida.
projected_diff_end_of_race = diff_at_end_of_lap_16 + projected_time_change

print(f"Ritmo médio de Hamilton (Voltas 17-56, excluindo pit): {avg_lap_time_ham_post_pit1:.3f} segundos")
print(f"Ritmo médio de Verstappen (Voltas 19-56, excluindo pit - ritmo hipotético pós pit na volta 15): {avg_lap_time_ver_post_pit_hypothetical:.3f} segundos")
print(f"Diferença média de ritmo por volta (Verstappen - Hamilton): {lap_time_difference_per_lap:.3f} segundos")
print(f"Voltas restantes após a volta 16: {remaining_laps}")
print(f"Mudança total de tempo projetada no restante da corrida: {projected_time_change:.3f} segundos")
print(f"Diferença de tempo no final da volta 16 (Verstappen - Hamilton): {diff_at_end_of_lap_16:.3f} segundos")
print(f"Diferença de tempo projetada no final da corrida (Verstappen - Hamilton): {projected_diff_end_of_race:.3f} segundos")




