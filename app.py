import streamlit as st
import pandas as pd
import difflib
from datetime import datetime

# ==============================================================================
# 1. ARCHITECTURE VISUELLE & INJECTION CSS AVANCÉE
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
    
    /* FORCE LE THÈME SOMBRE ET FLUIDE */
    .stApp, [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {
        background: #010D08 !important;
        background-image: linear-gradient(135deg, #010D08 0%, #021F14 50%, #000503 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    
    /* BOUTON FLÈCHE FLOTTANTE DE LA SIDEBAR ULTRA-VISIBLE ET AGRANDIE */
    [data-testid="collapsedControl"] {
        background-color: #021F14 !important;
        border: 2px solid #10B981 !important;
        border-radius: 50% !important;
        width: 55px !important;
        height: 55px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 0 20px #10B981 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    [data-testid="collapsedControl"] svg {
        width: 32px !important;
        height: 32px !important;
        fill: #34D399 !important;
        color: #34D399 !important;
    }
    [data-testid="collapsedControl"]:hover {
        transform: scale(1.15) rotate(180deg) !important;
        box-shadow: 0 0 30px #34D399 !important;
    }
    
    /* TITRES LUMINEUX NÉON */
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
        text-align: center;
        font-size: 1.2rem;
        color: #A7F3D0;
        margin-bottom: 30px;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .welcome-banner {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.2) 50%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.25);
    }
    
    .welcome-text {
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #34D399;
        text-shadow: 0 0 10px rgba(52, 211, 153, 0.6);
        margin: 0;
    }

    /* MENUS DESIGN BOUTONS */
    .stTabs [data-baseweb="tab-list"] { gap: 15px !important; background-color: transparent !important; padding: 10px 0 !important; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 14px !important;
        padding: 16px 24px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #E5E7EB !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border-color: #34D399 !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
    }

    /* CADRES CADRÉS POUR LOGOS DANS LA SIDEBAR */
    .big-logo-box {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed #10B981 !important;
        border-radius: 12px;
        padding: 20px 5px;
        text-align: center;
        color: #34D399 !important;
        font-weight: 800;
        font-size: 0.8rem;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* SIGNATURE PROFESSIONNELLE EN BLEU ET CENTRÉE */
    .sidebar-blue-footer {
        border-top: 1px solid rgba(56, 189, 248, 0.2);
        padding-top: 20px;
        margin-top: 40px;
        font-size: 0.88rem;
        line-height: 1.6;
        color: #38BDF8 !important;
        text-align: center !important;
    }
    .sidebar-blue-footer b, .sidebar-blue-footer strong {
        color: #00E5FF !important;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
    }
    .badge-premium { background: linear-gradient(90deg, #F59E0B, #D97706); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; }
    .badge-free { background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; }
    
    /* COMPTEURS ET ALERTES DESIGN MAISON VIRTUELLE */
    .owner-box {
        background: rgba(56, 189, 248, 0.05) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. LE CERVEAU CENTRALISÉ AVEC DOUBLE SÉCURITÉ & LISTE DE TICKETS INTELLIGENTE
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
    # Base de sujets avec colonne 'Approuvé' pour le contrôle du Concepteur
    base_sujets = pd.DataFrame([
        {"id": 1, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Thermodynamique et Transfert Thermique", "Enseignant": "Dr. Eko", "Type": "Examen", "Année": "2024-2025", "Premium": False, "Downloads": 145, "Date": "12/03/2026", "Favori": False, "Approuvé": True},
        {"id": 2, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Mécanique des Fluides Appliquée + CORRIGÉ", "Enseignant": "Pr. Ndongo", "Type": "Examen", "Année": "2024-2025", "Premium": True, "Downloads": 92, "Date": "18/03/2026", "Favori": False, "Approuvé": True}
    ])
    
    # Espace des interactions partagées
    interactions = {
        "commentaires": ["Excellente lisibilité sur les sujets de Génie Énergétique.", "Sujet de Thermo Ing4 disponible !"],
        "suggestions": ["Ajouter les TP de chimie des solutions pour les L1."],
        "avis": [{"user": "Anonyme", "note": 5, "text": "L'interface à 300F vaut largement le coup !"}],
        "remerciements": ["Merci à Bertcal pour cette initiative de génie sur le campus."]
    }
    
    # Base intelligente de tickets à usage unique (Single Use Security)
    tickets_actifs = {
        "ISABEE-7762": {"statut": "Disponible", "date_creation": "15/06/2026", "utilise_par": ""},
        "ISABEE-3341": {"statut": "Disponible", "date_creation": "15/06/2026", "utilise_par": ""}
    }
    
    # Configuration des accès secrets de l'infrastructure
    config = {
        "copilot_password": "copilote",  # Mot de passe pour tes copilotes
        "owner_password": "owner",      # Ton mot de passe maître personnel (Maison Virtuelle)
        "logo_isabee": None,
        "logo_ubertoua": None
    }
    return {"db": base_sujets, "interactions": interactions, "tickets": tickets_actifs, "config": config}

# Appel du serveur de stockage global
serveur_data = initialiser_base_globale()

# Variables de sessions locales (propres à chaque téléphone individuel)
if 'is_premium_user' not in st.session_state:
    st.session_state.is_premium_user = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = "Visiteur" # Peut devenir "Copilote" ou "Owner"

# ==============================================================================
# 3. BARRE LATÉRALE (LOGOS INTERACTIFS, FILTRES, SIGNATURE BLEUE CENTRÉE)
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
            
    st.markdown("### 🔑 SÉCURITÉ & PREMIUM")
    user_matricule = st.text_input("Identifiant / Matricule Étudiant :", value="22I0000B")

    # Zone d'activation avec processus d'information de paiement
    if not st.session_state.is_premium_user:
        st.markdown("""
            <div style="background:rgba(245,158,11,0.1); border:1px solid #F59E0B; padding:10px; border-radius:8px; font-size:0.8rem; margin-bottom:10px;">
                <b>Frais d'activation : 300F</b><br>
                🟠 Orange Money : <b>696 07 56 60</b><br>
                🟡 MTN MoMo : <b>654 04 67 92</b><br>
                <i>Envoyez vos frais pour recevoir votre ticket unique.</i>
            </div>
        """, unsafe_allow_html=True)
        
        input_ticket = st.text_input("Saisir votre Ticket d'accès Unique :", type="default")
        if st.button("Valider et Activer mon Ticket"):
            input_ticket = input_ticket.strip()
            if input_ticket in serveur_data["tickets"] and serveur_data["tickets"][input_ticket]["statut"] == "Disponible":
                # Consommation immédiate du ticket à usage unique
                serveur_data["tickets"][input_ticket]["statut"] = "Consommé"
                serveur_data["tickets"][input_ticket]["utilise_par"] = user_matricule
                st.session_state.is_premium_user = True
                st.success("🎉 Ticket validé avec succès ! Mode Premium déverrouillé.")
                st.rerun()
            else:
                st.error("Ticket invalide, expiré ou déjà consommé.")
    else:
        st.success("👑 Accès Premium Activé")
        if st.button("Désactiver le Premium"):
            st.session_state.is_premium_user = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎛️ FILTRES DE SÉLECTION")
    f_cycle = st.selectbox("Cycle d'études", ["Tous", "Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
    f_filiere = st.selectbox("Filière", ["Toutes"] + FILIERES)
    f_type = st.selectbox("Type d'évaluation", ["Tous", "CC", "Examen", "Rattrapage", "TP"])

    # Coordonnées professionnelles, centrées et bleues
    st.markdown(f"""
        <div class="sidebar-blue-footer">
            Développé par: <b>Chemta Caleb Bertrand</b><br>
            étudiant ingénieur en génie énergétique.<br>
            <br>
            <strong>CONTACT COMMERCIAL :</strong><br>
            • Téléphone : +237 696 07 56 60<br>
            • Email : bertrandchemtacaleb@gmail.com<br>
            • Campus : ISABEE / U-BERTOUA
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. EN-TÊTE PRINCIPAL PUBLIC
# ==============================================================================
st.markdown("<h1 class='glow-title'>SOURCE ISABEE</h1>", unsafe_allow_html=True)
st.markdown("<p class='glow-subtitle'>Anciennes épreuves et sujets d'examens... Développé par Bertcal.</p>", unsafe_allow_html=True)

st.markdown("""
    <div class="welcome-banner">
        <p class="welcome-text">🌟 BIENVENUE SUR VOTRE PLATEFORME D'EXCELLENCE ACADÉMIQUE ! 🌟</p>
        <p style="margin: 5px 0 0 0; opacity:0.8; font-size:0.95rem; color:#FFFFFF;">Accédez instantanément aux archives de vos filières pour propulser vos résultats.</p>
    </div>
""", unsafe_allow_html=True)

# Application des filtres : Les utilisateurs voient uniquement les fichiers approuvés
df_view = serveur_data["db"][serveur_data["db"]['Approuvé'] == True].copy()
if f_cycle != "Tous": df_view = df_view[df_view['Cycle'] == f_cycle]
if f_filiere != "Toutes": df_view = df_view[df_view['Filière'] == f_filiere]
if f_type != "Tous": df_view = df_view[df_view['Type'] == f_type]

# ==============================================================================
# 5. ONGLETS DE SÉPARATION (PUBLIC & ZONE TECHNIQUE PAR MOT DE PASSE)
# ==============================================================================
tab_public_content, tab_public_interact, tab_dev_zone = st.tabs([
    "📂 ARCHIVES ACADÉMIQUES", 
    "💬 DISCUSSIONS & SUGGESTIONS", 
    "🔒 ACCÈS PANNEAU TECHNIQUE"
])

# ------------------------------------------------------------------------------
# ZONE 1 : INTERFACE PUBLIQUE
# ------------------------------------------------------------------------------
with tab_public_content:
    st.markdown("### 🔍 Rechercher une archive")
    search_bar = st.text_input("Saisir le nom d'une UE :", placeholder="Ex: Thermodynamique...")
    
    if search_bar:
        matches = []
        for idx, row in df_view.iterrows():
            sim = difflib.SequenceMatcher(None, search_bar.lower(), row['Matière'].lower()).ratio()
            if search_bar.lower() in row['Matière'].lower() or sim > 0.4:
                matches.append(row)
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
                    st.button("🔒 Débloquer le corrigé (Ticket Requis)", key=f"l_{row['id']}", disabled=True)
                else:
                    if st.button(f"📥 Télécharger le PDF", key=f"d_{row['id']}"):
                        serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Downloads'] += 1
                        st.success("Téléchargement lancé !")
            with c2:
                if st.button("⭐ Garder en Favori", key=f"f_{row['id']}"):
                    serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Favori'] = True
                    st.toast("Ajouté aux favoris privés !")

with tab_public_interact:
    st.markdown("### 🗣️ Espace Interactif des Étudiants (Commentaires & Suggestions)")
    col_comm, col_sug = st.columns(2)
    
    with col_comm:
        st.subheader("💬 Commentaires")
        for c in serveur_data["interactions"]["commentaires"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:8px;'>💬 {c}</div>", unsafe_allow_html=True)
        
        with st.form("new_comment_form", clear_on_submit=True):
            txt_c = st.text_input("Laisser un commentaire :")
            if st.form_submit_button("Envoyer") and txt_c:
                serveur_data["interactions"]["commentaires"].append(txt_c)
                st.rerun()

    with col_sug:
        st.subheader("💡 Suggestions d'amélioration")
        for s in serveur_data["interactions"]["suggestions"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:8px;'>💡 {s}</div>", unsafe_allow_html=True)
            
        with st.form("new_sug_form", clear_on_submit=True):
            txt_s = st.text_input("Proposer un document ou un changement :")
            if st.form_submit_button("Soumettre") and txt_s:
                serveur_data["interactions"]["suggestions"].append(txt_s)
                st.rerun()

# ------------------------------------------------------------------------------
# ZONE 2 : PANNEAU DES PASSERELLES (SÉCURISÉ PAR DEUX MOTS DE PASSE DISTINCTS)
# ------------------------------------------------------------------------------
with tab_dev_zone:
    if st.session_state.user_role == "Visiteur":
        st.markdown("### 🔐 Identification de Sécurité")
        st.info("Le système détecte automatiquement vos privilèges selon le code secret introduit.")
        
        secret_code = st.text_input("Entrer votre clé d'authentification :", type="password")
        if st.button("Ouvrir la session"):
            if secret_code == serveur_data["config"]["owner_password"]:
                st.session_state.user_role = "Owner"
                st.success("Bienvenue dans votre Maison Virtuelle, Concepteur en chef !")
                st.rerun()
            elif secret_code == serveur_data["config"]["copilot_password"]:
                st.session_state.user_role = "Copilote"
                st.success("Connexion Copilote établie. Accès restreint accordé.")
                st.rerun()
            else:
                st.error("Clé secrète invalide.")
    else:
        # Affichage du profil connecté
        col_title, col_logout = st.columns([4, 1])
        if st.session_state.user_role == "Owner":
            col_title.markdown("#### 🏛️ MAISON VIRTUELLE DE BERTCAL (Accès Maître)")
        else:
            col_title.markdown("#### 🚀 ESPACE COPILOTE (Téléversement Uniquement)")
            
        if col_logout.button("🔒 Fermer la Session"):
            st.session_state.user_role = "Visiteur"
            st.rerun()
            
        st.markdown("---")
        
        # --- CAS 1 : VUE RESTREINTE POUR LES COPILOTES ---
        if st.session_state.user_role == "Copilote":
            st.warning("⚠️ Vos fichiers seront envoyés au Concepteur en chef pour validation avant publication officielle.")
            with st.form("copilot_upload_form"):
                u_mat = st.text_input("Nom de la matière :")
                u_cyc = st.selectbox("Cycle", ["Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
                u_fil = st.selectbox("Filière", FILIERES)
                u_niv = st.selectbox("Niveau", ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5", "M1", "M2"])
                u_type = st.selectbox("Type", ["CC", "Examen", "Rattrapage", "TP"])
                u_prof = st.text_input("Enseignant :")
                u_prem = st.checkbox("Mettre en Premium (Bloqué derrière ticket)")
                u_file = st.file_uploader("Fichier épreuve")
                
                if st.form_submit_button("SOUMETTRE À BERTCAL"):
                    if u_mat and u_file:
                        new_row = {
                            "id": len(serveur_data["db"]) + 1, "Cycle": u_cyc, "Filière": u_fil, "Niveau": u_niv, 
                            "Matière": u_mat, "Enseignant": u_prof, "Type": u_type, "Année": "2025-2026", 
                            "Premium": u_prem, "Downloads": 0, "Date": datetime.today().strftime('%d/%m/%Y'), 
                            "Favori": False, 
                            "Approuvé": False # En attente de ta validation !
                        }
                        serveur_data["db"] = pd.concat([serveur_data["db"], pd.DataFrame([new_row])], ignore_index=True)
                        st.success("Fichier mis en attente d'approbation avec succès !")
                        
        # --- CAS 2 : MAISON VIRTUELLE DU CONCEPTEUR EN CHEF (TOUS LES DROITS) ---
        elif st.session_state.user_role == "Owner":
            sub_tabs = st.tabs([
                "📥 COMPTEUR & APPROBATIONS", 
                "🎫 ENTRÉE ET TICKETS INTELLIGENTS", 
                "🚀 DÉPÔT ÉLITE (DIRECT)", 
                "👑 PANNEAU DE CONTRÔLE", 
                "🤝 RECONNAISSANCE & CONFIGS"
            ])
            
            # Sous-onglet 1 : Approbation des fichiers envoyés par les copilotes
            with sub_tabs[0]:
                st.markdown("#### 🔎 Fichiers en attente de votre validation")
                df_pending = serveur_data["db"][serveur_data["db"]['Approuvé'] == False]
                
                if df_pending.empty:
                    st.info("Aucun document en attente d'approbation pour le moment.")
                else:
                    for idx, row in df_pending.iterrows():
                        with st.container():
                            st.markdown(f"""
                                <div class="owner-box">
                                    <b>Matière :</b> {row['Matière']} | <b>Filière :</b> {row['Filière']} ({row['Niveau']})<br>
                                    <b>Type :</b> {row['Type']} | <b>Premium demandé :</b> {'Oui' if row['Premium'] else 'Non'}
                                </div>
                            """, unsafe_allow_html=True)
                            col_app, col_rej = st.columns(2)
                            if col_app.button("✅ Approuver et Publier", key=f"app_{row['id']}"):
                                serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Approuvé'] = True
                                st.success("Document visible par les étudiants !")
                                st.rerun()
                            if col_rej.button("❌ Rejeter / Supprimer", key=f"rej_{row['id']}"):
                                serveur_data["db"] = serveur_data["db"][serveur_data["db"]['id'] != row['id']]
                                st.warning("Document rejeté.")
                                st.rerun()
            
            # Sous-onglet 2 : Gestion des Tickets Intelligents à Usage Unique
            with sub_tabs[1]:
                st.markdown("#### 🎫 Générateur de Tickets d'Accès Unique")
                
                with st.form("ticket_generation_form"):
                    nouveau_code = st.text_input("Créer un Code Ticket Unique (Ex: ISABEE-XXXX) :").strip()
                    if st.form_submit_button("Enregistrer et Activer le Ticket"):
                        if nouveau_code:
                            if nouveau_code not in serveur_data["tickets"]:
                                serveur_data["tickets"][nouveau_code] = {
                                    "statut": "Disponible", 
                                    "date_creation": datetime.today().strftime('%d/%m/%Y'),
                                    "utilise_par": ""
                                }
                                st.success(f"Ticket {nouveau_code} prêt à être envoyé par SMS/WhatsApp !")
                                st.rerun()
                            else:
                                st.error("Ce code existe déjà.")
                
                st.markdown("---")
                st.markdown("#### 📊 Suivi d'utilisation des tickets en temps réel")
                # Affichage sous forme de tableau propre
                data_t = []
                for k, v in serveur_data["tickets"].items():
                    data_t.append({"Code Ticket": k, "Statut de Sécurité": v["statut"], "Créé le": v["date_creation"], "Consommé par": v["utilise_par"]})
                st.dataframe(pd.DataFrame(data_t), use_container_width=True)

            # Sous-onglet 3 : Dépôt direct par l'owner (Approuvé automatiquement)
            with sub_tabs[2]:
                st.markdown("#### Téléversement direct (Auto-approuvé)")
                with st.form("owner_direct_upload"):
                    u_mat = st.text_input("Nom de la matière :")
                    u_cyc = st.selectbox("Cycle", ["Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
                    u_fil = st.selectbox("Filière", FILIERES)
                    u_niv = st.selectbox("Niveau", ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5", "M1", "M2"])
                    u_type = st.selectbox("Type", ["CC", "Examen", "Rattrapage", "TP"])
