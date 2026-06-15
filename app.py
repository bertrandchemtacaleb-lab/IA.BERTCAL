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
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. LE CERVEAU CENTRALISÉ (PARTAGÉ ENTRE TOUS LES TÉLÉPHONES)
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
    """Cette fonction crée la mémoire partagée unique pour tout le serveur."""
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
    config = {
        "dev_password": "admin",
        "logo_isabee": None,
        "logo_ubertoua": None
    }
    return {"db": base_sujets, "interactions": interactions, "config": config}

# Chargement du Cerveau Commun
serveur_data = initialiser_base_globale()

# Initialisation des variables privées (Propres à chaque téléphone)
if 'is_premium_user' not in st.session_state:
    st.session_state.is_premium_user = False
if 'dev_logged_in' not in st.session_state:
    st.session_state.dev_logged_in = False

# ==============================================================================
# 3. BARRE LATÉRALE (LOGOS INTERACTIFS, FILTRES, SIGNATURE BLEUE CENTRÉE)
# ==============================================================================
with st.sidebar:
    # Lecture des logos depuis le serveur commun
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
            
    st.markdown("### 🔑 ACCÈS COMPTE")
    user_matricule = st.text_input("Identifiant Matricule Étudiant :", value="22I0000B")

    # Système Premium local à chaque étudiant
    if not st.session_state.is_premium_user:
        activation_key = st.text_input("Saisir la clé Premium (300F) :", type="password")
        if st.button("Activer Premium"):
            if activation_key == "isabee300":
                st.session_state.is_premium_user = True
                st.rerun()
    else:
        st.success("👑 Premium Actif")
        if st.button("Retour Mode Gratuit"):
            st.session_state.is_premium_user = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎛️ FILTRES DE SÉLECTION")
    f_cycle = st.selectbox("Cycle d'études", ["Tous", "Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
    f_filiere = st.selectbox("Filière", ["Toutes"] + FILIERES)
    f_type = st.selectbox("Type d'évaluation", ["Tous", "CC", "Examen", "Rattrapage", "TP"])

    # Informations de contact impeccablement centrées et bleues
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
# 4. EN-TÊTE PRINCIPAL PUBLIC (SIGNE BERTCAL)
# ==============================================================================
st.markdown("<h1 class='glow-title'>SOURCE ISABEE</h1>", unsafe_allow_html=True)
st.markdown("<p class='glow-subtitle'>Anciennes épreuves et sujets d'examens... Développé par Bertcal.</p>", unsafe_allow_html=True)

st.markdown("""
    <div class="welcome-banner">
        <p class="welcome-text">🌟 BIENVENUE SUR VOTRE PLATEFORME D'EXCELLENCE ACADÉMIQUE ! 🌟</p>
        <p style="margin: 5px 0 0 0; opacity:0.8; font-size:0.95rem; color:#FFFFFF;">Accédez instantanément aux archives de vos filières pour propulser vos résultats.</p>
    </div>
""", unsafe_allow_html=True)

# Application des filtres de recherche sur la base globale
df_view = serveur_data["db"].copy()
if f_cycle != "Tous": df_view = df_view[df_view['Cycle'] == f_cycle]
if f_filiere != "Toutes": df_view = df_view[df_view['Filière'] == f_filiere]
if f_type != "Tous": df_view = df_view[df_view['Type'] == f_type]

# ==============================================================================
# 5. ONGLETS DE SÉPARATION (PUBLIC VS ADMINISTRATEUR)
# ==============================================================================
tab_public_content, tab_public_interact, tab_dev_zone = st.tabs([
    "📂 ARCHIVES ACADÉMIQUES", 
    "💬 DISCUSSIONS & SUGGESTIONS", 
    "🔒 ACCÈS DÉVELOPPEUR"
])

# ------------------------------------------------------------------------------
# PARTIE UTILISATEURS GENERAUX
# ------------------------------------------------------------------------------
with tab_public_content:
    st.markdown("### 🔍 Rechercher une archive")
    search_bar = st.text_input("Saisir le nom d'une UE :", placeholder="Ex: Thermodinamique...")
    
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
                    st.button("🔒 Débloquer le corrigé (300F requis)", key=f"l_{row['id']}", disabled=True)
                else:
                    if st.button(f"📥 Télécharger le PDF", key=f"d_{row['id']}"):
                        serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Downloads'] += 1
                        st.success("Téléchargement lancé !")
            with c2:
                if st.button("⭐ Garder en Favori", key=f"f_{row['id']}"):
                    serveur_data["db"].loc[serveur_data["db"]['id'] == row['id'], 'Favori'] = True
                    st.toast("Ajouté aux favoris privés !")

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

# ------------------------------------------------------------------------------
# PARTIE ADMINISTRATEUR PRIVE
# ------------------------------------------------------------------------------
with tab_dev_zone:
    st.markdown("### 🔐 Espace de Gestion Privé (Bertcal)")
    
    if not st.session_state.dev_logged_in:
        input_pwd = st.text_input("Entrez le mot de passe Développeur :", type="password")
        if st.button("Déverrouiller les accès"):
            if input_pwd == serveur_data["config"]["dev_password"]:
                st.session_state.dev_logged_in = True
                st.success("Authentification réussie !")
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")
    else:
        if st.button("🔒 Déconnexion de l'espace Admin"):
            st.session_state.dev_logged_in = False
            st.rerun()
            
        st.markdown("---")
        sub_tab_upload, sub_tab_fav, sub_tab_control, sub_tab_thanks, sub_tab_config = st.tabs([
            "🚀 DÉPÔT ÉLITE", 
            "⭐ MES FAVORIS", 
            "👑 PANNEAU DE CONTRÔLE", 
            "🤝 RECONNAISSANCE",
            "⚙️ CONFIGURATION INTERNE"
        ])
        
        # 1. DEPOT ELITE
        with sub_tab_upload:
            st.markdown("#### Téléversement de nouvelles épreuves")
            with st.form("upload_form"):
                u_mat = st.text_input("Nom de la matière :")
                u_cyc = st.selectbox("Cycle", ["Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
                u_fil = st.selectbox("Filière", FILIERES)
                u_niv = st.selectbox("Niveau", ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5", "M1", "M2"])
                u_type = st.selectbox("Type", ["CC", "Examen", "Rattrapage", "TP"])
                u_prof = st.text_input("Enseignant :")
                u_prem = st.checkbox("Verrouiller derrière l'accès Premium (300F)")
                u_file = st.file_uploader("Fichier")
                
                # AJUSTEMENT : Bouton placé précisément pour fermer le formulaire correctement
                btn_publier = st.form_submit_button("PUBLIER LE DOCUMENT")
                
            if btn_publier:
                if u_mat and u_file:
                    new_row = {
                        "id": len(serveur_data["db"]) + 1, 
                        "Cycle": u_cyc, 
                        "Filière": u_fil, 
                        "Niveau": u_niv, 
                        "Matière": u_mat, 
                        "Enseignant": u_prof, 
                        "Type": u_type, 
                        "Année": "2025-2026", 
                        "Premium": u_prem, 
                        "Downloads": 0, 
                        "Date": datetime.today().strftime('%d/%m/%Y'), 
                        "Favori": False
                    }
                    # AJUSTEMENT : Découpage propre pour éviter l'erreur de parenthèse (SyntaxError)
                    new_df = pd.DataFrame([new_row])
                    serveur_data["db"] = pd.concat([serveur_data["db"], new_df], ignore_index=True)
                    st.success("Publié sur toutes les machines !")
                    st.rerun()
        
        # 2. MES FAVORIS
        with sub_tab_fav:
            st.markdown("#### Tes favoris enregistrés")
            df_fav = serveur_data["db"][serveur_data["db"]['Favori'] == True]
            if df_fav.empty:
                st.info("Aucun favori enregistré.")
            else:
                for idx, row in df_fav.iterrows():
                    st.write(f"• **{row['Matière']}** ({row['Niveau']})")
        
        # 3. PANNEAU DE CONTRÔLE
        with sub_tab_control:
            st.markdown("#### Gestion Globale en Temps Réel")
            st.dataframe(serveur_data["db"][['Matière', 'Niveau', 'Downloads', 'Premium']], use_container_width=True)
            
            for idx, row in serveur_data["db"].iterrows():
                col_n, col_b = st.columns([4, 1])
                col_n.write(f"🗑️ {row['Matière']} ({row['Niveau']})")
                if col_b.button("Supprimer", key=f"del_{row['id']}"):
                    serveur_data["db"] = serveur_data["db"][serveur_data["db"]['id'] != row['id']]
                    st.rerun()
                    
        # 4. RECONNAISSANCE 
        with sub_tab_thanks:
            col_av, col_rem = st.columns(2)
            with col_av:
                st.write("#### ⭐ Évaluations Reçues")
                for a in serveur_data["interactions"]["avis"]:
                    st.markdown(f"**{a['user']}** ({a['note']}★) : _{a['text']}_")
            with col_rem:
                st.write("#### 🙏 Mots de gratitude reçus")
                for r in serveur_data["interactions"]["remerciements"]:
                    st.write(f"• {r}")
                    
        # 5. CONFIGURATION
        with sub_tab_config:
            st.markdown("#### 🛠️ Paramètres du Système Principal")
            
            new_pwd = st.text_input("Modifier le mot de passe Admin Global :", value=serveur_data["config"]["dev_password"], type="password")
            if st.button("Enregistrer le nouveau mot de passe"):
                serveur_data["config"]["dev_password"] = new_pwd
                st.success("Le nouveau code d'accès administrateur est opérationnel !")
            
            st.markdown("---")
            st.markdown("#### 🖼️ Cadres d'Importation des Logos")
            
            up_isabee = st.file_uploader("Importer le Logo ISABEE :", key="upload_isabee_logo")
            if up_isabee is not None:
                serveur_data["config"]["logo_isabee"] = up_isabee
                st.success("Logo ISABEE enregistré au niveau central !")
                
            up_ubertoua = st.file_uploader("Importer le Logo Université de Bertoua :", key="upload_ubertoua_logo")
            if up_ubertoua is not None:
                serveur_data["config"]["logo_ubertoua"] = up_ubertoua
                st.success("Logo U-BERTOUA enregistré au niveau central !")
                
            if up_isabee or up_ubertoua:
                if st.button("Rafraîchir pour appliquer les nouveaux visuels"):
                    st.rerun()
