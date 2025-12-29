import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Dashboard RH Intelligente",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f3c88;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2d4da3;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 10px;
    }
    .stProgress .st-bo {
        background-color: #1f3c88;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

# ======================================
# GESTION DE SESSION
# ======================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.profil = None
    st.session_state.messages = []
    st.session_state.kpis_data = None
    st.session_state.last_refresh = None


def logout():
    st.session_state.authenticated = False
    st.session_state.profil = None
    st.session_state.messages = []
    st.session_state.kpis_data = None

def refresh_kpis():
    try:
        r = requests.get(f"{BACKEND_URL}/kpis/", timeout=60)
        if r.status_code == 200:
            st.session_state.kpis_data = r.json()
            st.session_state.last_refresh = datetime.now().strftime("%H:%M:%S")
        else:
            st.error("Erreur lors de la récupération des données")
    except Exception as e:
        st.error(f"Erreur de connexion au serveur: {e}")

# ======================================
# PAGE DE CONNEXION
# ======================================
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1000/1000946.png", width=150)
        st.markdown('<h1 class="main-header">🔐 Connexion </h1>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown("")
            identifiant = st.text_input("**Identifiant**", placeholder="Votre identifiant")
            mdp = st.text_input("**Mot de passe**", type="password", placeholder="Votre mot de passe")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚀 Se connecter", use_container_width=True):
                    try:
                        r = requests.post(
                            f"{BACKEND_URL}/login/",
                            json={"identifiant": identifiant, "mdp": mdp},
                            timeout=60
                        )
                        res = r.json()
                        
                        if res.get("success"):
                            st.session_state.authenticated = True
                            st.session_state.profil = res["profil"]
                            st.session_state.messages = []
                            st.rerun()
                        else:
                            st.error("❌ Identifiants incorrects")
                    except Exception as e:
                        st.error(f"⚠️ Erreur de communication: {e}")
            
            with col_btn2:
                if st.button("🔄 Réinitialiser", use_container_width=True, type="secondary"):
                    st.rerun()
            
            st.markdown("---")
            st.caption("© 2024 Dashboard RH Intelligente - Version 2.0")
    
    st.stop()

# ======================================
# DASHBOARD RH (Accès admin)
# ======================================
if st.session_state.profil and st.session_state.profil.lower() == "rh":
    # Barre latérale
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1998/1998610.png", width=80)
        st.markdown(f"### 👋 Bienvenue, **{st.session_state.profil}**")
        st.markdown("---")
        
        if st.button("🔄 Actualiser les données", use_container_width=True, type="primary"):
            refresh_kpis()
            st.rerun()
        
        if st.session_state.last_refresh:
            st.caption(f"🕐 Dernière actualisation: {st.session_state.last_refresh}")
        
        st.markdown("---")
        
        st.markdown("### 📈 Filtres")
        period = st.selectbox(
            "Période d'analyse",
            ["Dernières 24h", "7 derniers jours", "30 derniers jours", "Tout"]
        )
        
        st.markdown("---")
        
        if st.button("🚪 Déconnexion", use_container_width=True, type="secondary"):
            logout()
            st.rerun()
        
        st.markdown("---")
        st.caption("**Support technique**:\nsupport@rh-dashboard.com")

    # Contenu principal
    st.markdown('<h1 class="main-header">📊 Tableau de Bord RH Intelligente</h1>', unsafe_allow_html=True)
    
    # En-tête avec métriques principales
    if st.session_state.kpis_data is None:
        refresh_kpis()
    
    if st.session_state.kpis_data:
        kpis = st.session_state.kpis_data
        
        # Métriques principales
        st.markdown("### 📈 KPIs Principaux")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            comprehension = kpis.get("Taux de compréhension (%)", 0)
            st.metric(
                label="🎯 Compréhension",
                value=f"{comprehension}%",
                delta=f"{comprehension - 85}%" if comprehension > 85 else None,
                delta_color="normal"
            )
            st.progress(comprehension / 100)
        
        with col2:
            correct = kpis.get("Taux de réponse correcte (%)", 0)
            st.metric(
                label="✅ Réponses Correctes",
                value=f"{correct}%",
                delta=f"{correct - 80}%" if correct > 80 else None
            )
            st.progress(correct / 100)
        
        with col3:
            escalation = kpis.get("Taux d’escalade (%)", 0)
            st.metric(
                label="📞 Taux d'Escalade",
                value=f"{escalation}%",
                delta=f"{15 - escalation}%" if escalation < 15 else f"+{escalation - 15}%",
                delta_color="inverse"
            )
            st.progress(escalation / 100)
        
        with col4:
            avg_time = kpis.get("Temps moyen de réponse (s)", 0)
            st.metric(
                label="⏱ Temps Moyen",
                value=f"{avg_time}s",
                delta=f"-{avg_time - 5}s" if avg_time > 5 else None,
                delta_color="inverse"
            )
        
        # Deuxième ligne de métriques
        st.markdown("### 📊 Métriques Supplémentaires")
        col5, col6, col7 = st.columns(3)
        
        with col5:
            st.markdown("""
            <div class="metric-card">
                <h3>👥 Utilisateurs Actifs</h3>
                <h2>{}</h2>
                <p>Profils connectés</p>
            </div>
            """.format(kpis.get("Profils connectés", 0)), unsafe_allow_html=True)
        
        with col6:
            domains = kpis.get("Répartition des domaines (%)", {})
            total_domains = len(domains)
            st.markdown(f"""
            <div class="metric-card">
                <h3>📚 Domaines Couverts</h3>
                <h2>{total_domains}</h2>
                <p>Catégories de questions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col7:
            top_domains = kpis.get("Classement des domaines", [])
            total_questions = sum(count for _, count in top_domains)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🗣️ Questions Total</h3>
                <h2>{total_questions}</h2>
                <p>Interactions traitées</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphiques
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("### 📊 Répartition des Domaines")
            if domains:
                # Préparation des données pour le graphique
                df_domains = pd.DataFrame(list(domains.items()), columns=['Domaine', 'Pourcentage'])
                fig1 = px.pie(
                    df_domains, 
                    values='Pourcentage', 
                    names='Domaine',
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                fig1.update_layout(height=400)
                st.plotly_chart(fig1, use_container_width=True)
        
        with col_chart2:
            st.markdown("### 🏆 Top 5 Domaines")
            if top_domains:
                top_5 = top_domains[:5]
                df_top = pd.DataFrame(top_5, columns=['Domaine', 'Questions'])
                fig2 = px.bar(
                    df_top,
                    x='Questions',
                    y='Domaine',
                    orientation='h',
                    color='Questions',
                    color_continuous_scale='Viridis'
                )
                fig2.update_layout(height=400, xaxis_title="Nombre de questions", yaxis_title="")
                st.plotly_chart(fig2, use_container_width=True)
    
    
    else:
        st.warning("⚠️ Aucune donnée disponible. Veuillez actualiser le dashboard.")
    
    st.stop()

# ======================================
# INTERFACE CHATBOT (Pour autres utilisateurs)
# ======================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.markdown(f"### 👤 Profil: **{st.session_state.profil}**")
    st.markdown("---")
    
    if st.button("🗑️ Effacer l'historique", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.info("""
    Ce chatbot RH peut vous aider avec:
    • Questions sur les congés
    • Informations salariales
    • Politiques d'entreprise
    • Formation et développement
    • Avantages sociaux
    """)

# Interface principale du chatbot
st.markdown('<h1 class="main-header">🤖 Assistant RH Intelligente</h1>', unsafe_allow_html=True)
st.markdown("Posez vos questions sur les ressources humaines en toute confidentialité.")

# Historique de conversation
chat_container = st.container()
with chat_container:
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(f'<div class="chat-message {msg["role"]}-message">{msg["content"]}</div>', unsafe_allow_html=True)

# Saisie utilisateur
if prompt := st.chat_input("💬 Tapez votre question RH ici..."):
    # Affichage du message utilisateur
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Réponse du chatbot avec animation
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analyse de votre question..."):
            try:
                r = requests.post(
                    f"{BACKEND_URL}/chat_messages/",
                    json={
                        "input_text": prompt,
                        "profil": st.session_state.profil
                    },
                    timeout=60
                )
                response = r.json().get("agent", "Désolé, je n'ai pas pu traiter votre demande.")
            except Exception as e:
                response = f"⚠️ Erreur de connexion au serveur: {str(e)}"
        
        st.markdown(f'<div class="chat-message bot-message">{response}</div>', unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Pied de page
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)
with col_footer1:
    st.caption("🛡️ Conversations sécurisées et cryptées")
with col_footer2:
    st.caption("⏱️ Temps de réponse moyen: < 5 secondes")
with col_footer3:
    if st.button("🔓 Déconnexion", use_container_width=True, type="secondary"):
        logout()
        st.rerun()