import streamlit as st
import json
import hashlib
import uuid
from datetime import datetime, timedelta

def gerar_id():
    return str(uuid.uuid4())

def criar_mandato(usuario, produtos, metodo_pagamento, tempo_exp=5):
    """
    Cria um mandato AP2 com assinatura simulada.
    """
    mandato = {
        "id_mandato": gerar_id(),
        "usuario": usuario,
        "produtos": produtos,
        "valor_total": sum(p["preco"] for p in produtos),
        "timestamp": datetime.utcnow().isoformat(),
        "expiracao": (datetime.utcnow() + timedelta(minutes=tempo_exp)).isoformat()
    }

    mandato_json = json.dumps(mandato, sort_keys=True)
    assinatura = hashlib.sha256(mandato_json.encode()).hexdigest()
    mandato["assinatura_usuario"] = assinatura
    return mandato

def gerar_fluxograma(valor_total):
    """
    Gera fluxograma Graphviz com nó AP2 colorido de acordo com o valor total.
    """
    if valor_total < 50:
        cor = "#7CFC00"  # verde claro
    elif valor_total <= 100:
        cor = "#FFD700"  # amarelo
    else:
        cor = "#FF4500"  # vermelho

    fluxograma = f"""
    flowchart LR
        Usuario[👤 Usuário] --> AgenteUsuario[🤖 Agente do Usuário]
        AgenteUsuario --> ComunicacaoA2A[🔗 Comunicação A2A]
        ComunicacaoA2A --> AcessoMCP[🛠️ Acesso a Recursos via MCP]
        AcessoMCP --> AgenteCompras[🛒 Agente de Compras]
        AgenteCompras --> MandatoAP2[💳 Mandato AP2: R$ {valor_total:.2f}{{bgcolor={cor}}}]
        MandatoAP2 --> BackendBFA[🗄️ Backend BFA]
        BackendBFA --> Comerciante[🏪 Comerciante]
        BackendBFA --> ProvedorCredenciais[🔑 Provedor de Credenciais]
        ProvedorCredenciais --> RedeBanco[🏦 Rede/Banco]
    """
    return fluxograma


st.set_page_config(page_title="Simulador AP2 Definitivo", layout="wide")
st.title("Simulador AP2 Interativo Definitivo")
st.markdown(
    """
    Adicione produtos e visualize **em tempo real**:
    - Mandato AP2 gerado automaticamente
    - Fluxograma do fluxo AP2 atualizado
    - Nó AP2 com cor dinâmica de acordo com o valor total
    """
)

if "produtos_adicionados" not in st.session_state:
    st.session_state["produtos_adicionados"] = []

produtos_adicionados = st.session_state["produtos_adicionados"]

with st.sidebar:
    st.subheader("Configuração do Usuário")
    usuario = st.text_input("Nome do Usuário", "Fala, IAzeiro!")
    metodo_pagamento = st.text_input("Token do Método de Pagamento", "token_cartao_1234")

    st.subheader("Adicionar Produto")
    nome_produto = st.text_input("Nome do Produto", key="nome_produto")
    preco_produto = st.number_input("Preço do Produto", min_value=0.0, step=0.01, key="preco_produto")

    if st.button("Adicionar Produto"):
        if nome_produto and preco_produto > 0:
            produtos_adicionados.append({"nome": nome_produto, "preco": preco_produto})
            st.session_state["produtos_adicionados"] = produtos_adicionados
            st.session_state["nome_produto"] = ""
            st.session_state["preco_produto"] = 0.0

st.subheader("Produtos Adicionados")
if produtos_adicionados:
    st.json(produtos_adicionados)
else:
    st.info("Nenhum produto adicionado ainda.")

if produtos_adicionados:
    mandato = criar_mandato(usuario, produtos_adicionados, metodo_pagamento)
    st.subheader("Mandato AP2 Gerado")
    st.json(mandato)

    valor_total = sum(p["preco"] for p in produtos_adicionados)
    fluxograma = gerar_fluxograma(valor_total)
    st.subheader("Fluxograma Dinâmico do Mandato AP2")
    st.graphviz_chart(fluxograma)
