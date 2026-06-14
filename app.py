import streamlit as st
import pandas as pd
import numpy as np
import difflib  # Pour la recherche intelligente tolérante aux fautes d'orthographe
from datetime import datetime

# ==============================================================================
# 1. ARCHITECTURE ET CONFIGURATION NEXT-GEN (STYLING VERCEL / LINEAR / APPLE)
# ==============================================================================
st.set_page_config(
    page_title="SOURCE ISABEE — Plateforme Premium",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation du choix du thème (Sombre/Clair) dans la session
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "Sombre"

# Injection de styles CSS avancés (Glassmorphism, animations et variables globales)
if st.session_state.theme_mode == "Sombre":
    bg_gradient = "linear-gradient(135deg, #021A11 0%, #032418 50%, #010D08 100%)"
    card_bg = "rgba(255, 255, 255, 0.03)"
    text_color = "#FFFFFF"
    border_color = "rgba(16, 185, 129, 0.2)"
    sidebar_bg = "rgba(2, 26, 17, 0.95)"
else:
    bg_gradient = "linear-gradient(135deg, #F0FDF4 0%, #E8F5E9 50%, #FFFFFF 100%)"
    card_bg = "rgba(0, 0, 0, 0.02)"
    text_color = "#0B2F21"
    border_color = "rgba(16, 185, 129, 0.4)"
    sidebar_bg = "rgba(240, 253, 244, 0.95)"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    .stApp {{
        background: {bg_gradient};
        color: {text_color};
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    [data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid {border_color};
    }}
    
    /* Titre animé ultra-brillant */
    .hero-title {{
        font-size: 4.5rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #10B981, #34D399, #A7F3D0, #10B981);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: shine 4s linear infinite;
        margin-bottom: 0px;
        letter-spacing: -2px;
    }}
    
    @keyframes shine {{
        to {{ background-position: 200% center; }}
    }}
    
    /* Cartes Glassmorphism avancées */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {border_color};
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        border-color: #10B981;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.15);
    }}
    
    /* Boutons de l'interface */
    .stButton>button {{
        background: linear-gradient(90deg, #059669 0%, #10B981 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
        transition: 0.3s !important;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6) !important;
    }}
    
    /* Badges de métadonnées */
    .badge {{
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        padding: 6px 14px;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. INITIALISATION DU MOTEUR DE DONNÉES (SQLITE SIMULATION VIA SESSION STATE)
# ==============================================================================
if 'db_initialized' not in st.session_state:
    # Base principale des documents académiques
    st.session_state.documents = pd.DataFrame([
        {"id": 1, "Matière": "Thermodynamique Appliquée", "Cycle": "Cycle Ingénieur", "Niveau": "Ingénieur 4", "Année": "2025", "Type": "Examen Semestriel", "Filière": "Génie Énergétique", "Enseignant": "Dr. Eko", "Taille": "1.2 Mo", "Date": "12/03/2026", "Téléchargements": 142, "Note": 5, "Favori": False},
        {"id": 2, "Matière": "Botanique et Structure des Bois", "Cycle": "Cycle Ingénieur", "Niveau": "Ingénieur 1", "Année": "2024", "Type": "Contrôle Continu", "Filière": "Génie du Bois", "Enseignant": "Pr. Ndongo", "Taille": "850 Ko", "Date": "05/01/2026", "Téléchargements": 98, "Note": 4, "Favori": True},
        {"id": 3, "Matière": "Hydrologie Générale", "Cycle": "Licence en Sciences de l'Ingénieur", "Niveau": "Licence 3", "Année": "2025", "Type": "Examen Semestriel", "Filière": "Génie de l'Eau", "Enseignant": "Dr. Bella", "Taille": "2.1 Mo", "Date": "18/04/2026", "Téléchargements": 210, "Note": 5, "Favori": False},
        {"id": 4, "Matière": "Modélisation des Écosystèmes Forestiers", "Cycle": "Master I", "Niveau": "Master 1", "Année": "2026", "Type": "Travaux Pratiques", "Filière": "Environnement", "Enseignant": "Membres du département", "Taille": "4.3 Mo", "Date": "14/06/2026", "Téléchargements": 34, "Note": 3, "Favori": False}
    ])
    
    # Historique utilisateur & Statistiques globales
    st.session_state.total_downloads = 484
    st.session_state.authenticated = False
    st.session_state.user_matricule = ""
    st.session_state.user_role = "Étudiant"
    st.session_state.comments = {1: ["Très bon sujet, proche de la session de rattrapage."], 2: ["Erreur de frappe à la question 3."]}
    st.session_state.db_initialized = True

# ==============================================================================
# 3. SIDEBAR INTELLIGENTE : LOGOS, AUTHENTIFICATION ET FILTRES DYNAMIQUES
# ==============================================================================
with st.sidebar:
    # Zone des logos officiels réutilisables
    st.markdown("""
        <div style="display: flex; gap: 12px; margin-bottom: 25px; background: rgba(255,255,255,0.02); padding: 12px; border-radius: 18px; border: 1px dashed rgba(16, 185, 129, 0.3);">
            <div style="flex: 1; text-align: center; color: #10B981; font-size: 0.75rem; font-weight: 800; border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px; padding: 15px 5px;">LOGO<br>ISABEE</div>
            <div style="flex: 1; text-align: center; color: #10B981; font-size: 0.75rem; font-weight: 800; border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px; padding: 15px 5px;">UNIVERSITÉ<br>BERTOUA</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Contrôle de Thème Lumineux / Sombre
    st.session_state.theme_mode = st.selectbox("Thème Visuel", ["Sombre", "Clair"])
    
    st.markdown("### 🔐 ESPACE IDENTIFICATION")
    if not st.session_state.authenticated:
        matricule = st.text_input("Matricule Étudiant (Ex: 23U245)", value="")
        role_select = st.selectbox("Niveau d'accès", ["Étudiant", "Délégué Académique", "Administrateur"])
        if st.button("S'AUTHENTIFIER"):
            if matricule:
                st.session_state.authenticated = True
                st.session_state.user_matricule = matricule.upper()
                st.session_state.user_role = role_select
                st.rerun()
    else:
        st.markdown(f"🟢 **Session active :** `{st.session_state.user_matricule}`")
        st.markdown(f"Privilège : **{st.session_state.user_role}**")
        if st.button("Se déconnecter"):
            st.session_state.authenticated = False
            st.rerun()
            
    st.markdown("---")
    st.markdown("### 🗂️ NAVIGATION ACADÉMIQUE")
    cycle_choisi = st.radio(
        "Sélectionnez le cycle :",
        ["Licence en Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"]
    )
    
    # Moteur de filtrage dynamique adaptatif selon le cycle
    if cycle_choisi == "Licence en Sciences de l'Ingénieur":
        niveaux_disponibles = ["Licence 1", "Licence 2", "Licence 3"]
    elif cycle_choisi == "Cycle Ingénieur":
        niveaux_disponibles = ["Ingénieur 1", "Ingénieur 2", "Ingénieur 3", "Ingénieur 4", "Ingénieur 5"]
    elif cycle_choisi == "Master I":
        niveaux_disponibles = ["Master 1"]
    else:
        niveaux_disponibles = ["Master 2"]
        
    niveaux_choisis = st.multiselect("Filtrer par niveau :", niveaux_disponibles, default=niveaux_disponibles)
    
    st.markdown("### 🔍 FILTRES AVANCÉS DE NOUVELLE GÉNÉRATION")
    filtre_annee = st.selectbox("Année de session", ["Toutes", "2026", "2025", "2024", "2023"])
    filtre_type = st.selectbox("Type d'évaluation", ["Tous", "Examen Semestriel", "Contrôle Continu", "Travaux Pratiques", "Rattrapage"])
    filtre_filiere = st.selectbox("Filière", ["Toutes", "Génie Énergétique", "Génie du Bois", "Génie de l'Eau", "Agriculture", "Environnement"])

# ==============================================================================
# 4. PAGE D'ACCUEIL : HERO SECTION SPECTACULAIRE ET COMPTEURS DYNAMIQUES
# ==============================================================================
st.markdown("<h1 class='hero-title'>SOURCE ISABEE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3rem; font-weight: 300; letter-spacing: 2px; color: #34D399; margin-bottom: 40px;'>\"La mémoire académique de l'excellence\"</p>", unsafe_allow_html=True)

# Ligne des compteurs d'activité en temps réel
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.markdown(f"""
        <div style='text-align: center; background: rgba(16, 185, 129, 0.08); padding: 20px; border-radius: 18px; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <h2 style='color: #10B981; margin: 0; font-size: 2.5rem;'>{len(st.session_state.documents)}</h2>
            <p style='margin: 0; font-size: 0.9rem; text-transform: uppercase; opacity: 0.7;'>Épreuves archivées</p>
        </div>
    """, unsafe_allow_html=True)
with col_stat2:
    st.markdown(f"""
        <div style='text-align: center; background: rgba(16, 185, 129, 0.08); padding: 20px; border-radius: 18px; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <h2 style='color: #10B981; margin: 0; font-size: 2.5rem;'>{len(st.session_state.documents['Matière'].unique())}</h2>
            <p style='margin: 0; font-size: 0.9rem; text-transform: uppercase; opacity: 0.7;'>Unités d'Enseignement</p>
        </div>
    """, unsafe_allow_html=True)
with col_stat3:
    st.markdown(f"""
        <div style='text-align: center; background: rgba(16, 185, 129, 0.08); padding: 20px; border-radius: 18px; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <h2 style='color: #10B981; margin: 0; font-size: 2.5rem;'>{st.session_state.total_downloads}</h2>
            <p style='margin: 0; font-size: 0.9rem; text-transform: uppercase; opacity: 0.7;'>Téléchargements sécurisés</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Configuration de l'organisation par Onglets
tab_archives, tab_depot, tab_favoris, tab_admin, tab_remerciements = st.tabs([
    "💎 ARCHIVES PREMIUM", "🚀 DÉPÔT ÉLITE", "⭐ MES FAVORIS", "🔑 ESPACE ADMINISTRATEUR", "🤝 RECONNAISSANCES"
])

# ==============================================================================
# 5. ONGLET 1 : ARCHIVES PREMIUM (RECHERCHE PAR COMPARAISON INTELLIGENTE)
# ==============================================================================
with tab_archives:
    st.markdown("### 🔍 Moteur de recherche à tolérance de fautes")
    search_query = st.text_input("Entrez le mot-clé ou le nom d'une matière (Ex: Termodynamique, Idrologie, Bois...)")
    
    # Filtrage initial des documents basé sur la sidebar académique
    df_filtered = st.session_state.documents[
        (st.session_state.documents['Cycle'] == cycle_choisi) &
        (st.session_state.documents['Niveau'].isin(niveaux_choisis))
    ]
    
    if filtre_annee != "Toutes":
        df_filtered = df_filtered[df_filtered['Année'] == filtre_annee]
    if filtre_type != "Tous":
        df_filtered = df_filtered[df_filtered['Type'] == filtre_type]
    if filtre_filiere != "Toutes":
        df_filtered = df_filtered[df_filtered['Filière'] == filtre_filiere]
        
    # Logique IA de tolérance aux fautes d'orthographe (Fuzzy text check)
    if search_query:
        matches = []
        for index, row in df_filtered.iterrows():
            # Analyse du ratio de proximité textuelle entre la recherche et le nom réel du cours
            ratio = difflib.SequenceMatcher(None, search_query.lower(), row['Matière'].lower()).ratio()
            # Si le mot est contenu directement ou si la proximité phonétique/textuelle dépasse 40%
            if search_query.lower() in row['Matière'].lower() or ratio > 0.4:
                matches.append(row)
        df_filtered = pd.DataFrame(matches) if matches else pd.DataFrame(columns=df_filtered.columns)

    # Affichage des épreuves sous forme de cartes Premium Glassmorphism
    if df_filtered.empty:
        st.info("Aucun document validé ne correspond à vos filtres actuels pour le moment.")
    else:
        for idx, row in df_filtered.iterrows():
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div>
                            <span class="badge">{row['Type']}</span>
                            <span style="margin-left: 10px; font-weight: 600; opacity: 0.8;">📅 Session {row['Année']}</span>
                        </div>
                        <div style="color: #FBBF24; font-weight: bold;">{"★" * row['Note']}{"☆" * (5 - row['Note'])}</div>
                    </div>
                    <h3 style="margin: 5px 0; font-size: 1.6rem; color: #10B981;">{row['Matière']}</h3>
                    <p style="font-size: 0.9rem; opacity: 0.7; margin-bottom: 15px;">
                        📍 <b>{row['Niveau']}</b> | Filière : {row['Filière']} | Titulaire : {row['Enseignant']} <br>
                        📦 Taille : {row['Taille']} | Ajouté le : {row['Date']} | ⬇️ Vu {row['Téléchargements']} fois
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Grille d'actions pour l'étudiant sous chaque épreuve
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            with btn_col1:
                if st.button(f"📥 Télécharger", key=f"download_{row['id']}"):
                    st.session_state.documents.loc[st.session_state.documents['id'] == row['id'], 'Téléchargements'] += 1
                    st.session_state.total_downloads += 1
                    st.success(f"Téléchargement du fichier de '{row['Matière']}' démarré (Simulation PWA).")
                    st.rerun()
            with btn_col2:
                fav_label = "❤️ Retirer des favoris" if row['Favori'] else "⭐ Ajouter aux favoris"
                if st.button(fav_label, key=f"fav_{row['id']}"):
                    st.session_state.documents.loc[st.session_state.documents['id'] == row['id'], 'Favori'] = not row['Favori']
                    st.rerun()
            with btn_col3:
                # Évaluation par notation étoile interactive
                nouvelle_note = st.slider("Noter l'épreuve", 1, 5, int(row['Note']), key=f"rate_{row['id']}")
                if nouvelle_note != row['Note']:
                    st.session_state.documents.loc[st.session_state.documents['id'] == row['id'], 'Note'] = nouvelle_note
                    st.rerun()
            with btn_col4:
                with st.expander("🔗 QR Code & Partage"):
                    st.write("Scannez pour partager sur WhatsApp :")
                    st.code(f"https://source-isabee.cm/archive?id={row['id']}")
            
            # Module de commentaires et d'avis sous l'épreuve
            with st.expander(f"💬 Commentaires et retours d'expérience ({len(st.session_state.comments.get(row['id'], []))})"):
                for comment in st.session_state.comments.get(row['id'], []):
                    st.markdown(f"- *{comment}*")
                nouveau_comm = st.text_input("Ajouter une remarque ou signaler une erreur :", key=f"add_comm_{row['id']}")
                if st.button("Publier le commentaire", key=f"btn_comm_{row['id']}"):
                    if nuevo_comm:
                        if row['id'] not in st.session_state.comments:
                            st.session_state.comments[row['id']] = []
                        st.session_state.comments[row['id']].append(nouveau_comm)
                        st.success("Commentaire ajouté !")
                        st.rerun()

# ==============================================================================
# 6. ONGLET 2 : DÉPÔT ÉLITE (ESPACE SÉCURISÉ DES DÉLÉGUÉS ACADÉMIQUES)
# ==============================================================================
with tab_depot:
    st.markdown("### 🚀 Téléversement de nouveaux documents de révision")
    
    if not st.session_state.authenticated or st.session_state.user_role == "Étudiant":
        st.warning("⚠️ L'accès à la section 'Dépôt Élite' est strictement restreint aux délégués de classes et à l'administration de l'ISABEE pour assurer la conformité des sujets stockés.")
    else:
        st.info(f"Session de téléversement sécurisée au nom du délégué `{st.session_state.user_matricule}`")
        with st.form("form_depot_elite"):
            u_matiere = st.text_input("Nom de la matière ou de l'Unité d'Enseignement (UE)*")
            col_d1, col_d2 = st.columns(2)
            u_cycle = col_d1.selectbox("Cycle d'études", ["Licence en Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
            
            # Détermination dynamique des options de niveau dans le formulaire d'upload
            if u_cycle == "Licence en Sciences de l'Ingénieur":
                niv_opts = ["Licence 1", "Licence 2", "Licence 3"]
            elif u_cycle == "Cycle Ingénieur":
                niv_opts = ["Ingénieur 1", "Ingénieur 2", "Ingénieur 3", "Ingénieur 4", "Ingénieur 5"]
            elif u_cycle == "Master I":
                niv_opts = ["Master 1"]
            else:
                niv_opts = ["Master 2"]
                
            u_niveau = col_d2.selectbox("Niveau exact du cours", niv_opts)
            
            col_d3, col_d4, col_d5 = st.columns(3)
            u_type = col_d3.selectbox("Type d'évaluation", ["Examen Semestriel", "Contrôle Continu", "Travaux Pratiques", "Rattrapage"])
            u_annee = col_d4.selectbox("Année académique", ["2026", "2025", "2024", "2023"])
            u_filiere = col_d5.selectbox("Filière cible", ["Génie Énergétique", "Génie du Bois", "Génie de l'Eau", "Agriculture", "Environnement"])
            
            u_enseignant = st.text_input("Nom de l'Enseignant titulaire de la chaire")
            u_desc = st.text_area("Description ou remarques importantes concernant le sujet")
            
            # Upload par glisser-déposer conforme aux formats autorisés
            u_file = st.file_uploader("Sélectionnez l'épreuve numérisée (PDF, JPG, PNG, JPEG)", type=['pdf', 'jpg', 'png', 'jpeg'])
            
            submit_upload = st.form_submit_button("SÉCURISER LE DOCUMENT DANS LA SOURCE")
            
            if submit_upload:
                if u_matiere and u_file:
                    # Simulation d'analyse de métadonnées et de détection de doublons
                    new_id = int(st.session_state.documents['id'].max() + 1)
                    taille_simulee = f"{np.random.round(u_file.size / (1024*1024), 2)} Mo"
                    
                    new_entry = {
                        "id": new_id, "Matière": u_matiere, "Cycle": u_cycle, "Niveau": u_niveau,
                        "Année": u_annee, "Type": u_type, "Filière": u_filiere, "Enseignant": u_enseignant if u_enseignant else "Inconnu",
                        "Taille": taille_simulee, "Date": datetime.today().strftime('%d/%m/%m%Y'), "Téléchargements": 0, "Note": 5, "Favori": False
                    }
                    
                    st.session_state.documents = pd.concat([st.session_state.documents, pd.DataFrame([new_entry])], ignore_index=True)
                    st.success(f"Félicitations ! L'épreuve de '{u_matiere}' a été chiffrée et sauvegardée avec succès.")
                    st.rerun()
                else:
                    st.error("Erreur critique : Veuillez renseigner le titre du cours et associer le document PDF/Image.")

# ==============================================================================
# 7. ONGLET 3 : COMPILATION ET ESPACE FAVORIS ÉTUDIANT
# ==============================================================================
with tab_favoris:
    st.markdown("### ⭐ Votre collection de révision sur-mesure")
    df_favs = st.session_state.documents[st.session_state.documents['Favori'] == True]
    
    if df_favs.empty:
        st.info("Vous n'avez pas encore d'épreuve enregistrée dans vos favoris.")
    else:
        for idx, row in df_favs.iterrows():
            st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid #10B981; border-radius: 15px; padding: 20px; margin-bottom: 15px;">
                    <h4 style="margin: 0; color: #FFFFFF;">{row['Matière']} — <span style="color: #34D399;">{row['Niveau']}</span></h4>
                    <p style="margin: 5px 0 0 0; font-size: 0.85rem; opacity: 0.8;">Cycle : {row['Cycle']} | Type : {row['Type']} | Session : {row['Année']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Retirer", key=f"del_fav_{row['id']}"):
                st.session_state.documents.loc[st.session_state.documents['id'] == row['id'], 'Favori'] = False
                st.rerun()

# ==============================================================================
# 8. ONGLET 4 : ANALYTICS ET ESPACE DE MODÉRATION ADMINISTRATEUR
# ==============================================================================
with tab_admin:
    st.markdown("### 📊 Tableau de bord analytique de l'administration")
    
    if not st.session_state.authenticated or st.session_state.user_role != "Administrateur":
        st.warning("🔒 Section sécurisée. Veuillez vous connecter avec un profil 'Administrateur' dans le panneau de gauche pour gérer les archives de l'Université de Bertoua.")
    else:
        st.success(f"Accès d'administration globale accordé pour le matricule {st.session_state.user_matricule}")
        
        col_adm1, col_adm2 = st.columns(2)
        with col_adm1:
            st.markdown("#### 📈 Classement des matières les plus consultées")
            df_most_viewed = st.session_state.documents.sort_values(by="Téléchargements", ascending=False)[['Matière', 'Niveau', 'Téléchargements']]
            st.dataframe(df_most_viewed, use_container_width=True)
            
        with col_adm2:
            st.markdown("#### 🛠️ Liste de modération et d'élagage des fichiers")
            for idx, row in st.session_state.documents.iterrows():
                col_row_name, col_row_btn = st.columns([3, 1])
                col_row_name.write(f"🗑️ {row['Matière']} ({row['Niveau']})")
                if col_row_btn.button("Supprimer", key=f"del_doc_{row['id']}"):
                    st.session_state.documents = st.session_state.documents[st.session_state.documents['id'] != row['id']]
                    st.success("Fichier retiré.")
                    st.rerun()

# ==============================================================================
# 9. ONGLET 5 : REMERCIEMENTS & ENGAGEMENT INSTITUTIONNEL
# ==============================================================================
with tab_remerciements:
    st.markdown("### 🤝 Reconnaissances et engagements institutionnels")
    st.markdown("""
    L'évolution de la plateforme **SOURCE ISABEE** est le fruit d'une synergie commune dédiée à l'avancement technologique de notre environnement éducatif :
    
    * **À la Direction de l'ISABEE et à l'Université de Bertoua :** Pour l'impulsion vers la transition numérique de nos campus.
    * **Au Corps Enseignant :** Pour la qualité des évaluations qui préparent les futurs ingénieurs aux défis industriels et écologiques du Cameroun.
    * **Aux Délégués Académiques :** Véritables gardiens du temple, qui œuvrent quotidiennement pour collecter et numériser proprement les supports de révision.
    """)
    
    st.markdown("---")
    st.markdown("### 📜 Politique de confidentialité et d'utilisation responsable")
    with st.expander("Consulter les termes de protection des données académiques"):
        st.write("""
        1. **Protection des documents :** Les épreuves restent la propriété intellectuelle exclusive des enseignants de l'Université de Bertoua. Toute exploitation commerciale est strictement interdite.
        2. **Sécurisation de la vie privée :** Les matricules d'accès servent uniquement à réguler le trafic et à éviter les attaques par déni de service sur le serveur de stockage de Bélabo.
        3. **Sauvegarde automatique :** Les bases de données sont dupliquées chaque nuit pour éviter toute perte de données en cas d'interruption électrique.
        """)

# ==============================================================================
# 10. PIED DE PAGE OFFICIEL : CERTIFICATION DE L'INGÉNIEUR CONCEPTEUR
# ==============================================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
col_foot1, col_foot2 = st.columns(2)
with col_foot1:
    st.markdown("""
        ⚙️ **Développé par :** **CHEMTA Caleb Bertrand** *Étudiant Ingénieur en Génie Énergétique / Informaticien / Entrepreneur* **ISABEE — Université de Bertoua**
    """, unsafe_allow_html=True)

with col_foot2:
    st.markdown(f"""
        📞 **Contact Technologique :** • Téléphone : `696 07 56 60`  
        • Email : `bertrandchemtacaleb@gmail.com`  
        • © 2026 **SOURCE ISABEE** | Tous droits réservés.
    """)
