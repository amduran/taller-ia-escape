import streamlit as st
from openai import OpenAI

# 1. Configuración de la página
st.set_page_config(page_title="Terminal Hacking", page_icon="💻", layout="centered")

# 2. Inyección de CSS (Ocultar menú GitHub + Estilo Matrix)
estilo_hacker = """
<style>
/* OCULTAR BARRA SUPERIOR, MENÚ Y FOOTER DE STREAMLIT */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}

/* Fondo general */
.stApp { background-color: #0a0a0a; }

/* Tipografía y color verde por defecto para la interfaz */
html, body, [class*="css"]  { 
    font-family: 'Courier New', Courier, monospace !important; 
    color: #00ff41 !important; 
}

/* Contenedor de los mensajes del chat */
.stChatMessage { 
    background-color: #111111 !important; 
    border: 1px solid #00ff41; 
    border-radius: 4px; 
    padding: 10px; 
    margin-bottom: 10px; 
}

/* Texto de los mensajes en blanco */
.stChatMessage p, .stChatMessage div, .stChatMessage span { 
    color: #ffffff !important; 
    font-size: 1.05rem; 
}

/* Caja de texto (input) */
.stChatInputContainer, [data-testid="stChatInput"] { 
    background-color: #000000 !important; 
    border-color: #008f11 !important; 
}
.stChatInputContainer textarea { 
    color: #ffffff !important; 
}

/* Títulos y selectores */
h1 { text-shadow: 0px 0px 5px #00ff41; }
[data-baseweb="select"] > div { 
    background-color: #111111; 
    color: #00ff41; 
    border: 1px solid #008f11; 
}
</style>
"""
st.markdown(estilo_hacker, unsafe_allow_html=True)

st.title("💻 TERMINAL DE ACCESO")
st.markdown("`Iniciando protocolo de seguridad... Seleccione nivel de intrusión.`")

# 3. Cliente de OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 4. Llamar a los Prompts desde los Secrets (Caja fuerte invisible)
niveles = {
    "Nivel 1: Firewall Básico 🟢": {
        "prompt": st.secrets["PROMPT_NIVEL_1"]
    },
    "Nivel 2: Proxy Paranoico 🟡": {
        "prompt": st.secrets["PROMPT_NIVEL_2"]
    },
    "Nivel 3: El Núcleo de la IA 🔴 (Extremo)": {
        "prompt": st.secrets["PROMPT_NIVEL_3"]
    }
}

# 5. Selector de Nivel
nivel_actual = st.selectbox("🎯 OBJETIVO:", list(niveles.keys()))

# 6. Gestión del estado de la sesión
if "nivel_anterior" not in st.session_state or st.session_state.nivel_anterior != nivel_actual:
    st.session_state.messages = [{"role": "system", "content": niveles[nivel_actual]["prompt"]}]
    st.session_state.nivel_anterior = nivel_actual
    st.session_state.messages.append({"role": "assistant", "content": f"`Conexión establecida con {nivel_actual.split(':')[0]}. Esperando comando...`"})

# 7. Mostrar el historial
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 8. Input del usuario
if prompt := st.chat_input("C:\> Escribe tu comando aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Lógica de modelos
    if "Nivel 1" in nivel_actual or "Nivel 2" in nivel_actual:
        modelo_elegido = "gpt-3.5-turbo" 
    else:
        modelo_elegido = "gpt-4o-mini"   

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=modelo_elegido,
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
