import streamlit as st
import pandas as pd
import difflib
import random
import string
from datetime import datetime
import time
import json
import urllib.request

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
        "title_size": 7.0,  # Augmenté à 7.0 pour être bien visible dès l'entrée
        "primary_color": "#10B981",
        "secondary_color": "#059669",
        "language": "Français"
    }
    return {"db": base_sujets, "staging": staging_files, "tickets": tickets_actifs, "interactions": interactions, "config": config}

serveur_data = initialiser_base_globale()

# Gestion de la langue sélectionnée dans la configuration globale
current_lang = serveur_data["config"].get("language", "Français")

def translate(text_fr, text_en):
    return text_fr if current_lang == "Français" else text_en

# Extraction dynamique des styles pour le CSS réactif
f_size = serveur_data["config"].get("font_size", 16)
t_size = serveur_data["config"].get("title_size", 7.0)
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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;600;700;800&family=JetBrains+Mono:wght=400;700&display=swap');
    
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
        text-shadow: 0 0 25px {p_color}, 0 0 50px rgba(16, 185, 129, 0.5);
    }}
    @media (max-width: 768px) {{ .glow-title {{ font-size: 3.5rem !important; }} }}
    
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
            
    st.markdown(f"### 🔑 {translate('ACCÈS COMPTE & VALIDATION TICKET', 'ACCOUNT ACCESS & TICKET VALIDATION')}")
    user_matricule = st.text_input(translate("Identifiant Matricule Étudiant :", "Student Matricule ID:"), value="22I0000B")

    if not st.session_state.is_premium_user:
        ticket_input = st.text_input(translate("Entrez votre Ticket Unique Premium :", "Enter Your Unique Premium Ticket:"), type="default", placeholder="Ex: ISABEE-XXXX")
        if st.button(translate("🔥 Valider le Ticket", "🔥 Validate Ticket")):
            if ticket_input in serveur_data["tickets"]:
                serveur_data["tickets"].remove(ticket_input)
                st.session_state.is_premium_user = True
                st.success(translate("👑 Accès Élite Activé ! Le ticket a été détruit de la base.", "👑 Elite Access Activated! Ticket consumed."))
                st.rerun()
            else:
                st.error(translate("Ticket invalide, expiré ou déjà consommé.", "Invalid, expired or already consumed ticket."))
    else:
        st.success(translate("👑 Statut : Compte Élite Académique", "👑 Status: Academic Elite Account"))
        if st.button(translate("Quitter le mode Premium", "Leave Premium Mode")):
            st.session_state.is_premium_user = False
            st.rerun()

    st.markdown("---")
    st.markdown(f"### 🎛️ {translate('FILTRES DE RECHERCHE', 'SEARCH FILTERS')}")
    f_cycle = st.selectbox(translate("Cycle d'études", "Study Cycle"), [translate("Tous", "All"), "Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
    f_filiere = st.selectbox(translate("Filière", "Department"), [translate("Toutes", "All Departments")] + FILIERES)
    f_type = st.selectbox(translate("Type d'évaluation", "Evaluation Type"), [translate("Tous", "All"), "CC", "Examen", "Rattrapage", "TP"])

    st.markdown(f"""
        <div class="sidebar-blue-footer">
            {translate('Développé par:', 'Developed by:')} <b>Chemta Caleb Bertrand</b><br>
            {translate('étudiant ingénieur en génie énergétique.', 'engineering student in energy engineering.')}<br>
            <br>
            <strong>CONTACT COMMERCIAL :</strong><br>
            • {translate('Téléphone', 'Phone')} : +237 {serveur_data["config"]["orange_target"]}<br>
            • Email : bertrandchemtacaleb@gmail.com<br>
            • Campus : ISABEE / U-BERTOUA
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. EN-TÊTE PRINCIPAL
# ==============================================================================
st.markdown("<h1 class='glow-title'>SOURCE ISABEE</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='glow-subtitle'>{translate('Anciennes épreuves et sujets d\'examens... Développé par Bertcal.', 'Past exams and assessment papers... Developed by Bertcal.')}</p>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="welcome-banner">
        <p class="welcome-text">🌟 {translate("BIENVENUE SUR VOTRE PLATEFORME D'EXCELLENCE ACADÉMIQUE !", "WELCOME TO YOUR ACADEMIC EXCELLENCE PLATFORM!")} 🌟</p>
        <p style="margin: 5px 0 0 0; opacity:0.8; font-size:0.95rem; color:#FFFFFF;">{translate("Accédez instantanément aux archives de vos filières pour propulser vos résultats.", "Get instant access to your department archives to skyrocket your results.")}</p>
    </div>
""", unsafe_allow_html=True)

df_view = serveur_data["db"].copy()
if f_cycle != translate("Tous", "All"): df_view = df_view[df_view['Cycle'] == f_cycle]
if f_filiere != translate("Toutes", "All Departments"): df_view = df_view[df_view['Filière'] == f_filiere]
if f_type != translate("Tous", "All"): df_view = df_view[df_view['Type'] == f_type]

# ==============================================================================
# 5. ONGLETS DE NAVIGATION PRINCIPAUX (ARCHIVES, PAIEMENT, INTERACT, SECURE DEV, PARAMÈTRES PERSISTANTS)
# ==============================================================================
tab_public_content, tab_payment_gateway, tab_public_interact, tab_dev_zone, tab_global_settings = st.tabs([
    translate("📂 ARCHIVES ACADÉMIQUES", "📂 ACADEMIC ARCHIVES"), 
    translate("💳 ACHAT ACCÈS ÉLITE (CAMPAY INTERNET)", "💳 PURCHASE ELITE ACCESS (CAMPAY)"),
    translate("💬 DISCUSSIONS & SUGGESTIONS", "💬 DISCUSSIONS & SUGGESTIONS"), 
    translate("🔒 ACCÈS DÉVELOPPEUR", "🔒 DEVELOPER ACCESS"),
    translate("⚙️ PARAMÈTRES DU SYSTÈME", "⚙️ SYSTEM SETTINGS") # Placé ici pour rester indéfiniment là !
])

# --- ONGLET 1 : ARCHIVES PUBLIC ---
with tab_public_content:
    st.markdown(f"### 🔍 {translate('Rechercher une archive', 'Search an archive')}")
    search_bar = st.text_input(translate("Saisir le nom d'une UE :", "Enter course title:"), placeholder="Ex: Thermodynamique...")
    
    if search_bar:
        matches = []
        for idx, row in df_view.iterrows():
            sim = difflib.SequenceMatcher(None, search_bar.lower(), row['Matière'].lower()).ratio()
            if search_bar.lower() in row['Matière'].lower() or sim > 0.4: matches.append(row)
        df_view = pd.DataFrame(matches) if matches else pd.DataFrame(columns=df_view.columns)

    if df_view.empty:
        st.info(translate("Aucun document trouvé pour ces critères.", "No documents found matching criteria."))
    else:
        def incrementer_compteur_telechargement(doc_id):
            serveur_data["db"].loc[serveur_data["db"]['id'] == doc_id, 'Downloads'] += 1

        for idx, row in df_view.iterrows():
            badge = f"<span class='badge-premium'>💎 {translate('PREMIUM (Corrigé)', 'PREMIUM (Solved)')}</span>" if row['Premium'] else f"<span class='badge-free'>🆓 {translate('GRATUIT', 'FREE')}</span>"
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="color:#FFFFFF; margin:0;">{row['Matière']}</h4>
                        {badge}
                    </div>
                    <p style="font-size:0.85rem; opacity:0.8; margin: 5px 0; color:#E5E7EB;">
                        <b>{translate('Filière', 'Department')} :</b> {row['Filière']} | <b>{translate('Niveau', 'Level')} :</b> {row['Niveau']} | <b>{translate('Session', 'Session')} :</b> {row['Année']}<br>
                        📊 {translate('Téléchargé', 'Downloaded')} {row['Downloads']} {translate('fois.', 'times.')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if row['Premium'] and not st.session_state.is_premium_user:
                    st.button(translate("🔒 Débloquer le corrigé (300F requis)", "🔒 Unlock solved paper (300F required)"), key=f"l_{row['id']}", disabled=True)
                else:
                    try:
                        content_pdf = row["file_bytes"] if ("file_bytes" in row.index and pd.notna(row["file_bytes"])) else b"%PDF-1.5\n% Document Virtuel Source Isabee"
                    except:
                        content_pdf = b"%PDF-1.5\n% Document Virtuel Source Isabee"
                    
                    st.download_button(
                        label=translate("📥 Télécharger le PDF", "📥 Download PDF"),
                        data=content_pdf,
                        file_name=f"{row['Matière'].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"d_{row['id']}",
                        on_click=incrementer_compteur_telechargement,
                        args=(row['id'],)
                    )
            with c2:
                if st.button(translate("⭐ Garder en Favori", "⭐ Mark as Favorite"), key=f"f_{row['id']}"):
                    serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Favori'] = True
                    st.toast(translate("Ajouté aux favoris privés!", "Added to private favorites!"))

# --- ONGLET 2 : PASSERELLE DE PAIEMENT CAMPAY EN DIRECT ---
with tab_payment_gateway:
    st.markdown(f"### ⚡ {translate('Passerelle Réelle Directe par API Campay', 'Live Gateway via CamPay API')}")
    
    mode_actuel = serveur_data["config"]["campay_mode"]
    st.warning(f"{translate('Configuration actuelle :', 'Current config:')} **Mode {mode_actuel}**. {translate('Les fonds seront routés automatiquement.', 'Funds will be automatically routed.')}")
    
    col_pay_form, col_pay_info = st.columns([2, 1])
    
    with col_pay_form:
        st.markdown(f"#### {translate('Formulaire d\'Abonnement Automatisé', 'Automated Subscription Form')}")
        operator = st.radio(translate("Sélectionnez votre opérateur :", "Select your provider:"), ["Orange Money", "MTN MoMo"])
        
        if mode_actuel == "Démo":
            st.info(translate("💡 En mode Démo, la valeur est fixée à 25 XAF au lieu de 300F maximum, conformément aux spécifications CamPay.", "💡 Demo mode set to 25 XAF for testing."))
            montant_reel = 25
        else:
            formule = st.selectbox(translate("Formule Élite :", "Elite Pack:"), ["300 F CFA - Accès Standard Unique", "500 F CFA - Pack Révision Intensive"])
            montant_reel = 300 if "300" in formule else 500

        phone_pay = st.text_input(translate("Entrez le numéro Camerounais à débiter (9 chiffres) :", "Enter 9-digit Cameroon phone number:"), placeholder="Ex: 6XXXXXXXX")
        
        if st.button(translate("🚀 LANCER LA DEMANDE DE RETRAIT EN DIRECT", "🚀 TRIGGER LIVE PAYMENT REQUEST")):
            if len(phone_pay) != 9 or not phone_pay.isdigit():
                st.error(translate("Format invalide. Indiquez les 9 chiffres du numéro de téléphone.", "Invalid format. Exactly 9 digits required."))
            else:
                status_box = st.empty()
                progress_bar = st.progress(0)
                status_box.warning(translate("🔄 Authentification auprès des serveurs CamPay...", "🔄 Authenticating with CamPay servers..."))
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
                    status_box.info(translate("📲 Requête Push USSD émise. Regarde ton téléphone...", "📲 Push USSD requested. Check your phone pin prompt..."))
                    
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
                        status_box.info(f"⏳ Verification PIN ({check+1}/5)...")
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
                        status_box.error("❌ La transaction a échoué.")
                        
                except Exception as e:
                    status_box.error(f"🔌 Erreur de communication API.")
                    
    with col_pay_info:
        st.markdown(f"#### {translate('Comptes de Réception Actifs', 'Active Destination Accounts')}")
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
    st.markdown(f"### 🗣️ {translate('Espace Interactif des Étudiants', 'Students Communication Hub')}")
    col_comm, col_sug = st.columns(2)
    
    with col_comm:
        st.subheader("💬 Commentaires")
        for c in serveur_data["interactions"]["commentaires"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:8px;'>💬 {c}</div>", unsafe_allow_html=True)
        
        with st.form("new_comment_form", clear_on_submit=True):
            txt_c = st.text_input(translate("Laisser un commentaire :", "Leave a comment:"))
            if st.form_submit_button(translate("Envoyer le commentaire", "Send Comment")) and txt_c:
                serveur_data["interactions"]["commentaires"].append(txt_c)
                st.rerun()

    with col_sug:
        st.subheader("💡 Suggestions")
        for s in serveur_data["interactions"]["suggestions"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:8px;'>💡 {s}</div>", unsafe_allow_html=True)
            
        with st.form("new_sug_form", clear_on_submit=True):
            txt_s = st.text_input(translate("Proposer un document ou une idée :", "Suggest a paper or an idea:"))
            if st.form_submit_button(translate("Soumettre la suggestion", "Submit Suggestion")) and txt_s:
                serveur_data["interactions"]["suggestions"].append(txt_s)
                st.rerun()

# ==============================================================================
# 6. PARTIE PRIVÉE : FILTRE DES RÔLES & ACCÈS DE HAUT NIVEAU
# ==============================================================================
with tab_dev_zone:
    st.markdown(f"### 🔒 {translate('Espace d\'Infrastructure Sécurisé', 'Secure Infrastructure Zone')}")
    
    if st.session_state.dev_role is None:
        input_pwd = st.text_input(translate("Entrez votre clé d'accès d'infrastructure :", "Enter architecture access key:"), type="password")
        if st.button(translate("Vérifier le niveau d'autorisation", "Verify Clearance Level")):
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
                        st.warning("⚠️ Document stocké dans le sas d'attente.")
                    else:
                        new_dataframe_row = pd.DataFrame([temp_row])
                        serveur_data["db"] = pd.concat([serveur_data["db"], new_dataframe_row], ignore_index=True)
                        st.success("✅ Document injecté directement en base publique.")
                        st.rerun()
                else:
                    st.error("Veuillez renseigner un nom d'UE ainsi qu'un fichier PDF valide.")

        # ZONE SECRÈTE DU CONCEPTEUR EN CHEF (SUPPRESSION AJOUTÉE ICI)
        if st.session_state.dev_role == "Chief":
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="chief-vault">
                    <h2 style="color: #A78BFA; margin:0;">👁️ COFFRE-FORT VIRTUEL DU CONCEPTEUR EN CHEF</h2>
                    <p style="font-size:0.9rem; opacity:0.8;">Contrôle total sur l'application et l'infrastructure financière.</p>
                </div>
            """, unsafe_allow_html=True)
            
            sub_tab_vault, sub_tab_tickets_mgr, sub_tab_global_db = st.tabs([
                "📥 VALIDATION DES SOUMISSIONS",
                "🎫 INJECTEUR DE TICKETS",
                "👑 PANNEAU DE SUPPRESSION DES ÉPREUVES INUTILES"
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
                            st.warning("Élément purgé.")
                            st.rerun()

            with sub_tab_tickets_mgr:
                st.markdown("#### Génération manuelle de secours")
                col_gen, col_list = st.columns(2)
                with col_gen:
                    num_to_gen = st.number_input("Nombre de pass à injecter :", min_value=1, max_value=50, value=5)
                    if st.button("⚡ Injecter de force"):
                        for _ in range(num_to_gen):
                            code = "ISABEE-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
                            serveur_data["tickets"].append(code)
                        st.success(f"Modifications appliquées au registre.")
                        st.rerun()
                with col_list:
                    st.write(serveur_data["tickets"])

            with sub_tab_global_db:
                st.markdown("#### 🗑️ Purge Absolue des Épreuves Inutiles")
                
                col_stat1, col_stat2 = st.columns(2)
                col_stat1.metric("Total Sujets Actifs", len(serveur_data["db"]))
                col_stat2.metric("Total Tickets Valides", len(serveur_data["tickets"]))
                
                st.markdown("---")
                st.markdown("##### Liste des épreuves déployées sur le serveur")
                
                # Système d'élimination d'épreuves directes
                if serveur_data["db"].empty:
                    st.info("Aucune archive présente dans la base de données actuellement.")
                else:
                    for idx, row in serveur_data["db"].iterrows():
                        col_n, col_b = st.columns([5, 1])
                        col_n.markdown(f"🔹 **ID: {row['id']}** | {row['Matière']} (*{row['Filière']} - {row['Niveau']}*)")
                        if col_b.button("Supprimer", key=f"del_sec_{row['id']}"):
                            serveur_data["db"] = serveur_data["db"][serveur_data["db"]['id'] != row['id']]
                            st.toast(f"Épreuve supprimée définitivement : {row['Matière']}")
                            st.rerun()

# ==============================================================================
# 7. PARAMÈTRES DU SYSTÈME (INDÉFINIMENT VISIBLES ET COMPLÈTEMENT OPÉRATIONNELS)
# ==============================================================================
with tab_global_settings:
    st.markdown(f"### ⚙️ {translate('Panneau de Configuration Général et Visuel', 'System Configuration & Layout Engine')}")
    st.write(translate("Modifiez les variables structurelles ici. Les changements s'appliquent immédiatement sans altérer le code source.", "Modify operational layouts here. Values persist reactively across pages."))
    
    st.markdown("---")
    
    # 1. Gestion de la Langue
    st.markdown(f"##### 🌐 {translate('Sélection de la Langue globale', 'Global Language Driver')}")
    selected_language = st.selectbox(
        translate("Langue de l'interface", "Interface Core Language"), 
        ["Français", "English"], 
        index=0 if serveur_data["config"]["language"] == "Français" else 1
    )
    if selected_language != serveur_data["config"]["language"]:
        serveur_data["config"]["language"] = selected_language
        st.rerun()

    st.markdown("---")

    # 2. Tailles et Polices
    st.markdown(f"##### 📏 {translate('Tailles de Police & Affichage', 'Typography & Sizing Engine')}")
    col_size1, col_size2 = st.columns(2)
    with col_size1:
        new_f_size = st.slider(translate("Taille de la police générale (px)", "Main Body Font Size (px)"), min_value=12, max_value=24, value=int(f_size))
        if new_f_size != f_size:
            serveur_data["config"]["font_size"] = new_f_size
            st.rerun()
    with col_size2:
        new_t_size = st.slider(translate("Taille du Grand Titre SOURCE (rem)", "Main Title Size (rem)"), min_value=3.0, max_value=12.0, value=float(t_size), step=0.5)
        if new_t_size != t_size:
            serveur_data["config"]["title_size"] = new_t_size
            st.rerun()

    st.markdown("---")

    # 3. Couleurs du Système
    st.markdown(f"##### 🎨 {translate('Thème & Identification Couleur', 'Color Schemes & Branding Customization')}")
    col_col1, col_col2 = st.columns(2)
    with col_col1:
        new_p_color = st.color_picker(translate("Couleur Primaire Éclatante", "Primary Glowing Color"), value=p_color)
        if new_p_color != p_color:
            serveur_data["config"]["primary_color"] = new_p_color
            st.rerun()
    with col_col2:
        new_s_color = st.color_picker(translate("Couleur Secondaire", "Secondary Accent Color"), value=s_color)
        if new_s_color != s_color:
            serveur_data["config"]["secondary_color"] = new_s_color
            st.rerun()

    st.markdown("---")

    # 4. Paramètres financiers et Campay
    st.markdown(f"##### 💳 {translate('Configuration Passerelle CamPay & Numéros Cibles', 'Financial Infrastructure & CamPay API Routing')}")
    col_pay1, col_pay2 = st.columns(2)
    with col_pay1:
        serveur_data["config"]["orange_target"] = st.text_input("Orange Money Target (+237) :", value=serveur_data["config"]["orange_target"])
        serveur_data["config"]["campay_username"] = st.text_input("CamPay APP USERNAME :", value=serveur_data["config"]["campay_username"])
        new_campay_mode = st.selectbox("CamPay Payment Mode :", ["Démo", "Réel"], index=0 if mode_actuel == "Démo" else 1)
        if new_campay_mode != mode_actuel:
            serveur_data["config"]["campay_mode"] = new_campay_mode
            st.rerun()
    with col_pay2:
        serveur_data["config"]["mtn_target"] = st.text_input("MTN MoMo Target (+237) :", value=serveur_data["config"]["mtn_target"])
        serveur_data["config"]["campay_password"] = st.text_input("CamPay APP PASSWORD :", value=serveur_data["config"]["campay_password"], type="password")

    st.markdown("---")
    st.info(translate("🔒 Toutes les modifications configurées ci-dessus restent actives indéfiniment sur la mémoire globale partagée de l'application.", "🔒 All modified attributes configured above are dynamically bound to the application's runtime structure permanently."))
