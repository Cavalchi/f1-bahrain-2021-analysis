# 🏎️💨 Análise Estratégica e de Ritmo: GP do Bahrein de 2021

## 🤔 Sobre o Projeto

Este projeto oferece uma análise aprofundada do Grande Prêmio do Bahrein de 2021, com foco na intensa disputa entre Lewis Hamilton e Max Verstappen. Através da utilização de dados de telemetria e ferramentas de análise de dados em Python, exploramos as nuances da estratégia de corrida, o desempenho dos pneus e o impacto das paradas nos boxes.

O objetivo é ir além dos resultados superficiais, quantificando o ritmo de corrida dos pilotos em diferentes fases da prova e avaliando como as decisões estratégicas influenciaram o desfecho. Incluímos também uma simulação baseada em dados para contextualizar o quão próxima a batalha realmente foi nas voltas finais.

## ✨ Principais Insights e Descobertas:

*   **Performance por Stint:** Análise comparativa do ritmo médio de volta, destacando a superioridade de Verstappen em ritmo puro em todos os stints, especialmente no final da corrida.
*   **Eficiência dos Pit Stops:** Avaliação da duração das paradas nos boxes e sua contribuição para o tempo total de corrida de cada piloto.
*   **Momentos Críticos da Corrida:** Visualizações que ilustram a evolução da diferença de tempo e posição entre os líderes.
*   **Análise das Voltas Finais:** Uma quantificação da diferença de ritmo nas voltas decisivas e uma projeção do cenário hipotético caso a corrida se estendesse.

Este estudo demonstra a aplicação de análise e ciência de dados para extrair insights valiosos de impacto pequenos detalhes na estratégia e execução.

## 🛠️ Tecnologias Utilizadas

*   **Python**
*   `fastf1`
*   `pandas`
*   `matplotlib` & `plotly.express`

## 🚀  Este projeto exemplifica a capacidade de:

*   Trabalhar com dados complexos e de séries temporais.
*   Realizar análises comparativas e quantitativas.
*   Visualizar dados para comunicar insights de forma clara.
*   Aplicar raciocínio analítico para modelar cenários hipotéticos.

Fique à vontade para explorar o código e as análises detalhadas neste repositório!


### Neste projeto trabalhos com 2 cenários hipotéticos para entendermos, quantas voltas a mais de corrida seria necessário para Verstappen passar Hamilton?

**O Final e a Simulação Hipotética:** A corrida culminou em um final apertado, com Hamilton cruzando a linha de chegada apenas 0.700 segundos à frente de Verstappen. Nossa análise das últimas voltas revelou que, enquanto Verstappen mantinha um ritmo significativamente mais rápido (ganhando cerca de 0.376 segundos por volta, considerando a diferença de ritmo e a perda de ritmo do Hamilton), seriam necessárias aproximadamente **1.98 voltas adicionais** para que ele conseguisse compensar a diferença e efetuar a ultrapassagem em condições de corrida.

**Conclusão:** Os dados confirmam a performance superior do carro de Verstappen em termos de ritmo puro na maioria dos stints. No entanto, a gestão estratégica de Hamilton e a execução impecável em momentos cruciais garantiram a vitória em uma das corridas mais memoráveis dos últimos tempos. A simulação hipotética das voltas finais sublinha o quão perto Verstappen chegou de reverter o resultado, destacando a margem mínima que separou os dois competidores no Bahrein.


## No segundo cenário hipotético analisamos como uma possível para simulada 2 voltas mais cedo de Verstappen poderia ter mudado o resultado da corrida 

**Resultados Principais da Simulação (Pit Stop de Verstappen na Volta 15):**

*   **Diferença de Tempo no Final da Volta 16:** No cenário hipotético, ao final da volta 16 (Verstappen tendo acabado de sair dos boxes e Hamilton completando uma volta normal), Verstappen estaria aproximadamente **8.615 segundos à frente de Hamilton**. Este valor representa a diferença acumulada até este ponto, considerando o tempo gasto no pit stop.
*   **Diferença Média de Ritmo Projetada (Voltas 17-56):** Projetamos que, após a volta 16, Verstappen manteria um ritmo médio de volta aproximadamente **0.131 segundos mais rápido** que Hamilton (baseado no ritmo real de ambos após suas primeiras paradas).
*   **Mudança Total de Tempo Projetada (Voltas 17-56):** Ao longo das 40 voltas restantes da corrida (da volta 17 à volta 56), essa diferença de ritmo levaria a uma mudança total na diferença de tempo de aproximadamente **-5.246 segundos** (ganho para Verstappen).
*   **Diferença de Tempo Projetada no Final da Corrida:** Combinando a diferença na volta 16 com a mudança projetada, a diferença de tempo estimada no final da corrida seria de **-13.861 segundos** (Verstappen - Hamilton).

Antecipar o pit stop para a volta 15 teria colocado Verstappen em uma posição de liderança mais sólida no meio da corrida. Embora isso o colocasse em pneus mais velhos no final em comparação com Hamilton, o ritmo superior projetado no cenário hipotético parece ter sido suficiente para construir e manter uma vantagem significativa até a bandeira quadriculada.

**Suposições e Limitações da Simulação:**

É importante notar que esta simulação se baseia em algumas suposições:

*   **Ritmo Médio Constante:** Assumimos que o ritmo médio calculado após o pit stop inicial se manteria consistente para o restante da corrida, ignorando degradação de pneu variável, mudanças nas condições da pista ou voltas de tráfego.
*   **Duração do Pit Stop:** Utilizamos a duração real da primeira parada de Verstappen como base para a parada hipotética, assumindo que a equipe conseguiria replicar essa performance.


Apesar das simplificações, a análise fornece uma forte indicação de que uma estratégia de pit stop antecipada poderia ter sido vantajosa para Max Verstappen no GP do Bahrein de 2021, permitindo-lhe construir uma liderança que, com base no ritmo projetado, teria sido difícil para Hamilton superar.
