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

st.title("🔬 Discretização e Topologia da Matriz Global")
st.markdown("""
**Objetivo:** Demonstrar o impacto do refinamento da malha ($h$-refinement) na estrutura da Matriz de Rigidez ($K$).
*Base Teórica: Bathe (2014) e Zienkiewicz (2013).*
""")

# Sidebar para controle da banca
st.sidebar.header("Configurações do Modelo")
L = st.sidebar.slider("Comprimento da Barra (L)", 1.0, 10.0, 5.0)
EA = st.sidebar.number_input("Rigidez Axial (EA)", value=1000.0)
n_el = st.sidebar.select_slider(
    "Número de Elementos (n_el)",
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
    ax.set_title(f"Malha com {n_el} elementos | h = {le:.3f} m")
    ax.axis('off')
    st.pyplot(fig)

    st.markdown(f"**Graus de Liberdade (GDL):** {n_nodes}")
    
    if n_el <= 8:
        st.write("### Matriz Numérica $[K]$")
        st.dataframe(K.astype(float))
    else:
        st.info("A matriz excedeu o limite de visualização tabular. Verifique o padrão de esparsidade ao lado.")

with col2:
    st.subheader("Sparsity Pattern (Esparsidade)")
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    
    # Plot da estrutura da matriz
    sns.heatmap(K, annot=(n_el <= 8), fmt=".0f", cmap="Blues", cbar=False, ax=ax2, 
                linewidths=0.5 if n_el <= 16 else 0)
    ax2.set_title(f"Estrutura da Matriz Global {n_nodes}x{n_nodes}")
    st.pyplot(fig2)

# Seção de Fundamentação Matemática (Uso de Raw Strings para evitar SyntaxWarning)
st.divider()
st.subheader("Análise de Rigidez e Condicionamento")

c1, c2 = st.columns(2)
with c1:
    st.write("**Formulação de Equilíbrio:**")
    st.latex(r"\{F\} = [K] \{U\}")
    st.write("**Matriz do Elemento:**")
    st.latex(r"k_e = \frac{EA}{l_e} \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}")

with c2:
    # Cálculo do número de condicionamento (cond)
    cond_number = np.linalg.cond(K)
    st.write("**Número de Condicionamento:**")
    st.latex(r"\kappa(K) = ||K|| \cdot ||K^{-1}||")
    st.metric("Valor Calculado", f"{cond_number:.2e}")

st.markdown("""
> **Observação para a Banca:** Note que o aumento do número de elementos reduz o erro de truncamento da solução física, mas o **número de condicionamento** aumenta, tornando o sistema mais sensível a erros numéricos de precisão finita. Em problemas 1D, a matriz é estritamente tridiagonal, resultando em uma banda constante.
""")