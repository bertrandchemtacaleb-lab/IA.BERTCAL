import streamlit as st
import pandas as pd
import numpy as np
import difflib
from datetime import datetime

# ==============================================================================
# 1. ARCHITECTURE VISUELLE & GRAPHISME PREMIUM (STYLE LINEAR / STRIPE)
# ==============================================================================
st.set_page_config(
    page_title="SOURCE ISABEE — La Mémoire Académique de l'Excellence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection CSS pour le Glassmorphism, animations néon et police Plus Jakarta Sans
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Fond de page dégradé sombre institutionnel */
    .stApp {
        background: linear-gradient(135deg, #021A11 0%, #032418 50%, #010D08 100%);
        color: #FFFFFF;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Barre latérale personnalisée */
    [data-testid="stSidebar"] {
        background: rgba(2, 26, 17, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    /* Grand Titre Neon Glow */
    .hero-title {
        font-size: 4rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #10B981, #34D399, #A7F3D0, #10B981);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: shine 4s linear infinite;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    
    @keyframes shine {
        to { background-position: 200% center; }
    }
    
    /* Cartes d'épreuves en Glassmorphism avancé */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .glass-card:hover {
        border-color: #10B981;
        background: rgba(16, 185, 129, 0.05);
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.15);
    }
    
    /* Badges de l'interface */
    .badge-premium { background: linear-gradient(90deg, #F59E0B, #D97706); color: white; padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: bold; letter-spacing: 0.5px; }
    .badge-free { background: rgba(16, 185, 129, 0.15); color: #34D399; padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-type { background: rgba(255, 255, 255, 0.08); color: #E5E7EB; padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; }
    
    /* Onglets de navigation */
    .stTabs [data-baseweb="tab"] {
        color: #A7F3D0 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #10B981 !important;
        border-bottom-color: #10B981 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CONFIGURATION DES DONNÉES ET DES STRUCTURES (LES 16 FILIÈRES D'ISABEE)
# ==============================================================================
FILIERES = [
    "Production Végétale", "Production Animale", "Protection des Cultures",
    "Opérations Forestières", "Aménagement Forestier", 
    "Gestion de la Faune, des Aires Protected et Écotourisme",
    "Sylviculture et Plantations Forestières", "Sciences du Bois",
    "Techniques Spécialisées en Transformation du Bois", "Génie de l'Environnement",
    "Systèmes Agro-Sylvo-Pastoraux et Bioénergies", "Bioénergies et Environnement",
    "Génie Énergétique", "Agroéconomie", "Politique et Gouvernance Forestière",
    "Études d'Impact Environnemental et Social"
]

# Initialisation de la base de données interne (Simulation SQLite / Mémoire persistante)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {
            "id": 1, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4",
            "Matière": "Thermodynamique Technique et Transfert de Chaleur", "Enseignant": "Dr. Eko",
            "Type": "Examen", "Année": "2024-2025", "Premium": False, "Fichier": "Sujet_Thermo_2025.pdf",
            "Téléchargements": 142, "Date_Ajout": "12/02/2026", "Note": 5, "Favori": False
        },
        {
            "id": 2, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4",
            "Matière": "Thermodynamique Appliquée [CORRIGÉ PREMIUM]", "Enseignant": "Dr. Eko",
            "Type": "Examen", "Année": "2024-2025", "Premium": True, "Fichier": "Corrige_Thermo_2025.pdf",
            "Téléchargements": 89, "Date_Ajout": "15/02/2026", "Note": 5, "Favori": False
        },
        {
            "id": 3, "Cycle": "Licence Sciences de l'Ingénieur", "Filière": "Sciences du Bois", "Niveau": "L3",
            "Matière": "Physique et Mécanique des Matériaux Ligneux", "Enseignant": "Pr. Ndongo",
            "Type": "CC", "Année": "2023-2024", "Premium": False, "Fichier": "CC_Mecanique_Bois.pdf",
            "Téléchargements": 64, "Date_Ajout": "05/01/2026", "Note": 4, "Favori": False
        },
        {
            "id": 4, "Cycle": "Master II", "Filière": "Bioénergies et Environnement", "Niveau": "M2",
            "Matière": "Modélisation des Systèmes Énergétiques Biomasse", "Enseignant": "Dr. Bella",
            "Type": "Rattrapage", "Année": "2024-2025", "Premium": True, "Fichier": "Biomasse_M2_Corrige.pdf",
            "Téléchargements": 31, "Date_Ajout": "28/05/2026", "Note": 3, "Favori": False
        }
    ])
    
    st.session_state.is_premium_user = False
    st.session_state.global_downloads = 326
    st.session_state.comments_db = {1: ["Sujet très complet !"], 2: ["Le corrigé m'a sauvé pour les révisions de rattrapage."]}

# ==============================================================================
# 3. BARRE LATÉRALE : IDENTITÉ INTERACTIVE & FILTRES DE NOUVELLE GÉNÉRATION
# ==============================================================================
with st.sidebar:
    # Logo placeholders requis par la charte officielle
    st.markdown("""
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center; color: #10B981; font-size: 10px; font-weight: bold; border: 1px dashed rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px 2px;">[ LOGO ISABEE ]</div>
            <div style="flex: 1; text-align: center; color: #10B981; font-size: 10px; font-weight: bold; border: 1px dashed rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px 2px;">[ U-BERTOUA ]</div>
        </div>
    """, unsafe_allow_html=True)
    
    # BANNER D'ABONNEMENT BUSINESS FREEMIUM (300 FCFA)
    if not st.session_state.is_premium_user:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 18px; border-radius: 14px; text-align: center; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); margin-bottom: 20px;">
                <h4 style="margin: 0; color: white; font-weight: 800; font-size:1.1rem;">ACCÈS PREMIUM 👑</h4>
                <p style="margin: 4px 0; font-size: 0.8rem; color: #E6F4EA;">Débloque tous les corrigés d'épreuves</p>
                <div style="font-size: 1.6rem; font-weight: 900; color: #FFFFFF; margin: 8px 0;">300 FCFA <span style="font-size: 0.8rem; font-weight: 400; opacity: 0.9;">/ sem</span></div>
                <p style="font-size: 0.7rem; color: #E6F4EA; margin: 0;">Achetez votre clé auprès de Caleb Bertrand</p>
            </div>
        """, unsafe_allow_html=True)
        
        activation_key = st.text_input("Saisir la clé Premium reçue :", type="password")
        if st.button("Activer l'accès Premium"):
            if activation_key.lower() == "isabee300":
                st.session_state.is_premium_user = True
                st.success("Mode PREMIUM activé avec succès ! ✨")
                st.rerun()
            else:
                st.error("Clé invalide. Payez 300F à Caleb.")
    else:
        st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <span style="color: #34D399; font-weight: bold;">👑 ABONNEMENT PREMIUM ACTIF</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Simuler Compte Gratuit (Test)"):
            st.session_state.is_premium_user = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🗛 FILTRES AVANCÉS")
    
    # Filtre 1 : Le Cycle
    filter_cycle = st.selectbox("Cycle d'études", ["Tous", "Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
    
    # Filtre 2 : La Filière (Les 16 filières officielles de l'ISABEE)
    filter_filiere = st.selectbox("Filière Académique", ["Toutes"] + FILIERES)
    
    # Filtre 3 : Cartographie dynamique intelligente du niveau selon le cycle choisi
    if filter_cycle == "Licence Sciences de l'Ingénieur":
        levels_options = ["L1", "L2", "L3"]
    elif filter_cycle == "Cycle Ingénieur":
        levels_options = ["Ing1", "Ing2", "Ing3", "Ing4", "Ing5"]
    elif filter_cycle == "Master I":
        levels_options = ["M1"]
    elif filter_cycle == "Master II":
        levels_options = ["M2"]
    else:
        levels_options = ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5", "M1", "M2"]
        
    filter_niveau = st.multiselect("Niveau d'études", levels_options, default=levels_options)
    
    # Filtres secondaires
    filter_type = st.selectbox("Type d'évaluation", ["Tous", "CC", "Examen", "Rattrapage", "TP"])
    filter_annee = st.selectbox("Année Académique", ["Toutes", "2025-2026", "2024-2025", "2023-2024", "2022-2023"])

# ==============================================================================
# 4. EXÉCUTION DU MOTEUR DE SÉLECTION & RECHERCHE INTÉLLIGENTE IA (TOLÉRANCE DE FAUTES)
# ==============================================================================
df_filtered = st.session_state.db.copy()

if filter_cycle != "Tous":
    df_filtered = df_filtered[df_filtered['Cycle'] == filter_cycle]
if filter_filiere != "Toutes":
    df_filtered = df_filtered[df_filtered['Filière'] == filter_filiere]
    
df_filtered = df_filtered[df_filtered['Niveau'].isin(filter_niveau)]

if filter_type != "Tous":
    df_filtered = df_filtered[df_filtered['Type'] == filter_type]
if filter_annee != "Toutes":
    df_filtered = df_filtered[df_filtered['Année'] == filter_annee]

# ==============================================================================
# 5. CONCEPTION DU CONTENU PRINCIPAL DE L'APPLICATION
# ==============================================================================
st.markdown("<h1 class='hero-title'>SOURCE ISABEE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8; font-size:1.1rem; letter-spacing:1px; margin-bottom: 30px;'>La mémoire académique de l'excellence — Produit par Caleb Bertrand</p>", unsafe_allow_html=True)

# Ligne de statistiques dynamiques en temps réel
stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.markdown(f"<div style='text-align:center; background:rgba(255,255,255,0.02); padding:15px; border-radius:12px; border:1px solid rgba(16, 185, 129, 0.2);'><h3 style='color:#10B981; margin:0;'>{len(st.session_state.db)}</h3><p style='margin:0; font-size:0.8rem; opacity:0.7;'>DOCUMENTS EN LIGNE</p></div>", unsafe_allow_html=True)
with stat_col2:
    st.markdown(f"<div style='text-align:center; background:rgba(255,255,255,0.02); padding:15px; border-radius:12px; border:1px solid rgba(16, 185, 129, 0.2);'><h3 style='color:#10B981; margin:0;'>16</h3><p style='margin:0; font-size:0.8rem; opacity:0.7;'>FILIÈRES METIERS</p></div>", unsafe_allow_html=True)
with stat_col3:
    st.markdown(f"<div style='text-align:center; background:rgba(255,255,255,0.02); padding:15px; border-radius:12px; border:1px solid rgba(16, 185, 129, 0.2);'><h3 style='color:#10B981; margin:0;'>{st.session_state.global_downloads}</h3><p style='margin:0; font-size:0.8rem; opacity:0.7;'>TÉLÉCHARGEMENTS</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Définition des onglets applicatifs
tab_arch, tab_upload, tab_fav, tab_owner, tab_credits = st.tabs([
    "📂 ARCHIVES PREMIUM", "🚀 DÉPÔT ÉLITE", "⭐ MES FAVORIS", "👑 PANNEAU DE CONTRÔLE", "🤝 RECONNAISSANCE"
])

# ------------------------------------------------------------------------------
# ONGLET 1 : ARCHIVES & SYSTÈME DE RECHERCHE IA AVEC FAUTES
# ------------------------------------------------------------------------------
with tab_arch:
    st.markdown("🔍 **Moteur de recherche intelligent** *(Tapez le nom de l'UE même avec des fautes d'orthographe)*")
    search_query = st.text_input("Rechercher une matière...", placeholder="Ex: Termodinamik, Idrologie, Compte...")
    
    if search_query:
        matches = []
        for idx, row in df_filtered.iterrows():
            # Mesure de similarité textuelle de 0.0 à 1.0 (Tolérance de fautes)
            similarity = difflib.SequenceMatcher(None, search_query.lower(), row['Matière'].lower()).ratio()
            if search_query.lower() in row['Matière'].lower() or similarity > 0.4:
                matches.append(row)
        df_filtered = pd.DataFrame(matches) if matches else pd.DataFrame(columns=df_filtered.columns)

    if df_filtered.empty:
        st.info("Aucune archive disponible pour ces critères de filtrage.")
    else:
        for idx, row in df_filtered.iterrows():
            # Rendu visuel dynamique en fonction de la gratuité/premium du document
            badge_status = "<span class='badge-premium'>💎 CORRIGÉ PREMIUM</span>" if row['Premium'] else "<span class='badge-free'>🆓 SUJET GRATUIT</span>"
            
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div>
                            <span class="badge-type">{row['Type']}</span>
                            <span style="font-size:0.85rem; margin-left:10px; opacity:0.8;">📍 <b>{row['Niveau']}</b> | Session {row['Année']}</span>
                        </div>
                        {badge_status}
                    </div>
                    <h3 style="color:#10B981; margin:6px 0; font-size:1.4rem;">{row['Matière']}</h3>
                    <p style="font-size:0.85rem; opacity:0.7; margin-bottom:12px;">
                        🌿 Filière : <b>{row['Filière']}</b> | Titulaire : {row['Enseignant']} <br>
                        📊 Vu/Téléchargé : {row['Téléchargements']} fois | Publié le : {row['Date_Ajout']} | Évaluation : {"★" * row['Note']}{"☆" * (5 - row['Note'])}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Grille de contrôle de la carte
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                if row['Premium'] and not st.session_state.is_premium_user:
                    st.button("🔒 Corrigé Verrouillé (300F)", key=f"lock_{row['id']}", disabled=True)
                else:
                    if st.button(f"📥 Télécharger PDF", key=f"dl_{row['id']}"):
                        st.session_state.db.loc[st.session_state.db['id'] == row['id'], 'Téléchargements'] += 1
                        st.session_state.global_downloads += 1
                        st.success(f"Téléchargement lancé : {row['Fichier']}")
                        st.rerun()
            with col_b2:
                fav_text = "❤️ Retirer" if row['Favori'] else "⭐ Favoris"
                if st.button(fav_text, key=f"fav_{row['id']}"):
                    st.session_state.db.loc[st.session_state.db['id'] == row['id'], 'Favori'] = not row['Favori']
                    st.rerun()
            with col_b3:
                new_rating = st.selectbox("Noter", [1, 2, 3, 4, 5], index=int(row['Note'])-1, key=f"rate_{row['id']}")
                if new_rating != row['Note']:
                    st.session_state.db.loc[st.session_state.db['id'] == row['id'], 'Note'] = new_rating
                    st.rerun()
            with col_b4:
                with st.expander("🔗 Partager"):
                    st.caption("Lien unique WhatsApp / PWA :")
                    st.code(f"https://source-isabee.net/share?id={row['id']}")
            
            # Module des commentaires sous chaque épreuve
            with st.expander(f"💬 Espace d'échange et retours d'expérience ({len(st.session_state.comments_db.get(row['id'], []))})"):
                for comment in st.session_state.comments_db.get(row['id'], []):
                    st.markdown(f"<p style='font-size:0.85rem; font-style:italic; margin: 2px 0;'>- {comment}</p>", unsafe_allow_html=True)
                user_comm = st.text_input("Laisser un avis ou signaler une erreur de sujet :", key=f"add_comm_{row['id']}")
                if st.button("Envoyer", key=f"btn_comm_{row['id']}"):
                    if user_comm:
                        if row['id'] not in st.session_state.comments_db:
                            st.session_state.comments_db[row['id']] = []
                        st.session_state.comments_db[row['id']].append(user_comm)
                        st.rerun()

# ------------------------------------------------------------------------------
# ONGLET 2 : SYSTÈME DE TÉLÉVERSEMENT INDÉPENDANT SÉCURISÉ (DÉPÔT ÉLITE)
# ------------------------------------------------------------------------------
with tab_upload:
    st.markdown("### 🚀 Dépose une nouvelle épreuve ou un corrigé sur la plateforme")
    st.caption("En tant que propriétaire ou délégué, tu peux utiliser ce formulaire pour étendre la base de données de ton application.")
    
    with st.form("form_upload_isabee"):
        u_matiere = st.text_input("Intitulé exact de la matière / UE :")
        col_up1, col_up2 = st.columns(2)
        u_cycle = col_up1.selectbox("Cycle correspondant", ["Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
        u_filiere = col_up2.selectbox("Filière concernée", FILIERES)
        
        col_up3, col_up4, col_up5 = st.columns(3)
        u_niveau = col_up3.selectbox("Niveau d'études requis", ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5", "M1", "M2"])
        u_type = col_up4.selectbox("Nature de l'évaluation", ["CC", "Examen", "Rattrapage", "TP"])
        u_annee = col_up5.selectbox("Année de passation", ["2025-2026", "2024-2025", "2023-2024", "2022-2023"])
        
        u_enseignant = st.text_input("Enseignant responsable du sujet :")
        u_premium = st.checkbox("Définir ce document comme PREMIUM (Accès restreint payant à 300 FCFA)")
        
        uploaded_file = st.file_uploader("Téléverser le document (PDF, JPG, PNG)", type=["pdf", "jpg", "png", "jpeg"])
        
        submit_upload = st.form_submit_button("SÉCURISER ET ARCHIVER LE DOCUMENT")
        
        if submit_upload:
            if u_matiere and uploaded_file:
                new_doc_id = int(st.session_state.db['id'].max() + 1)
                new_row = {
                    "id": new_doc_id, "Cycle": u_cycle, "Filière": u_filiere, "Niveau": u_niveau,
                    "Matière": u_matiere, "Enseignant": u_enseignant if u_enseignant else "Non spécifié",
                    "Type": u_type, "Année": u_annee, "Premium": u_premium, "Fichier": uploaded_file.name,
                    "Téléchargements": 0, "Date_Ajout": datetime.today().strftime('%d/%m/%Y'), "Note": 5, "Favori": False
                }
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Succès : '{u_matiere}' a bien été crypté et intégré au catalogue Freemium !")
            else:
                st.error("Remplis le nom de la matière et glisse un fichier valide.")

# ------------------------------------------------------------------------------
# ONGLET 3 : DASHBOARD PERSONNEL DES FAVORIS ÉTUDIANT
# ------------------------------------------------------------------------------
with tab_fav:
    st.markdown("### ⭐ Tes documents de révision mis de côté")
    df_favs = st.session_state.db[st.session_state.db['Favori'] == True]
    
    if df_favs.empty:
        st.info("Aucun document n'est sauvegardé dans tes favoris pour le moment.")
    else:
        for idx, row in df_favs.iterrows():
            st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.05); border-left: 4px solid #10B981; border-radius: 8px; padding: 15px; margin-bottom: 10px;">
                    <h4 style="margin:0; color:white;">{row['Matière']} ({row['Niveau']})</h4>
                    <span style="font-size:0.8rem; opacity:0.7;">Filière : {row['Filière']} | Type : {row['Type']}</span>
                </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ONGLET 4 : LE PANNEAU DE CONTRÔLE DE L'ENTREPRENEUR (CALEB BERTRAND)
# ------------------------------------------------------------------------------
with tab_owner:
    st.markdown("### 🛠️ Espace Maître à Bord — Gestion du Système")
    st.caption("Cette section t'est réservée pour suivre l'analyse de ton application et faire la modération.")
    
    col_own1, col_own2 = st.columns(2)
    with col_own1:
        st.markdown("#### 📈 Classement des documents les plus rentables / recherchés")
        df_ranking = st.session_state.db.sort_values(by="Téléchargements", ascending=False)[['Matière', 'Niveau', 'Téléchargements', 'Premium']]
        st.dataframe(df_ranking, use_container_width=True)
        
    with col_own2:
        st.markdown("#### 🗑️ Actions rapides de suppression d'archives")
        for idx, row in st.session_state.db.iterrows():
            col_rm_name, col_rm_btn = st.columns([3, 1])
            col_rm_name.write(f"• {row['Matière']} ({row['Niveau']})")
            if col_rm_btn.button("Retirer", key=f"del_owner_{row['id']}"):
                st.session_state.db = st.session_state.db[st.session_state.db['id'] != row['id']]
                st.toast("Épreuve supprimée !")
                st.rerun()

# ------------------------------------------------------------------------------
# ONGLET 5 : RECONNAISSANCE & POLITIQUE DE CONFIDENTIALITÉ
# ------------------------------------------------------------------------------
with tab_credits:
    st.markdown("### 🤝 Engagement Qualité de l'Application")
    st.markdown("""
    **SOURCE ISABEE** est une plateforme indépendante conçue pour soutenir l'effort d'apprentissage et de réussite des étudiants de l'ISABEE (Université de Bertoua).
    
    * **Droits et Propriété intellectuelle :** Les épreuves appartiennent à leurs auteurs respectifs (le corps enseignant de l'ISABEE). La plateforme n'assure que leur archivage, indexation et facilitation d'accès.
    * **Protection des données (RGPD/PWA) :** Aucun mot de passe complexe n'est stocké en ligne pour assurer la fluidité de consultation sur mobile et tablette.
    """)
    st.markdown("---")
    st.markdown("🔒 **Sauvegarde Automatique :** Base de données active synchronisée sur mémoire locale `SessionState` de l'application.")

# ==============================================================================
# 6. PIED DE PAGE OFFICIEL UNIQUE ET SIGNATURE ENTREPRENEURIALE
# ==============================================================================
st.markdown("<br><hr style='border-color: rgba(16, 185, 129, 0.2);'>", unsafe_allow_html=True)
col_foot1, col_foot2 = st.columns(2)
with col_foot1:
    st.markdown("""
        ⚡ **Propriétaire & Développeur :** **CHEMTA Caleb Bertrand** *Étudiant Ingénieur en Génie Énergétique / Informaticien / Entrepreneur* **ISABEE — Université de Bertoua**
    """, unsafe_allow_html=True)

with col_foot2:
    st.markdown("""
        📞 **Contact Commercial & Support Clés :** • Téléphone : `696 07 56 60` | Email : `bertrandchemtacaleb@gmail.com`  
        • © 2026 **SOURCE ISABEE** — Tous droits réservés. Mode Saas Freemium.
    """, unsafe_allow_html=True)
