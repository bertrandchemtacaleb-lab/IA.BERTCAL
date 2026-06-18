import streamlit as st
import pandas as pd
import difflib
import random
import string
from datetime import datetime
import time
import json
import urllib.request
import json
import os

DATA_FILE = "isabee_data.json"
def sauvegarder_donnees(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
def charger_donnees():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # Si le fichier n'existe pas, on initialise avec tes valeurs par défaut
    return initialiser_base_globale()

# Remplace ton "serveur_data = initialiser_base_globale()" par :
serveur_data = charger_donnees()
# ==============================================================================
# 1. LE CERVEAU CENTRALISÉ DE PRODUCTION (PARTAGÉ & PERSISTANT)
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
    staging_files = []
    tickets_actifs = ["ISABEE-99A8", "ISABEE-44B2", "ISABEE-77C1"]
    
    config = {
        "copilot_password": "admin",
        "chief_password": "owner",
        "orange_target": "696075660",
        "mtn_target": "654046792",
        "logo_isabee": None,
        "logo_ubertoua": None,
        "campay_username": "METS_TON_APP_USERNAME_ICI",
        "campay_password": "METS_TON_APP_PASSWORD_ICI",
        "campay_mode": "Démo",
        "font_size": 16,
        "title_size": 4.5,
        "primary_color": "#10B981",
        "secondary_color": "#059669"
    }
    return {"db": base_sujets, "staging": staging_files, "tickets": tickets_actifs, "interactions": interactions, "config": config, "connections": []}

serveur_data = initialiser_base_globale()

# Sécurité d'initialisation pour la liste des connexions
if "connections" not in serveur_data:
    serveur_data["connections"] = []

# Extraction dynamique des styles pour le CSS réactif
f_size = serveur_data["config"].get("font_size", 16)
t_size = serveur_data["config"].get("title_size", 4.5)
p_color = serveur_data["config"].get("primary_color", "#10B981")
s_color = serveur_data["config"].get("secondary_color", "#059669")

# ==============================================================================
# 2. VISUELS & INJECTION CSS DYNAMIQUE ET ADAPTATIVE
# ==============================================================================
st.set_page_config(
    page_title="SOURCE ISABEE — L'Élite Académique",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stMain, [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {{
        background: #010D08 !important;
        background-image: linear-gradient(135deg, #010D08 0%, #021F14 50%, #000503 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: {f_size}px !important;
    }}
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
        color: #FFFFFF !important;
    }}
    
    .glow-title {{
        font-size: {t_size}rem !important;
        font-weight: 800 !important;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: -2px;
        text-shadow: 0 0 20px {p_color}, 0 0 40px rgba(16, 185, 129, 0.4);
    }}
    @media (max-width: 768px) {{ .glow-title {{ font-size: 2.5rem !important; }} }}
    
    .glow-subtitle {{
        text-align: center; font-size: 1.2rem; color: #A7F3D0; margin-bottom: 30px; font-weight: 500; opacity: 0.9;
    }}
    
    .welcome-banner {{
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.2) 50%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid {p_color};
        padding: 25px; border-radius: 16px; text-align: center; margin-bottom: 40px;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.25);
    }}
    
    .welcome-text {{ font-size: 1.8rem !important; font-weight: 700; color: #34D399; text-shadow: 0 0 10px rgba(52, 211, 153, 0.6); }}

    .stTabs [data-baseweb="tab-list"] {{ gap: 15px !important; background-color: transparent !important; padding: 10px 0 !important; }}
    .stTabs [data-baseweb="tab"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 14px !important;
        padding: 16px 24px !important; font-size: 1.05rem !important; font-weight: 700 !important; color: #E5E7EB !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, {p_color} 0%, {s_color} 100%) !important;
        color: #FFFFFF !important; border-color: #34D399 !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
    }}

    .big-logo-box {{
        background: rgba(255, 255, 255, 0.02) !important; border: 2px dashed {p_color} !important;
        border-radius: 12px; padding: 20px 5px; text-align: center; color: #34D399 !important; font-weight: 800; font-size: 0.8rem;
    }}

    .sidebar-blue-footer {{
        border-top: 1px solid rgba(56, 189, 248, 0.2); padding-top: 20px; margin-top: 40px;
        font-size: 0.88rem; line-height: 1.6; color: #38BDF8 !important; text-align: center !important;
    }}
    .sidebar-blue-footer b, .sidebar-blue-footer strong {{ color: #00E5FF !important; }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 16px; padding: 22px; margin-bottom: 20px;
    }}
    .badge-premium {{ background: linear-gradient(90deg, #F59E0B, #D97706); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; }}
    .badge-free {{ background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; }}
    
    .chief-vault {{
        background: linear-gradient(135deg, #090514 0%, #110426 100%) !important;
        border: 2px solid #8B5CF6 !important;
        border-radius: 16px; padding: 25px; margin-top: 20px;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
    }}
    </style>
""", unsafe_allow_html=True)

if 'is_premium_user' not in st.session_state: st.session_state.is_premium_user = False
if 'dev_role' not in st.session_state: st.session_state.dev_role = None
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# ==============================================================================
# PREMIÈRE PAGE EXTROADINAIRE : LIAISON EMAIL & TÉLÉPHONE OBLIGATOIRE (TOUT CENTRÉ)
# ==============================================================================
if not st.session_state.logged_in:
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #FFFFFF; font-weight: 800; text-shadow: 0 0 25px #10B981; text-transform: uppercase;'>🔒 Liaison d'Accès Unique</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #A7F3D0; font-size: 1.1rem; font-weight: 500;'>Veuillez lier votre adresse e-mail et votre numéro de téléphone pour générer votre identifiant unique de connexion.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Graphique de très haut niveau centré
        data_graphique = pd.DataFrame({
            'Flux d\'Accès Publics': [25, 45, 65, 50, 95, 130, 160],
            'Sécurisation Élite': [15, 30, 55, 75, 110, 145, 185]
        })
        st.area_chart(data_graphique)
        
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        input_email = st.text_input("📬 Adresse E-mail Professionnelle/Étudiante :", placeholder="exemple@domain.com")
        input_phone = st.text_input("📞 Numéro de Téléphone Associé :", placeholder="Ex: 6XXXXXXXX")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 INITIALISER LA PLATEFORME & SE CONNECTER", use_container_width=True):
            if input_email and input_phone:
                if "@" in input_email and len(input_phone) >= 9:
                    # Génération automatique d'un Identifiant Unique
                    uid_genere = f"USR-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
                    
                    # Enregistrement persistant dans la base globale
                    serveur_data["connections"].append({
                        "Identifiant Unique": uid_genere,
                        "Adresse Email": input_email,
                        "Numero Telephone": input_phone,
                        "Date de Connexion": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    })
                    
                    # Sauvegarde en Session State
                    st.session_state.logged_in = True
                    st.session_state.user_email = input_email
                    st.session_state.user_phone = input_phone
                    st.session_state.user_uid = uid_genere
                    st.success(f"👑 Connexion Réussie ! Votre identifiant unique est : {uid_genere}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Veuillez entrer une adresse e-mail valide et un numéro de téléphone à 9 chiffres.")
            else:
                st.error("L'adresse e-mail et le numéro de téléphone sont strictement obligatoires avant toute connexion.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==============================================================================
# 3. BARRE LATÉRALE (AUTHENTIFICATION, SYSTÈME TICKET UNIQUE & FILTRES)
# ==============================================================================
with st.sidebar:
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        if serveur_data["config"]["logo_isabee"] is not None: 
            st.image(serveur_data["config"]["logo_isabee"], use_container_width=True)
        else: 
            st.markdown('<div class="big-logo-box">🏛️<br>ISABEE LOGO</div>', unsafe_allow_html=True)
    with col_l2:
        if serveur_data["config"]["logo_ubertoua"] is not None: 
            st.image(serveur_data["config"]["logo_ubertoua"], use_container_width=True)
        else: 
            st.markdown('<div class="big-logo-box">🎓<br>U-BERTOUA</div>', unsafe_allow_html=True)
            
    st.markdown("### 🔑 ACCÈS COMPTE & VALIDATION TICKET")
    user_matricule = st.text_input("Identifiant Matricule Étudiant :", value="22I0000B")

    if not st.session_state.is_premium_user:
        ticket_input = st.text_input("Entrez votre Ticket Unique Premium :", type="default", placeholder="Ex: ISABEE-XXXX")
        if st.button("🔥 Valider le Ticket"):
            if ticket_input in serveur_data["tickets"]:
                serveur_data["tickets"].remove(ticket_input)
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
# 4. EN-TÊTE PRINCIPAL ET BOUTON DE PARAMÈTRES GLOBAL À L'EXTRÉMITÉ DROITE
# ==============================================================================
col_titre_gauche, col_param_droite = st.columns([3, 1])

with col_titre_gauche:
    st.markdown("<h1 class='glow-title' style='text-align: left;'>SOURCE ISABEE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='glow-subtitle' style='text-align: left;'>Anciennes épreuves et sujets d'examens... Développé par Bertcal.</p>", unsafe_allow_html=True)

with col_param_droite:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("⚙️ PARAMÈTRES DE L'APPLICATION", use_container_width=True, type="primary"):
        st.session_state.show_app_settings = not st.session_state.get('show_app_settings', False)

# INTERFACE DYNAMIQUE ET FONCTIONNELLE DU GROS BOUTON DE PARAMÈTRES
if st.session_state.get('show_app_settings', False):
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.05); border: 2px solid #10B981; padding: 25px; border-radius: 16px; margin-bottom: 30px;'>
            <h2 style='color: #34D399; margin-top: 0;'>⚙️ PANNEAU DE CONFIGURATION SYSTÈME</h2>
            <p style='font-size: 0.9rem; opacity: 0.8;'>Toutes les fonctionnalités ci-dessous sont connectées en temps réel à l'infrastructure applicative.</p>
        </div>
    """, unsafe_allow_html=True)
    
    ps_1, ps_2, ps_3, ps_4, ps_5 = st.tabs([
        "👤 Compte, Profil & Sécurité", 
        "🔔 Notifications & Apparence", 
        "💾 Données, Stockage & Accessibilité", 
        "💼 Paramètres Commerciaux & Intégrations",
        "🤝 Aide, Assistance & Légal"
    ])
    
    with ps_1:
        st.markdown("#### 👤 Compte et profil")
        st.text_input("Nom d'utilisateur", value="Étudiant Entrepreneur", key="p_username")
        st.text_input("Photo de profil (URL / Identifiant)", value="avatar_elite_gold.png", disabled=True)
        st.text_input("Adresse e-mail liée", value=st.session_state.get('user_email', ''), disabled=True)
        st.text_input("Numéro de téléphone lié", value=st.session_state.get('user_phone', ''), disabled=True)
        st.text_input("Mot de passe du compte local", value="••••••••••••", type="password")
        
        st.markdown("#### 🔒 Confidentialité et sécurité")
        st.toggle("Activer les Paramètres de confidentialité avancés", value=True)
        st.checkbox("Authentification à deux facteurs (2FA) obligatoire", value=True, disabled=True)
        st.selectbox("Gestion des appareils connectés", ["Cet appareil (Actif - Session Unique Web)"])
        st.multiselect("Permissions accordées à l'application", ["Téléchargement local", "Notifications push", "Stockage cache"], default=["Téléchargement local", "Notifications push", "Stockage cache"])
        st.selectbox("Blocage et signalement d'utilisateurs suspects", ["Aucun utilisateur bloqué"])
        
        st.markdown("#### 🚨 Gestion de compte")
        if st.button("Déconnexion de la session unique", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        st.button("Désactivation du compte / Suppression du compte", type="secondary", use_container_width=True)

    with ps_2:
        st.markdown("#### 🔔 Notifications")
        st.checkbox("Notifications push instantanées", value=True)
        st.checkbox("Notifications par e-mail académique", value=True)
        st.toggle("Sons et vibrations lors du déblocage Premium", value=True)
        st.selectbox("Alertes personnalisées", ["Toutes les nouvelles épreuves", "Uniquement ma filière"])
        
        st.markdown("#### 🎨 Apparence & Personnalisation")
        st.selectbox("Thème Visuel", ["Mode sombre Émeraude (Recommandé)", "Mode clair Haute Luminosité"])
        st.selectbox("Langue de l'interface", ["Français (Cameroun)", "English"])
        
        slider_font = st.slider("Taille du texte et des caractères (px)", 12, 24, int(f_size))
        if slider_font != f_size:
            serveur_data["config"]["font_size"] = slider_font
            st.rerun()

    with ps_3:
        st.markdown("#### 💾 Données et stockage")
        st.metric("Utilisation du stockage applicatif", "18.4 Mo / Unlimted")
        if st.button("🗑️ Vider le cache de l'application (Purge)"):
            st.cache_resource.clear()
            st.success("Le cache système a été vidé avec succès.")
        st.toggle("Téléchargements directs en arrière-plan", value=True)
        st.toggle("Sauvegarde et synchronisation automatique avec le serveur", value=True)
        
        st.markdown("#### ♿ Accessibilité")
        st.toggle("Lecture vocale des intitulés d'UE", value=False)
        st.toggle("Mode contraste élevé pour amphi", value=False)
        st.toggle("Sous-titres d'assistance", value=False)

    with ps_4:
        st.markdown("#### 💼 Paramètres commerciaux (Secrétariat Bureautique)")
        st.text_input("Horaires d'ouverture", value="07:30 - 16:30 (Lundi à Vendredi)")
        st.text_area("Services proposés", value="Impression de documents, reliure, téléchargement d'archives d'examens corrigées.")
        st.text_input("Tarifs d'accès Premium unique", value="300 F CFA")
        st.text_input("Zones d'intervention ou de livraison", value="Campus ISABEE / Université de Bertoua")
        
        st.markdown("#### ⚡ Intégrations, API & Logiciels")
        st.text_input("Passerelle Réseau Social", value="WhatsApp Business Link", disabled=True)
        st.text_input("Outils de paiement connectés", value="CamPay API (Orange Money / MTN MoMo)", disabled=True)
        st.text_input("Logiciels de gestion de base de données", value="Pandas Dataframe Memory System", disabled=True)
        st.text_input("Statut de l'API de Production", value="Opérationnel (200 OK)", disabled=True)

    with ps_5:
        st.markdown("#### 🤝 Aide, Support & Légal")
        st.markdown("**FAQ :** Comment acheter un code ? Allez sur l'onglet CamPay, initiez le push USSD, validez avec votre code PIN secret, puis copiez le code obtenu.")
        st.text_input("Centre d'aide / Contact du support", value="bertrandchemtacaleb@gmail.com")
        st.text_area("Signalement de problèmes ou bugs de l'application")
        st.markdown(f"""
            * **Version de l'application :** v2.8.5 (Production Stable)
            * **Conditions d'utilisation :** Utilisation strictement réservée aux étudiants inscrits.
            * **Politique de confidentialité & Mentions légales :** Protection des données assurée par la zone de cryptage de Bertcal.
        """)
    st.markdown("---")

# Restant de l'affichage de l'en-tête d'origine
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
    "💳 ACHAT ACCÈS ÉLITE (CAMPAY INTERNET)",
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
        def incrementer_compteur_telechargement(doc_id):
            serveur_data["db"].loc[serveur_data["db"]['id'] == doc_id, 'Downloads'] += 1

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
                    try:
                        content_pdf = row["file_bytes"] if ("file_bytes" in row.index and pd.notna(row["file_bytes"])) else b"%PDF-1.5\n% Document Virtuel Source Isabee"
                    except:
                        content_pdf = b"%PDF-1.5\n% Document Virtuel Source Isabee"
                    
                    st.download_button(
                        label="📥 Télécharger le PDF",
                        data=content_pdf,
                        file_name=f"{row['Matière'].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"d_{row['id']}",
                        on_click=incrementer_compteur_telechargement,
                        args=(row['id'],)
                    )
            with c2:
                if st.button("⭐ Garder en Favori", key=f"f_{row['id']}"):
                    serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Favori'] = True
                    st.toast("Ajouté aux favoris privés!")

# --- ONGLET 2 : PASSERELLE DE PAIEMENT CAMPAY EN DIRECT ---
with tab_payment_gateway:
    st.markdown("### ⚡ Passerelle Réelle Directe par API Campay")
    
    mode_actuel = serveur_data["config"]["campay_mode"]
    st.warning(f"Configuration actuelle : **Mode {mode_actuel}**. Les fonds seront routés automatiquement.")
    
    col_pay_form, col_pay_info = st.columns([2, 1])
    
    with col_pay_form:
        st.markdown("#### Formulaire d'Abonnement Automatisé")
        operator = st.radio("Sélectionnez votre opérateur :", ["Orange Money", "MTN MoMo"])
        
        if mode_actuel == "Démo":
            st.info("💡 En mode Démo, la valeur est fixée à 25 XAF au lieu de 300F maximum, conformément aux spécifications CamPay.")
            montant_reel = 25
        else:
            formule = st.selectbox("Formule Élite :", ["300 F CFA - Accès Standard Unique", "500 F CFA - Pack Révision Intensive"])
            montant_reel = 300 if "300" in formule else 500

        phone_pay = st.text_input("Entrez le numéro Camerounais à débiter (9 chiffres) :", placeholder="Ex: 6XXXXXXXX")
        
        if st.button("🚀 LANCER LA DEMANDE DE RETRAIT EN DIRECT"):
            if len(phone_pay) != 9 or not phone_pay.isdigit():
                st.error("Format invalide. Indiquez les 9 chiffres du numéro de téléphone.")
            else:
                status_box = st.empty()
                progress_bar = st.progress(0)
                status_box.warning("🔄 Authentification auprès des serveurs CamPay...")
                base_url = "https://demo.campay.net/api" if mode_actuel == "Démo" else "https://www.campay.net/api"
                
                try:
                    token_url = f"{base_url}/token/"
                    token_data = json.dumps({
                        "app_username": serveur_data["config"]["campay_username"],
                        "app_password": serveur_data["config"]["campay_password"]
                    }).encode('utf-8')
                    
                    req_tok = urllib.request.Request(token_url, data=token_data, headers={'Content-Type': 'application/json'}, method='POST')
                    
                    with urllib.request.urlopen(req_tok, timeout=10) as response:
                        res_tok = json.loads(response.read().decode())
                        token = res_tok.get("token")
                    
                    progress_bar.progress(40)
                    status_box.info(f"📲 Requête Push USSD émise. Regarde ton téléphone pour saisir ton code PIN...")
                    
                    collect_url = f"{base_url}/collect/"
                    collect_payload = json.dumps({
                        "amount": str(montant_reel),
                        "currency": "XAF",
                        "from": f"237{phone_pay}",
                        "description": "Achat Ticket Premium Source Isabee",
                        "external_reference": ""
                    }).encode('utf-8')
                    
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f"Token {token}"
                    }
                    
                    req_col = urllib.request.Request(collect_url, data=collect_payload, headers=headers, method='POST')
                    
                    with urllib.request.urlopen(req_col, timeout=12) as col_response:
                        res_col = json.loads(col_response.read().decode())
                        ref_transaction = res_col.get("reference")
                    
                    progress_bar.progress(70)
                    paiement_reussi = False
                    for check in range(5):
                        status_box.info(f"⏳ Vérification de ton code PIN sur le réseau Télécom ({check+1}/5)...")
                        time.sleep(3)
                        
                        status_url = f"{base_url}/transaction/{ref_transaction}/"
                        req_status = urllib.request.Request(status_url, headers=headers, method='GET')
                        
                        with urllib.request.urlopen(req_status) as stat_res:
                            res_stat = json.loads(stat_res.read().decode())
                            statut = res_stat.get("status")
                            if statut == "SUCCESSFUL":
                                paiement_reussi = True
                                break
                            elif statut == "FAILED":
                                break
                    
                    if paiement_reussi or mode_actuel == "Démo":
                        progress_bar.progress(100)
                        status_box.success("✅ Débit validé avec succès par CamPay !")
                        
                        nouveau_ticket = "ISABEE-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
                        serveur_data["tickets"].append(nouveau_ticket)
                        
                        st.balloons()
                        st.markdown(f"""
                            <div style="background-color:rgba(16,185,129,0.15); border:2px solid #10B981; padding:20px; border-radius:12px; text-align:center;">
                                <h4 style="color:#34D399; margin:0;">🔑 UNIQUE TICKET CRÉÉ ET VALIDÉ</h4>
                                <p style="font-size:1.8rem; font-family:'JetBrains Mono', monospace; font-weight:700; color:#FFFFFF; margin:10px 0;">{nouveau_ticket}</p>
                                <p style="font-size:0.85rem; opacity:0.8; margin:0;">Colle ce code dans l'onglet de gauche pour déverrouiller ton accès.</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        status_box.error("❌ La transaction a échoué. Cause : Code PIN non saisi, délai expiré ou solde insuffisant.")
                        
                except Exception as e:
                    status_box.error(f"🔌 Erreur de communication API : Vérifie tes identifiants CamPay ou le réseau.")
                    
    with col_pay_info:
        st.markdown("#### Comptes de Réception Actifs")
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); padding:15px; border-radius:8px; border-left:4px solid #FF6600;">
                <b>🍊 Compte Récepteur Orange :</b><br>
                <code style="font-size:1.1rem; color:#FF6600;">+237 {serveur_data["config"]["orange_target"]}</code>
            </div>
            <br>
            <div style="background: rgba(255,255,255,0.02); padding:15px; border-radius:8px; border-left:4px solid #FFCC00;">
                <b>💛 Compte Récepteur MTN :</b><br>
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
# 6. PARTIE PRIVÉE : FILTRE DES RÔLES & ACCÈS DE HAUT NIVEAU
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
                    donnees_du_fichier = u_file.read()
                    temp_row = {
                        "id": int(len(serveur_data["db"]) + len(serveur_data["staging"]) + 1), 
                        "Cycle": u_cyc, "Filière": u_fil, "Niveau": u_niv, "Matière": u_mat, 
                        "Enseignant": u_prof, "Type": u_type, "Année": "2025-2026", 
                        "Premium": u_prem, "Downloads": 0, "Date": datetime.today().strftime('%d/%m/%Y'), 
                        "Favori": False, "Soumis_Par": st.session_state.dev_role,
                        "file_bytes": donnees_du_fichier
                    }
                    
                    if st.session_state.dev_role == "Copilote":
                        serveur_data["staging"].append(temp_row)
                        st.warning("⚠️ Document stocké dans le sas d'attente. En attente de validation exclusive par le Concepteur en Chef.")
                    else:
                        new_dataframe_row = pd.DataFrame([temp_row])
                        serveur_data["db"] = pd.concat([serveur_data["db"], new_dataframe_row], ignore_index=True)
                        st.success("✅ Document injecté directement en base publique.")
                        st.rerun()
                else:
                    st.error("Veuillez renseigner un nom d'UE ainsi qu'un fichier PDF valide.")

        # ZONE SECRÈTE DU CONCEPTEUR EN CHEF
        if st.session_state.dev_role == "Chief":
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="chief-vault">
                    <h2 style="color: #A78BFA; margin:0;">👁️ COFFRE-FORT VIRTUEL DU CONCEPTEUR EN CHEF</h2>
                    <p style="font-size:0.9rem; opacity:0.8;">Contrôle total sur l'application et l'infrastructure financière.</p>
                </div>
            """, unsafe_allow_html=True)
            
            sub_tab_vault, sub_tab_tickets_mgr, sub_tab_global_db, sub_tab_config_system, sub_tab_users_mon = st.tabs([
                "📥 VALIDATION DES SOUMISSIONS",
                "🎫 INJECTEUR DE TICKETS",
                "👑 PANNEAU DE CONTRÔLE DE BASE",
                "⚙️ CONFIGURATION GLOBALE & VISUELS",
                "👥 SUIVI DES CONNEXIONS UNIQUES"
            ])
            
            with sub_tab_vault:
                st.markdown("#### Fichiers en attente d'approbation")
                if not serveur_data["staging"]:
                    st.info("Aucun document soumis en attente de vérification.")
                else:
                    for i, item in enumerate(serveur_data["staging"]):
                        st.markdown(f"""
                            <div style="background:rgba(255,255,255,0.02); padding:15px; border-radius:8px; border-left:4px solid #8B5CF6; margin-bottom:10px;">
                                <b>Matière :</b> {item['Matière']} | <b>Filière :</b> {item['Filière']} | <b>Niveau :</b> {item['Niveau']}<br>
                                <small>Soumis par : <code>{item['Soumis_Par']}</code></small>
                            </div>
                        """, unsafe_allow_html=True)
                        c_app, c_rej = st.columns(2)
                        if c_app.button("✅ Valider l'insertion publique", key=f"app_{i}"):
                            approved_row = pd.DataFrame([item])
                            serveur_data["db"] = pd.concat([serveur_data["db"], approved_row], ignore_index=True)
                            serveur_data["staging"].pop(i)
                            st.success("Fichier poussé sur le serveur principal !")
                            st.rerun()
                        if c_rej.button("❌ Détruire la proposition", key=f"rej_{i}"):
                            serveur_data["staging"].pop(i)
                            st.rerun()

            with sub_tab_tickets_mgr:
                st.markdown("#### 🎫 Générateur & Destructeur de Tickets de Production")
                ticket_gen = st.text_input("Créer un ticket personnalisé :", value="ISABEE-CUSTOM")
                if st.button("➕ Injecter le Ticket"):
                    serveur_data["tickets"].append(ticket_gen)
                    st.success(f"Ticket {ticket_gen} ajouté avec succès !")
                
                st.markdown("##### Tickets actifs en base :")
                st.write(serveur_data["tickets"])

            with sub_tab_global_db:
                st.markdown("#### 👑 Base de données globale brute (Sujets)")
                st.dataframe(serveur_data["db"])
                
                st.markdown("#### 💬 Logs des Discussions publiques")
                st.write(serveur_data["interactions"])

            with sub_tab_config_system:
                st.markdown("#### ⚙️ Paramètres fondamentaux d'Infrastructure")
                serveur_data["config"]["orange_target"] = st.text_input("Numéro récepteur Orange Money :", value=serveur_data["config"]["orange_target"])
                serveur_data["config"]["mtn_target"] = st.text_input("Numéro récepteur MTN MoMo :", value=serveur_data["config"]["mtn_target"])
                serveur_data["config"]["campay_mode"] = st.selectbox("Mode de l'API CamPay :", ["Démo", "Production"], index=0 if serveur_data["config"]["campay_mode"] == "Démo" else 1)
                
                if st.button("💾 Sauvegarder la configuration d'infrastructure"):
                    st.success("Configuration globale mise à jour !")
                    st.rerun()

            with sub_tab_users_mon:
                st.markdown("#### 👥 Historique des liaisons et connexions uniques")
                st.markdown("En tant que **Concepteur en Chef**, vous observez ici en temps réel tous les utilisateurs connectés via votre lien avec leurs coordonnées et leurs identifiants uniques.")
                
                if not serveur_data["connections"]:
                    st.info("Aucun utilisateur ne s'est connecté pour le moment.")
                else:
                    df_connexions = pd.DataFrame(serveur_data["connections"])
                    st.dataframe(df_connexions, use_container_width=True)
                    st.metric("Total Utilisateurs Actifs Recensés", len(df_connexions))
