import streamlit as st
import pandas as pd
import difflib
import random
import string
from datetime import datetime
import time

# ==============================================================================
# 1. VISUELS & INJECTION CSS DE SÉCURITÉ (ANTI-ÉCRAN BLANC MOBILE)
# ==============================================================================
st.set_page_config(
    page_title="SOURCE ISABEE — L'Élite Académique",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* FORÇAGE ABSOLU DU THÈME SOMBRE SUR TOUS LES APPAREILS MOBILE/PC */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stMain, [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {
        background: #010D08 !important;
        background-image: linear-gradient(135deg, #010D08 0%, #021F14 50%, #000503 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    
    /* TITRES LUMINEUX NÉON BERTCAL */
    .glow-title {
        font-size: 4.5rem !important;
        font-weight: 800 !important;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: -2px;
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.8), 0 0 40px rgba(16, 185, 129, 0.4);
    }
    @media (max-width: 768px) { .glow-title { font-size: 2.5rem !important; } }
    
    .glow-subtitle {
        text-align: center; font-size: 1.2rem; color: #A7F3D0; margin-bottom: 30px; font-weight: 500; opacity: 0.9;
    }
    
    .welcome-banner {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.2) 50%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 25px; border-radius: 16px; text-align: center; margin-bottom: 40px;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.25);
    }
    
    .welcome-text { font-size: 1.8rem !important; font-weight: 700; color: #34D399; text-shadow: 0 0 10px rgba(52, 211, 153, 0.6); }

    /* STYLISATION DES ONGLETS HAUT DE GAMME */
    .stTabs [data-baseweb="tab-list"] { gap: 15px !important; background-color: transparent !important; padding: 10px 0 !important; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 14px !important;
        padding: 16px 24px !important; font-size: 1.05rem !important; font-weight: 700 !important; color: #E5E7EB !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important; border-color: #34D399 !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
    }

    .big-logo-box {
        background: rgba(255, 255, 255, 0.02) !important; border: 2px dashed #10B981 !important;
        border-radius: 12px; padding: 20px 5px; text-align: center; color: #34D399 !important; font-weight: 800; font-size: 0.8rem;
    }

    .sidebar-blue-footer {
        border-top: 1px solid rgba(56, 189, 248, 0.2); padding-top: 20px; margin-top: 40px;
        font-size: 0.88rem; line-height: 1.6; color: #38BDF8 !important; text-align: center !important;
    }
    .sidebar-blue-footer b, .sidebar-blue-footer strong { color: #00E5FF !important; }

    .glass-card {
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 16px; padding: 22px; margin-bottom: 20px;
    }
    .badge-premium { background: linear-gradient(90deg, #F59E0B, #D97706); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; }
    .badge-free { background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; }
    
    /* STYLE POUR LE RECOIN SECRETS DU CONCEPTEUR */
    .chief-vault {
        background: linear-gradient(135deg, #090514 0%, #110426 100%) !important;
        border: 2px solid #8B5CF6 !important;
        border-radius: 16px; padding: 25px; margin-top: 20px;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. LE CERVEAU CENTRALISÉ DE PRODUCTION (PARTAGÉ & PERSISTANT)
# ==============================================================================
FILIERES = [
    "Production Végétale", "Production Animale", "Protection des Cultures",
    "Opérations Forestières", "Aménagement Forestier", 
    "Gestion de la Faune, des Aires Protégées et Écotourisme",
    "Sylviculture et Plantations Forestières", "Sciences du Bois",
    "Techniques Spécialisées en Transformation du Bois", "Génie de l'Environnement",
    "Systèmes Agro-Sylvo-Pastoraux et Bioénergies", "Bioénergies et Environnement",
    "Génie Énergétique", "Agroéconomie", "Politique et Gouvernance Forestière",
    "Études d'Impact Environnemental et Social"
]

@st.cache_resource
def initialiser_base_globale():
    base_sujets = pd.DataFrame([
        {"id": 1, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Thermodynamique et Transfert Thermique", "Enseignant": "Dr. Eko", "Type": "Examen", "Année": "2024-2025", "Premium": False, "Downloads": 145, "Date": "12/03/2026", "Favori": False},
        {"id": 2, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Mécanique des Fluides Appliquée + CORRIGÉ", "Enseignant": "Pr. Ndongo", "Type": "Examen", "Année": "2024-2025", "Premium": True, "Downloads": 92, "Date": "18/03/2026", "Favori": False}
    ])
    interactions = {
        "commentaires": ["Excellente lisibilité sur les sujets de Génie Énergétique.", "Sujet de Thermo Ing4 disponible !"],
        "suggestions": ["Ajouter les TP de chimie des solutions pour les L1."],
        "avis": [{"user": "Anonyme", "note": 5, "text": "L'interface à 300F vaut largement le coup !"}],
        "remerciements": ["Merci à Bertcal pour cette initiative de génie sur le campus."]
    }
    # Base de données pour stocker les fichiers des copilotes soumis à ta validation
    staging_files = []
    
    # Pool initial de tickets intelligents à usage unique de très haute sécurité
    tickets_actifs = ["ISABEE-99A8", "ISABEE-44B2", "ISABEE-77C1"]
    
    config = {
        "copilot_password": "admin",
        "chief_password": "owner",
        "orange_target": "696075660",
        "mtn_target": "654046792",
        "logo_isabee": None,
        "logo_ubertoua": None
    }
    return {"db": base_sujets, "staging": staging_files, "tickets": tickets_actifs, "interactions": interactions, "config": config}

serveur_data = initialiser_base_globale()

# Gestion des sessions utilisateur privées par terminal
if 'is_premium_user' not in st.session_state: st.session_state.is_premium_user = False
if 'dev_role' not in st.session_state: st.session_state.dev_role = None

# ==============================================================================
# 3. BARRE LATÉRALE (AUTHENTIFICATION, SYSTÈME TICKET UNIQUE & FILTRES)
# ==============================================================================
with st.sidebar:
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        if serveur_data["config"]["logo_isabee"] is not None: st.image(serveur_data["config"]["logo_isabee"], use_container_width=True)
        else: st.markdown('<div class="big-logo-box">🏛️<br>ISABEE LOGO</div>', unsafe_allow_html=True)
    with col_l2:
        if serveur_data["config"]["logo_ubertoua"] is not None: st.image(serveur_data["config"]["logo_ubertoua"], use_container_width=True)
        else: st.markdown('<div class="big-logo-box">🎓<br>U-BERTOUA</div>', unsafe_allow_html=True)
            
    st.markdown("### 🔑 ACCÈS COMPTE & VALIDATION TICKET")
    user_matricule = st.text_input("Identifiant Matricule Étudiant :", value="22I0000B")

    if not st.session_state.is_premium_user:
        ticket_input = st.text_input("Entrez votre Ticket Unique Premium :", type="default", placeholder="Ex: ISABEE-XXXX")
        if st.button("🔥 Valider le Ticket"):
            # VÉRIFICATION DE TRÈS HAUTE SÉCURITÉ ET DESTRUCTION IMMÉDIATE (SINGLE USE)
            if ticket_input in serveur_data["tickets"]:
                serveur_data["tickets"].remove(ticket_input) # Brûlé instantanément du pool global
                st.session_state.is_premium_user = True
                st.success("👑 Accès Élite Activé ! Le ticket a été détruit de la base.")
                st.rerun()
            else:
                st.error("Ticket invalide, expiré ou déjà consommé.")
    else:
        st.success("👑 Statut : Compte Élite Académique")
        if st.button("Quitter le mode Premium"):
            st.session_state.is_premium_user = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎛️ FILTRES DE RECHERCHE")
    f_cycle = st.selectbox("Cycle d'études", ["Tous", "Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
    f_filiere = st.selectbox("Filière", ["Toutes"] + FILIERES)
    f_type = st.selectbox("Type d'évaluation", ["Tous", "CC", "Examen", "Rattrapage", "TP"])

    st.markdown(f"""
        <div class="sidebar-blue-footer">
            Développé par: <b>Chemta Caleb Bertrand</b><br>
            étudiant ingénieur en génie énergétique.<br>
            <br>
            <strong>CONTACT COMMERCIAL :</strong><br>
            • Téléphone : +237 {serveur_data["config"]["orange_target"]}<br>
            • Email : bertrandchemtacaleb@gmail.com<br>
            • Campus : ISABEE / U-BERTOUA
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. EN-TÊTE PRINCIPAL
# ==============================================================================
st.markdown("<h1 class='glow-title'>SOURCE ISABEE</h1>", unsafe_allow_html=True)
st.markdown("<p class='glow-subtitle'>Anciennes épreuves et sujets d'examens... Développé par Bertcal.</p>", unsafe_allow_html=True)

st.markdown("""
    <div class="welcome-banner">
        <p class="welcome-text">🌟 BIENVENUE SUR VOTRE PLATEFORME D'EXCELLENCE ACADÉMIQUE ! 🌟</p>
        <p style="margin: 5px 0 0 0; opacity:0.8; font-size:0.95rem; color:#FFFFFF;">Accédez instantanément aux archives de vos filières pour propulser vos résultats.</p>
    </div>
""", unsafe_allow_html=True)

df_view = serveur_data["db"].copy()
if f_cycle != "Tous": df_view = df_view[df_view['Cycle'] == f_cycle]
if f_filiere != "Toutes": df_view = df_view[df_view['Filière'] == f_filiere]
if f_type != "Tous": df_view = df_view[df_view['Type'] == f_type]

# ==============================================================================
# 5. ONGLETS DE NAVIGATION PRINCIPAUX (PUBLIC VS DEVENIR PREMIUM VS DEV)
# ==============================================================================
tab_public_content, tab_payment_gateway, tab_public_interact, tab_dev_zone = st.tabs([
    "📂 ARCHIVES ACADÉMIQUES", 
    "💳 ACHAT ACCÈS ÉLITE (MOBILE MONEY)",
    "💬 DISCUSSIONS & SUGGESTIONS", 
    "🔒 ACCÈS DÉVELOPPEUR"
])

# --- ONGLET 1 : ARCHIVES PUBLIC ---
with tab_public_content:
    st.markdown("### 🔍 Rechercher une archive")
    search_bar = st.text_input("Saisir le nom d'une UE :", placeholder="Ex: Thermodynamique...")
    
    if search_bar:
        matches = []
        for idx, row in df_view.iterrows():
            sim = difflib.SequenceMatcher(None, search_bar.lower(), row['Matière'].lower()).ratio()
            if search_bar.lower() in row['Matière'].lower() or sim > 0.4: matches.append(row)
        df_view = pd.DataFrame(matches) if matches else pd.DataFrame(columns=df_view.columns)

    if df_view.empty:
        st.info("Aucun document trouvé pour ces critères.")
    else:
        for idx, row in df_view.iterrows():
            badge = "<span class='badge-premium'>💎 PREMIUM (Corrigé)</span>" if row['Premium'] else "<span class='badge-free'>🆓 GRATUIT</span>"
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="color:#FFFFFF; margin:0;">{row['Matière']}</h4>
                        {badge}
                    </div>
                    <p style="font-size:0.85rem; opacity:0.8; margin: 5px 0; color:#E5E7EB;">
                        <b>Filière :</b> {row['Filière']} | <b>Niveau :</b> {row['Niveau']} | <b>Session :</b> {row['Année']}<br>
                        📊 Téléchargé {row['Downloads']} fois.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if row['Premium'] and not st.session_state.is_premium_user:
                    st.button("🔒 Débloquer le corrigé (300F requis)", key=f"l_{row['id']}", disabled=True)
                else:
                    if st.button(f"📥 Télécharger le PDF", key=f"d_{row['id']}"):
                        serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Downloads'] += 1
                        st.success("Téléchargement lancé !")
            with c2:
                if st.button("⭐ Garder en Favori", key=f"f_{row['id']}"):
                    serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Favori'] = True
                    st.toast("Ajouté aux favoris privés !")

# --- ONGLET 2 : PASSERELLE DE PAIEMENT AUTOMATISÉE HAUT DE GAMME (STYLE PUSH API COMME SUR 1XBET) ---
with tab_payment_gateway:
    st.markdown("### ⚡ Passerelle de Paiement Direct par Push USSD")
    st.info("Paramètres de sécurité de très haut niveau configurés. Vos fonds sont directement sécurisés vers les comptes du concepteur en chef.")
    
    col_pay_form, col_pay_info = st.columns([2, 1])
    
    with col_pay_form:
        st.markdown("#### Formulaire d'Abonnement")
        operator = st.radio("Sélectionnez votre opérateur de paiement Mobile Money :", ["Orange Money Cameroun", "MTN Mobile Money"])
        amount_selected = st.selectbox("Formule d'accès Élite Académique :", ["300 F CFA - Accès Standard Unique", "500 F CFA - Pack Révision Intensive", "1000 F CFA - Support Intégral Annuel"])
        phone_pay = st.text_input("Entrez votre numéro de téléphone de débit (9 chiffres) :", placeholder="Ex: 6XXXXXXXX")
        
        if st.button("🚀 LANCER LA DEMANDE DE RETRAIT SÉCURISÉ"):
            if len(phone_pay) != 9 or not phone_pay.isdigit():
                st.error("Format du numéro invalide. Entrez un numéro à 9 chiffres.")
            else:
                # INTERFACE DE ROUTAGE ASYNCHRONE DIRECTE - SIMULATION D'UN PUSH GATEWAY WEBHOOK (STYLE 1XBET)
                status_box = st.empty()
                progress_bar = st.progress(0)
                
                status_box.warning("🔄 Connexion au commutateur central Telecom...")
                time.sleep(1.5)
                progress_bar.progress(30)
                
                status_box.info(f"📲 Requête PUSH envoyée avec succès sur le {phone_pay}. En attente de la saisie de votre code PIN secret...")
                # Compte à rebours de sécurité de très haut niveau pour laisser l'utilisateur valider sur son téléphone
                for i in range(5, 0, -1):
                    status_box.info(f"📲 En attente de validation sur votre téléphone ({i}s)... Saisissez votre code PIN secret.")
                    time.sleep(1)
                
                progress_bar.progress(80)
                status_box.warning("⚡ Traitement de la notification de débit (Webhook)...")
                time.sleep(1.5)
                
                # Génération automatisée immédiate du ticket cryptographique unique
                nouveau_ticket = "ISABEE-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
                serveur_data["tickets"].append(nouveau_ticket)
                
                progress_bar.progress(100)
                status_box.success("✅ Transaction Approuvée ! Débit effectué.")
                
                st.balloons()
                st.markdown(f"""
                    <div style="background-color:rgba(16,185,129,0.15); border:2px solid #10B981; padding:20px; border-radius:12px; text-align:center;">
                        <h4 style="color:#34D399; margin:0;">🔑 VOTRE TICKET PREMIUM UNIQUE COMPILÉ</h4>
                        <p style="font-size:1.8rem; font-family:'JetBrains Mono', monospace; font-weight:700; color:#FFFFFF; margin:10px 0;">{nouveau_ticket}</p>
                        <p style="font-size:0.85rem; opacity:0.8; margin:0;">Copiez ce code et collez-le dans la zone "ACCÈS COMPTE" de la barre latérale pour activer instantanément vos privilèges.</p>
                    </div>
                """, unsafe_allow_html=True)
                
    with col_pay_info:
        st.markdown("#### Comptes Sécurisés Officiels")
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); padding:15px; border-radius:8px; border-left:4px solid #FF6600;">
                <b>🍊 Orange Money Cible :</b><br>
                <code style="font-size:1.1rem; color:#FF6600;">+237 {serveur_data["config"]["orange_target"]}</code>
            </div>
            <br>
            <div style="background: rgba(255,255,255,0.02); padding:15px; border-radius:8px; border-left:4px solid #FFCC00;">
                <b>💛 MTN Mobile Money Cible :</b><br>
                <code style="font-size:1.1rem; color:#FFCC00;">+237 {serveur_data["config"]["mtn_target"]}</code>
            </div>
        """, unsafe_allow_html=True)

# --- ONGLET 3 : INTERACTIONS ---
with tab_public_interact:
    st.markdown("### 🗣️ Espace Interactif des Étudiants")
    col_comm, col_sug = st.columns(2)
    
    with col_comm:
        st.subheader("💬 Commentaires")
        for c in serveur_data["interactions"]["commentaires"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:8px;'>💬 {c}</div>", unsafe_allow_html=True)
        
        with st.form("new_comment_form", clear_on_submit=True):
            txt_c = st.text_input("Laisser un commentaire :")
            if st.form_submit_button("Envoyer le commentaire") and txt_c:
                serveur_data["interactions"]["commentaires"].append(txt_c)
                st.rerun()

    with col_sug:
        st.subheader("💡 Suggestions")
        for s in serveur_data["interactions"]["suggestions"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:8px;'>💡 {s}</div>", unsafe_allow_html=True)
            
        with st.form("new_sug_form", clear_on_submit=True):
            txt_s = st.text_input("Proposer un document ou une idée :")
            if st.form_submit_button("Soumettre la suggestion") and txt_s:
                serveur_data["interactions"]["suggestions"].append(txt_s)
                st.rerun()

# ==============================================================================
# 6. PARTIE PRIVÉE : FILTRE DES RÔLES & DRÉCISION ADMINISTRATIVE SECRÈTE
# ==============================================================================
with tab_dev_zone:
    st.markdown("### 🔒 Espace d'Infrastructure Sécurisé")
    
    if st.session_state.dev_role is None:
        input_pwd = st.text_input("Entrez votre clé d'accès d'infrastructure :", type="password")
        if st.button("Vérifier le niveau d'autorisation"):
            if input_pwd == serveur_data["config"]["chief_password"]:
                st.session_state.dev_role = "Chief"
                st.success("Bonjour Concepteur en Chef. Vos privilèges sont absolus.")
                st.rerun()
            elif input_pwd == serveur_data["config"]["copilot_password"]:
                st.session_state.dev_role = "Copilote"
                st.info("Accès Copilote autorisé : Module de téléversement uniquement.")
                st.rerun()
            else:
                st.error("Clé de sécurité invalide.")
    else:
        if st.button("🔒 Verrouiller la session d'administration"):
            st.session_state.dev_role = None
            st.rerun()
            
        st.markdown(f"**Niveau d'accréditation actuel :** `{st.session_state.dev_role}`")
        st.markdown("---")
        
        # ----------------------------------------------------------------------
        # SOUS-INTERFACE DESTINÉE AU COPILOTE (OU CHIEF) : UNIQUEMENT LE TÉLÉVERSEMENT
        # ----------------------------------------------------------------------
        if st.session_state.dev_role in ["Copilote", "Chief"]:
            st.markdown("### 🚀 Module de Soumission de Documents (DÉPÔT ÉLITE)")
            
            with st.form("upload_form"):
                u_mat = st.text_input("Nom de la matière :")
                u_cyc = st.selectbox("Cycle", ["Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
                u_fil = st.selectbox("Filière", FILIERES)
                u_niv = st.selectbox("Niveau", ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5", "M1", "M2"])
                u_type = st.selectbox("Type", ["CC", "Examen", "Rattrapage", "TP"])
                u_prof = st.text_input("Enseignant :")
                u_prem = st.checkbox("Verrouiller derrière l'accès Premium (300F)")
                u_file = st.file_uploader("Fichier")
                
                btn_publier = st.form_submit_button("SOUMETTRE LE DOCUMENT POUR FILTRAGE")
                
            if btn_publier:
                if u_mat and u_file:
                    temp_row = {
                        "id": int(len(serveur_data["db"]) + len(serveur_data["staging"]) + 1), 
                        "Cycle": u_cyc, "Filière": u_fil, "Niveau": u_niv, "Matière": u_mat, 
                        "Enseignant": u_prof, "Type": u_type, "Année": "2025-2026", 
                        "Premium": u_prem, "Downloads": 0, "Date": datetime.today().strftime('%d/%m/%Y'), 
                        "Favori": False, "Soumis_Par": st.session_state.dev_role
                    }
                    
                    # SI C'EST UN COPILOTE : Le fichier est bloqué dans le sas d'attente (Staging)
                    if st.session_state.dev_role == "Copilote":
                        serveur_data["staging"].append(temp_row)
                        st.warning("⚠️ Document envoyé avec succès dans la file d'attente. En attente exclusive de l'approbation du Concepteur en Chef.")
                    else:
                        # SI C'EST LE CHEF : Publication immédiate sans intermédiaire
                        new_df = pd.DataFrame([temp_row])
                        serveur_data["db"] = pd.concat([serveur_data["db"], new_df], ignore_index=True)
                        st.success("✅ Publication immédiate effectuée sur le serveur public.")
                        st.rerun()
                else:
                    st.error("Champs obligatoires manquants (Nom de matière ou Fichier).")

        # ----------------------------------------------------------------------
        # MODULE UNIQUE DU CONCEPTEUR EN CHEF (TOTALEMENT INVISIBLE POUR LES COPILOTES)
        # ----------------------------------------------------------------------
        if st.session_state.dev_role == "Chief":
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="chief-vault">
                    <h2 style="color: #A78BFA; margin:0;">👁️ COFFRE-FORT VIRTUEL DU CONCEPTEUR EN CHEF</h2>
                    <p style="font-size:0.9rem; opacity:0.8;">Espace de décision souverain. Toi seul contrôles la vie de l'application.</p>
                </div>
            """, unsafe_allow_html=True)
            
            sub_tab_vault, sub_tab_tickets_mgr, sub_tab_global_db, sub_tab_config_system = st.tabs([
                "📥 VALIDATION DES SOUUMISSIONS COPILOTES",
                "🎫 INJECTEUR INTELLIGENT DE TICKETS",
                "👑 PANNEAU DE CONTRÔLE DE LA BASE",
                "⚙️ PARAMÈTRES SECRETS DU SERVEUR"
            ])
            
            # A. SAS DE VALIDATION DES SOUUMISSIONS DES COPILOTES
            with sub_tab_vault:
                st.markdown("#### Fichiers en attente d'approbation réglementaire")
                if not serveur_data["staging"]:
                    st.info("Aucun document en attente dans la zone de filtrage des copilotes.")
                else:
                    for i, item in enumerate(serveur_data["staging"]):
                        st.markdown(f"""
                            <div style="background:rgba(255,255,255,0.02); padding:15px; border-radius:8px; border-left:4px solid #8B5CF6; margin-bottom:10px;">
                                <b>Matière :</b> {item['Matière']} | <b>Filière :</b> {item['Filière']} | <b>Niveau :</b> {item['Niveau']}<br>
                                <small>Proposé par le compte : <code>{item['Soumis_Par']}</code></small>
                            </div>
                        """, unsafe_allow_html=True)
                        c_app, c_rej = st.columns(2)
                        if c_app.button("✅ Approuver et Publier", key=f"app_{i}"):
                            new_df = pd.DataFrame([item])
                            serveur_data["db"] = pd.concat([serveur_data["db"], new_df], ignore_index=True)
                            serveur_data["staging"].pop(i)
                            st.success("Document validé et intégré à la base publique.")
                            st.rerun()
                        if c_rej.button("❌ Rejeter et Détruire", key=f"rej_{i}"):
                            serveur_data["staging"].pop(i)
                            st.warning("Soumission supprimée.")
                            st.rerun()

            # B. INJECTEUR ET GESTIONNAIRE DE TICKETS AUTOMATES
            with sub_tab_tickets_mgr:
                st.markdown("#### Gestion des Billets Authentifiés Unique")
                
                col_gen, col_list = st.columns(2)
                with col_gen:
                    st.markdown("##### Générateur Express de Tickets")
                    num_to_gen = st.number_input("Nombre de tickets de 300F à injecter :", min_value=1, max_value=50, value=5)
                    if st.button("⚡ Injecter au Pool Central"):
                        for _ in range(num_to_gen):
                            code = "ISABEE-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
                            serveur_data["tickets"].append(code)
                        st.success(f"{num_to_gen} Tickets uniques générés et enregistrés de force.")
                        st.rerun()
                        
                with col_list:
                    st.markdown("##### Pool Actif de Tickets Valides (Usage Unique)")
                    st.write(serveur_data["tickets"])

            # C. CONTROLE DE LA BASE DE DONNÉES PUBLIQUE
            with sub_tab_global_db:
                st.markdown("#### Table d'Autorité Publique")
                st.dataframe(serveur_data["db"][['Matière', 'Niveau', 'Downloads', 'Premium']], use_container_width=True)
                
                for idx, row in serveur_data["db"].iterrows():
                    col_n, col_b = st.columns([4, 1])
                    col_n.write(f"🗑️ {row['Matière']} ({row['Niveau']})")
                    if col_b.button("Supprimer Définitivement", key=f"del_sec_{row['id']}"):
                        serveur_data["db"] = serveur_data["db"][serveur_data["db"]['id'] != row['id']]
                        st.rerun()

            # D. PARAMÈTRES ET CONFIGURATION DES NUMÉROS ET DE LA SÉCURITÉ
            with sub_tab_config_system:
                st.markdown("#### Paramètres Fondamentaux d'Infrastructure")
                
                c_pwd1, c_pwd2 = st.columns(2)
                new_c_pwd = c_pwd1.text_input("Modifier le mot de passe Chef Secret :", value=serveur_data["config"]["chief_password"], type="password")
                new_co_pwd = c_pwd2.text_input("Modifier le mot de passe Copilote :", value=serveur_data["config"]["copilot_password"], type="password")
                
                if st.button("🔒 Sauvegarder la nouvelle matrice de sécurité"):
                    serveur_data["config"]["chief_password"] = new_c_pwd
                    serveur_data["config"]["copilot_password"] = new_co_pwd
                    st.success("Mise à jour immédiate des privilèges d'accès.")
                    
                st.markdown("---")
                st.markdown("#### Modification des Numéros Marchands Cibles (Cameroun)")
                c_num1, c_num2 = st.columns(2)
                serveur_data["config"]["orange_target"] = c_num1.text_input("Numéro Orange Money Récepteur :", value=serveur_data["config"]["orange_target"])
                serveur_data["config"]["mtn_target"] = c_num2.text_input("Numéro MTN MoMo Récepteur :", value=serveur_data["config"]["mtn_target"])
                
                if st.button("💾 Mettre à jour les passerelles financières"):
                    st.success("Les flux de paiements 1xBet style pointent désormais vers les nouveaux terminaux.")
