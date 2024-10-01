import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import timedelta, datetime

# Função para gerar gráfico de Gantt
def gerar_grafico_gantt(cronograma):
    fig = px.timeline(cronograma, x_start="Inicio", x_end="Fim", y="Nome", 
                      title="Cronograma de Obra - Gráfico Gantt",
                      labels={"Nome": "Atividades"})
    fig.update_yaxes(categoryorder="total ascending")
    return fig

# Inicializando o cronograma
if 'cronograma' not in st.session_state:
    st.session_state.cronograma = pd.DataFrame(columns=['Nome', 'Inicio', 'Fim', 'Predecessora', 'Sucessora'])

# Formulário para adicionar atividades
st.title("Cronograma de Obra")

with st.form("Atividade"):
    nome = st.text_input("Nome da atividade")
    duracao = st.number_input("Duração (dias)", min_value=1, step=1)
    predecessora = st.selectbox("Predecessora", options=['None'] + st.session_state.cronograma['Nome'].tolist())
    sucessora = st.text_input("Sucessora (opcional)")
    
    submitted = st.form_submit_button("Adicionar atividade")
    
    if submitted and nome:
        inicio = datetime.today()
        if predecessora != 'None':
            # Se houver predecessora, ajusta o início da atividade
            inicio = st.session_state.cronograma.loc[st.session_state.cronograma['Nome'] == predecessora, 'Fim'].values[0]
            inicio = pd.Timestamp(inicio)
        
        fim = inicio + timedelta(days=duracao)
        
        # Adiciona a atividade ao cronograma
        st.session_state.cronograma = st.session_state.cronograma.append({
            'Nome': nome,
            'Inicio': inicio,
            'Fim': fim,
            'Predecessora': predecessora,
            'Sucessora': sucessora
        }, ignore_index=True)

# Exibir cronograma atual
st.subheader("Cronograma Atual")
st.dataframe(st.session_state.cronograma)

# Exibir gráfico de Gantt
if not st.session_state.cronograma.empty:
    st.subheader("Gráfico de Gantt")
    fig = gerar_grafico_gantt(st.session_state.cronograma)
    st.plotly_chart(fig)
