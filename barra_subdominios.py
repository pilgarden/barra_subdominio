import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página para visualização técnica
st.set_page_config(page_title="Análise Numérica: Refinamento-h", layout="wide")

# Estilização customizada para ambiente acadêmico
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMarkdown h1 { color: #1e293b; border-bottom: 2px solid #6366f1; padding-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("Discretização da matriz global")
st.markdown("""
**Objetivo:** Demonstrar o impacto do refinamento da malha ($h$-refinement) na estrutura da matriz de rigidez $[K]$.
*Usar unidades consistentes.
""")

# Sidebar para controle da banca
st.sidebar.header("Configurações do Modelo")
# L = st.sidebar.slider("Comprimento da Barra (L)", 1.0, 10.0, 5.0)
#L =  st.sidebar.select_slider("Comprimento da Barra (mm)",options=[1000, 2000,3000,4000,5000,6000,7000,8000,9000,10000])
L = st.sidebar.number_input("Comprimento da Barra (L)", value=200_000)
# EA = st.sidebar.number_input("Rigidez Axial (EA)", value=1000.0)
E = st.sidebar.number_input("Módulo de elasticidade (E)", value=200_000)
A = st.sidebar.number_input("Área da seção transversal (A)", value=90_000)
EA = E*A
n_el = st.sidebar.select_slider(
    "Número de Elementos ($n_{el}$)",
    options=[1, 2, 4, 8, 16, 32, 64]
)

# Algoritmo de Montagem (MEF 1D)
def assemble_matrix(L, EA, n_el):
    n_nodes = n_el + 1
    le = L / n_el
    # Matriz de rigidez local do elemento de barra
    ke = (EA / le) * np.array([[1, -1], [-1, 1]])
    
    K_global = np.zeros((n_nodes, n_nodes))
    
    # Processo de espalhamento (Scatter)
    for i in range(n_el):
        K_global[i:i+2, i:i+2] += ke
        
    return K_global, le

K, le = assemble_matrix(L, EA, n_el)
n_nodes = n_el + 1

# Interface de Resultados
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Discretização do Domínio")
    fig, ax = plt.subplots(figsize=(8, 2))
    
    x_nodes = np.linspace(0, L, n_nodes)
    ax.plot(x_nodes, np.zeros_like(x_nodes), 's-', color='#6366f1', markersize=6, linewidth=2)
    
    # Identificação dos nós (apenas se houver poucos para não poluir)
    if n_el <= 16:
        for i, x in enumerate(x_nodes):
            ax.text(x, 0.1, f"{i}", ha='center', fontsize=8, color='#1e293b')
    
    ax.set_ylim(-0.5, 0.5)
    ax.set_title(f"Malha com {n_el} elementos | h = {le:.0f} mm")
    ax.axis('off')
    st.pyplot(fig)

    st.markdown(f"**Graus de Liberdade (GDL):** {n_nodes}")
    
    if n_el <= 8:
        st.write("### Matriz Numérica $[K]$")
        st.dataframe(K.astype(float))
    else:
        st.info("A matriz excedeu o limite de visualização tabular. Verifique o padrão de esparsidade ao lado.")

with col2:
    st.subheader(f"Estrutura da Matriz Global {n_nodes}x{n_nodes}")
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    
    # Plot da estrutura da matriz
    sns.heatmap(K, annot=(n_el <= 8), fmt=".0f", cmap="Blues", cbar=False, ax=ax2, 
                linewidths=0.5 if n_el <= 16 else 0)
    st.pyplot(fig2)
