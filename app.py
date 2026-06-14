import streamlit as st
import pandas as pd
import difflib
from datetime import datetime

# ==============================================================================
# 1. ARCHITECTURE VISUELLE HAUTE QUALITÉ & GLOW NÉON (CSS PARFAIT POUR MOBILE)
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
    
    /* FORCE LE THÈME SOMBRE SUR TOUS LES APPAREILS (MOBILE & DESKTOP) */
    .stApp, [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {
        background: #010D08 !important;
        background-image: linear-gradient(135deg, #010D08 0%, #021F14 50%, #000503 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Ajustement des textes de la sidebar pour éviter le blanc sur blanc */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    
    /* --- DESIGN DES EN-TÊTES TRÈS LUMINEUX --- */
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
    
    @media (max-width: 768px) {
        .glow-title { font-size: 2.5rem !important; }
    }
    
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

    /* --- TRANSFORMATION DES MENUS EN BOUTONS TRÈS MODERNES --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px !important;
        background-color: transparent !important;
        padding: 10px 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 14px !important;
        padding: 18px 28px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #E5E7EB !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(16, 185, 129, 0.1) !important;
        border-color: #10B981 !important;
        transform: translateY(-2px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border-color: #34D399 !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
    }

    /* --- COMPOSANTS DE LA SIDEBAR --- */
    .big-logo-container {
        display: flex;
        gap: 12px;
        margin-bottom: 25px;
    }
    
    .big-logo-box {
        flex: 1;
        background: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed #10B981 !important;
        border-radius: 16px;
        padding: 25px 10px;
        text-align: center;
        color: #34D399 !important;
        font-weight: 800;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.1);
    }
    
    .sidebar-footer-info {
        border-top: 1px solid rgba(16, 185, 129, 0.2);
        padding-top: 20px;
        margin-top: 40px;
        font-size: 0.85rem;
        line-height: 1.5;
        color: #A7F3D0 !important;
    }

    /* --- CARTES ET COMPOSANTS INTERNES --- */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: #10B981;
        background: rgba(16, 185, 129, 0.04);
        transform: translateY(-2px);
    }
    
    .badge-premium { background: linear-gradient(90deg, #F59E0B, #D97706); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; }
    .badge-free { background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CONFIGURATION ET INITIALISATION DES BASES DE DONNÉES IN-MEMORY
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

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"id": 1, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Thermodynamique et Transfert Thermique", "Enseignant": "Dr. Eko", "Type": "Examen", "Année": "2024-2025", "Premium": False, "Downloads": 145, "Date": "12/03/2026", "Favori": False},
        {"id": 2, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Mécanique des Fluides Appliquée + CORRIGÉ", "Enseignant": "Pr. Ndongo", "Type": "Examen", "Année": "2024-2025", "Premium": True, "Downloads": 92, "Date": "18/03/2026", "Favori": False},
        {"id": 3, "Cycle": "Licence Sciences de l'Ingénieur", "Filière": "Sciences du Bois", "Niveau": "L3", "Matière": "Rhéologie et Anatomie du Bois", "Enseignant": "Dr. Bella", "Type": "CC", "Année": "2023-2024", "Premium": False, "Downloads": 54, "Date": "02/02/2026", "Favori": False}
    ])
    st.session_state.is_premium_user = False
    
    st.session_state.interactions = {
        "commentaires": ["Excellente lisibilité sur les sujets de Génie Énergétique.", "Sujet de Thermo Ing4 disponible !"],
        "suggestions": ["Ajouter les TP de chimie des solutions pour les L1."],
        "avis": [{"user": "Anonyme", "note": 5, "text": "L'interface à 300F vaut largement le coup !"}],
        "remerciements": ["Merci à Caleb Bertrand pour cette initiative de génie sur le campus."]
    }

# ==============================================================================
# 3. INTERFACE DE LA BARRE LATÉRALE IMMUNE AUX SELECTION DE THÈMES SMARTPHONE
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div class="big-logo-container">
            <div class="big-logo-box">🏛️<br>ISABEE LOGO</div>
            <div class="big-logo-box">🎓<br>U-BERTOUA</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔑 ACCÈS COMPTE")
    
    user_matricule = st.text_input("Identifiant Matricule Étudiant :", value="22I0000B", placeholder="Ex: 22I0123B")
    if not user_matricule.endswith('B') or len(user_matricule) < 8:
        st.warning("Format suggéré : 22IxxxxB")

    if not st.session_state.is_premium_user:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 18px; border-radius: 12px; text-align: center; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
                <h5 style="margin: 0; color: white; font-weight:800;">PASS PREMIUM</h5>
                <div style="font-size: 1.5rem; font-weight: 900; color: white; margin: 5px 0;">300 FCFA <span style="font-size:0.8rem; font-weight:400;">/ sem</span></div>
                <p style="font-size: 0.75rem; color: #E6F4EA; margin:0;">Débloque tous les corrigés types d'ingénieurs</p>
            </div>
        """, unsafe_allow_html=True)
        
        activation_key = st.text_input("Saisir la clé Premium :", type="password")
        if st.button("Activer la clé Premium"):
            if activation_key == "isabee300":
                st.session_state.is_premium_user = True
                st.success("Accès Premium validé ! ✨")
                st.rerun()
    else:
        st.success("👑 Compte Premium Actif (300F)")
        if st.button("Basculer en Mode Gratuit"):
            st.session_state.is_premium_user = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎛️ FILTRES DE SÉLECTION")
    f_cycle = st.selectbox("Cycle d'études", ["Tous", "Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
    f_filiere = st.selectbox("Filière", ["Toutes"] + FILIERES)
    f_type = st.selectbox("Type d'évaluation", ["Tous", "CC", "Examen", "Rattrapage", "TP"])

    st.markdown(f"""
        <div class="sidebar-footer-info">
            <b>👨‍💻 DÉVELOPPEUR EN CHEF :</b><br>
            CHEMTA Caleb Bertrand<br>
            Étudiant Ingénieur en Génie Énergétique<br>
            <br>
            <b>📞 CONTACT COMMERCIAL :</b><br>
            • Téléphone : +237 696 07 56 60<br>
            • Email : bertrandchemtacaleb@gmail.com<br>
            • Campus : ISABEE / U-BERTOUA
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. EN-TÊTE PRINCIPAL : EFFET DE LUMIÈRE INTENSE & BIENVENUE
# ==============================================================================
st.markdown("<h1 class='glow-title'>SOURCE ISABEE</h1>", unsafe_allow_html=True)
st.markdown("<p class='glow-subtitle'>Anciennes épreuves et sujets d'examens et contrôles continus... Développé par Bertrand Caleb.</p>", unsafe_allow_html=True)

st.markdown("""
    <div class="welcome-banner">
        <p class="welcome-text">🌟 BIENVENUE SUR VOTRE PLATEFORME D'EXCELLENCE ACADÉMIQUE ! 🌟</p>
        <p style="margin: 5px 0 0 0; opacity:0.8; font-size:0.95rem; color:#FFFFFF;">Accédez instantanément aux archives de vos filières pour propulser vos résultats.</p>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. MENUS SOUS FORME DE BOUTONS TRÈS MODERNES
# ==============================================================================
tab_premium, tab_upload, tab_fav, tab_control, tab_thanks = st.tabs([
    "📂 ARCHIVES PREMIUM", 
    "🚀 DÉPÔT ÉLITE", 
    "⭐ MES FAVORIS", 
    "👑 PANNEAU DE CONTRÔLE", 
    "🤝 RECONNAISSANCE"
])

df_view = st.session_state.db.copy()
if f_cycle != "Tous": df_view = df_view[df_view['Cycle'] == f_cycle]
if f_filiere != "Toutes": df_view = df_view[df_view['Filière'] == f_filiere]
if f_type != "Tous": df_view = df_view[df_view['Type'] == f_type]

# ------------------------------------------------------------------------------
# ONGLET 1 : ARCHIVES PREMIUM
# ------------------------------------------------------------------------------
with tab_premium:
    st.markdown("### 🔍 Rechercher un document")
    search_bar = st.text_input("Saisir un mot-clé ou nom d'UE :", placeholder="Ex: Termodinamique...")
    
    if search_bar:
        matches = []
        for idx, row in df_view.iterrows():
            sim = difflib.SequenceMatcher(None, search_bar.lower(), row['Matière'].lower()).ratio()
            if search_bar.lower() in row['Matière'].lower() or sim > 0.4:
                matches.append(row)
        df_view = pd.DataFrame(matches) if matches else pd.DataFrame(columns=df_view.columns)

    if df_view.empty:
        st.info("Aucun document ne correspond aux filtres appliqués.")
    else:
        for idx, row in df_view.iterrows():
            badge = "<span class='badge-premium'>💎 PREMIUM (Corrigé)</span>" if row['Premium'] else "<span class='badge-free'>🆓 GRATUIT (Sujet seul)</span>"
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="color:#FFFFFF; margin:0;">{row['Matière']}</h4>
                        {badge}
                    </div>
                    <p style="font-size:0.85rem; opacity:0.8; margin: 5px 0; color:#E5E7EB;">
                        <b>Filière :</b> {row['Filière']} | <b>Niveau :</b> {row['Niveau']} | <b>Session :</b> {row['Année']} | <b>Enseignant :</b> {row['Enseignant']}<br>
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
                        st.session_state.db.loc[st.session_state.db['id'] == row['id'], 'Downloads'] += 1
                        st.success("Téléchargement initié avec succès !")
            with c2:
                if st.button("⭐ Mettre en Favoris", key=f"f_{row['id']}"):
                    st.session_state.db.loc[st.session_state.db['id'] == row['id'], 'Favori'] = True
                    st.toast("Ajouté aux favoris !")

# ------------------------------------------------------------------------------
# ONGLET 2 : DÉPÔT ÉLITE
# ------------------------------------------------------------------------------
with tab_upload:
    st.markdown("### 🚀 Panel de téléversement sécurisé")
    with st.form("upload_form"):
        u_mat = st.text_input("Nom complet de la matière / UE :")
        u_cyc = st.selectbox("Cycle", ["Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
        u_fil = st.selectbox("Filière de destination", FILIERES)
        u_niv = st.selectbox("Niveau exact", ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5", "M1", "M2"])
        u_type = st.selectbox("Type", ["CC", "Examen", "Rattrapage", "TP"])
        u_prof = st.text_input("Enseignant titulaire :")
        u_prem = st.checkbox("Activer la restriction Premium (Verrouillage 300F)")
        u_file = st.file_uploader("Fichier de l'épreuve (PDF ou Image)")
        
        if st.form_submit_button("PUBLIER SUR LA PLATEFORME"):
            if u_mat and u_file:
                new_id = len(st.session_state.db) + 1
                new_row = {"id": new_id, "Cycle": u_cyc, "Filière": u_fil, "Niveau": u_niv, "Matière": u_mat, "Enseignant": u_prof, "Type": u_type, "Année": "2025-2026", "Premium": u_prem, "Downloads": 0, "Date": datetime.today().strftime('%d/%m/%Y'), "Favori": False}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Document intégré au catalogue avec succès !")
            else:
                st.error("Veuillez remplir le nom de l'UE et insérer un document.")

# ------------------------------------------------------------------------------
# ONGLET 3 : MES FAVORIS
# ------------------------------------------------------------------------------
with tab_fav:
    st.markdown("### ⭐ Votre bibliothèque personnalisée de révision")
    df_fav = st.session_state.db[st.session_state.db['Favori'] == True]
    if df_fav.empty:
        st.info("Aucun document enregistré dans vos favoris pour le moment.")
    else:
        for idx, row in df_fav.iterrows():
            st.write(f"• **{row['Matière']}** ({row['Niveau']}) — {row['Type']}")

# ------------------------------------------------------------------------------
# ONGLET 4 : PANNEAU DE CONTRÔLE (POUR TOI ET TON CO-ADMIN)
# ------------------------------------------------------------------------------
with tab_control:
    st.markdown("### 👑 Espace de Modération & Métriques")
    st.write(f"**Identifiant connecté :** {user_matricule}")
    
    st.dataframe(st.session_state.db[['Matière', 'Niveau', 'Downloads', 'Premium']], use_container_width=True)
    
    st.markdown("#### Suppression d'archives obsolètes")
    for idx, row in st.session_state.db.iterrows():
        col_name, col_btn = st.columns([4, 1])
        col_name.write(f"🗑️ {row['Matière']} ({row['Niveau']})")
        if col_btn.button("Retirer", key=f"del_{row['id']}"):
            st.session_state.db = st.session_state.db[st.session_state.db['id'] != row['id']]
            st.rerun()

# ------------------------------------------------------------------------------
# ONGLET 5 : RECONNAISSANCE & TOUCHES SPÉCIALES INTERACTIVES
# ------------------------------------------------------------------------------
with tab_thanks:
    st.markdown("### 🤝 Communauté, Retours d'expérience et Remerciements")
    
    t_comm, t_sug, t_av, t_rem = st.tabs(["💬 Commentaires", "💡 Suggestions", "⭐ Avis", "🙏 Remerciements"])
    
    with t_comm:
        st.write("#### Zone de libre échange sur les épreuves")
        for c in st.session_state.interactions["commentaires"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:8px;'>💬 {c}</div>", unsafe_allow_html=True)
        new_c = st.text_input("Ajouter un commentaire de session :", key="in_c")
        if st.button("Poster le commentaire", key="b_c") and new_c:
            st.session_state.interactions["commentaires"].append(new_c)
            st.rerun()
            
    with t_sug:
        st.write("#### Proposer des fonctionnalités ou des dossiers manquants")
        for s in st.session_state.interactions["suggestions"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:8px;'>💡 {s}</div>", unsafe_allow_html=True)
        new_s = st.text_input("Quelle est votre suggestion ?", key="in_s")
        if st.button("Soumettre la suggestion", key="b_s") and new_s:
            st.session_state.interactions["suggestions"].append(new_s)
            st.rerun()
            
    with t_av:
        st.write("#### Votre note sur l'expérience globale de l'application")
        for a in st.session_state.interactions["avis"]:
            st.markdown(f"**{a['user']}** : {'★'*a['note']} <br>_{a['text']}_", unsafe_allow_html=True)
        new_note = st.slider("Attribuer une note de performance :", 1, 5, 5)
        new_txt = st.text_input("Votre avis général :", key="in_a")
        if st.button("Envoyer l'évaluation", key="b_a") and new_txt:
            st.session_state.interactions["avis"].append({"user": user_matricule, "note": new_note, "text": new_txt})
            st.rerun()
            
    with t_rem:
        st.write("#### Remerciements aux contributeurs de la base de données")
        for r in st.session_state.interactions["remerciements"]:
            st.markdown(f"<div style='padding:10px; border-left: 3px solid #10B981; background:rgba(16,185,129,0.05); margin-bottom:8px; color:#FFFFFF;'>🙏 {r}</div>", unsafe_allow_html=True)
        new_r = st.text_input("Laisser un mot de gratitude :", key="in_r")
        if st.button("Envoyer le mot", key="b_r") and new_r:
            st.session_state.interactions["remerciements"].append(new_r)
            st.rerun()
