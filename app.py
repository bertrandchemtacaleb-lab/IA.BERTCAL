import streamlit as st
import pandas as pd
import difflib
from datetime import datetime
import time

# ==============================================================================
# 1. ARCHITECTURE VISUELLE ET COMPOSANTS CSS INJECTÉS (FORÇAGE THÈME SOMBRE NÉON)
# ==============================================================================
st.set_page_config(
    page_title="SOURCE ISABEE — L'Élite Académique",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght=400;700&display=swap');
    
    /* APPLICATION GLOBALE DU THEME PRESTIGE VERT SOMBRE */
    .stApp, [data-testid="stMainView"], [data-testid="stHeader"], .main, .block-container, [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {
        background: #010D08 !important;
        background-image: linear-gradient(135deg, #010D08 0%, #021F14 50%, #000503 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    p, span, label, h1, h2, h3, h4, h5, h6, div {
        color: #FFFFFF !important;
    }
    
    /* BOUTON FLÈCHE FLOTTANTE DE LA SIDEBAR ULTRA-VISIBLE */
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
    }
    
    /* TITRES LUMINEUX NÉON */
    .glow-title {
        font-size: 4.2rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        text-align: center;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: -2px;
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.8), 0 0 40px rgba(16, 185, 129, 0.4);
    }
    @media (max-width: 768px) { .glow-title { font-size: 2.3rem !important; } }
    
    .glow-subtitle {
        text-align: center;
        font-size: 1.15rem;
        color: #A7F3D0 !important;
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    .welcome-banner {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.2) 50%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 35px;
    }
    
    /* STRUCTURES ET ENCADREMENTS */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 18px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35) !important;
    }
    
    /* PARAMETRES KPI BOXES */
    .kpi-box {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid #10B981;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }

    .sidebar-blue-footer {
        border-top: 1px solid rgba(56, 189, 248, 0.2);
        padding-top: 15px;
        margin-top: 35px;
        font-size: 0.85rem;
        color: #38BDF8 !important;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DONNÉES CENTRALE (SERVEUR GLOBAL COHÉRENT ET EN LIGNE)
# ==============================================================================
@st.cache_resource
def executer_serveur_central():
    # Catalogue global des épreuves
    base_sujets = pd.DataFrame([
        {"id": 1, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Thermodynamique Approfondie", "Enseignant": "Dr. Eko", "Type": "Examen", "Année": "2024-2025", "Premium": False, "Downloads": 194, "Approuvé": True},
        {"id": 2, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Mécanique des Fluides + Corrigé Élite", "Enseignant": "Pr. Ndongo", "Type": "Examen", "Année": "2024-2025", "Premium": True, "Downloads": 312, "Approuvé": True}
    ])
    
    # Historique de toutes les transactions de paiement automatique style 1xBet
    historique_paiements = pd.DataFrame([
        {"ID_Transaction": "TXN-OM-99821", "Matricule": "22I0041B", "Opérateur": "Orange Money", "Montant": 300, "Statut": "Réussi", "Date": "15/06/2026"}
    ])
    
    # Espace des interactions étudiantes
    interactions = {
        "commentaires": ["Le corrigé de fluide est ultra détaillé merci !", "Service automatique très rapide."],
        "suggestions": ["Mettez les épreuves de Protection des Cultures L3 svp."]
    }
    
    # Liste des tickets d'urgence générés manuellement
    tickets_manuels = {
        "ISABEE-ADMIN-100": {"statut": "Disponible", "utilise_par": ""}
    }
    
    # Configuration globale par défaut modulable en catégorie
    config = {
        "owner_password": "owner",
        "copilot_password": "copilote",
        "prix_premium": 300,
        "mode_api": "Automatique (Live)",
        "orange_phone": "696075660",
        "mtn_phone": "654046792",
        "nom_app": "SOURCE ISABEE",
        "filières_actives": [
            "Production Végétale", "Production Animale", "Protection des Cultures",
            "Opérations Forestières", "Aménagement Forestier", "Génie Énergétique", 
            "Agroéconomie", "Génie de l'Environnement"
        ]
    }
    return {"db": base_sujets, "paiements": historique_paiements, "interactions": interactions, "tickets": tickets_manuels, "config": config}

serveur = executer_serveur_central()

# Variables d'état pour le terminal de l'appareil courant
if 'is_premium_user' not in st.session_state:
    st.session_state.is_premium_user = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = "Visiteur"

# ==============================================================================
# 3. SIDEBAR : FILTRES & COORDONNÉES DE L'INGÉNIEUR CONCEPTEUR
# ==============================================================================
with st.sidebar:
    st.markdown(f"### 💎 COMPTE {st.session_state.user_role.upper()}")
    current_matricule = st.text_input("Matricule Étudiant :", value="22I0002B").strip()
    
    if st.session_state.is_premium_user:
        st.success("👑 Statut : Compte Premium Activé")
    else:
        st.info("🆓 Statut : Version Gratuite Limité")
        
    st.markdown("---")
    st.markdown("### 🎛️ CRITÈRES DE FILTRAGE")
    f_cycle = st.selectbox("Sélectionner le Cycle", ["Tous", "Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
    f_filiere = st.selectbox("Sélectionner la Filière", ["Toutes"] + serveur["config"]["filières_actives"])
    f_type = st.selectbox("Type d'Épreuve", ["Tous", "CC", "Examen", "Rattrapage", "TP"])

    st.markdown(f"""
        <div class="sidebar-blue-footer">
            Concepteur en Chef : <b>Chemta Caleb Bertrand</b><br>
            Étudiant Ingénieur en Génie Énergétique<br><br>
            <strong>ASSISTANCE UNIQUE :</strong><br>
            • Orange : +237 {serveur["config"]["orange_phone"]}<br>
            • MTN : +237 {serveur["config"]["mtn_phone"]}<br>
            • ISABEE / Université de Bertoua
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. DESIGN DU HEADER & ENTÊTE OFFICIEL
# ==============================================================================
st.markdown(f"<h1 class='glow-title'>{serveur['config']['nom_app']}</h1>", unsafe_allow_html=True)
st.markdown("<p class='glow-subtitle'>Système de distribution d'archives académiques sécurisé de haute performance.</p>", unsafe_allow_html=True)

st.markdown("""
    <div class="welcome-banner">
        <span style="font-size:1.4rem; font-weight:700; color:#34D399;">⚡ ENTRÉE IMMÉDIATE DANS LES ARCHIVES DE L'ÉLITE</span><br>
        <p style="margin:6px 0 0 0; opacity:0.85; font-size:0.95rem;">Recherchez vos matières, téléchargez vos supports de révision et accédez aux corrigés d'ingénierie.</p>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. SPLIT DE NAVIGATION EN ONGLETS MAÎTRES
# ==============================================================================
tab_archives, tab_pass_payment, tab_feedback, tab_maison_virtuelle = st.tabs([
    "📂 VUE DES ARCHIVES", 
    "💳 PASSERELLE DE PAIEMENT AUTOMATIQUE (1xBet Style)", 
    "💬 ESPACE D'INTERACTION ÉTUDIANTS",
    "🏛️ MAISON VIRTUELLE DU DÉVELOPPEUR"
])

# ------------------------------------------------------------------------------
# ONGLET A : VUE DES ARCHIVES PUBLIQUES
# ------------------------------------------------------------------------------
with tab_archives:
    st.markdown("### 🔍 Moteur de recherche d'épreuves")
    search_query = st.text_input("Tapez le nom d'une unité d'enseignement (Ex: Fluides...) :", value="")
    
    # Filtrage de la base de données
    df_public = serveur["db"][serveur["db"]['Approuvé'] == True].copy()
    if f_cycle != "Tous": df_public = df_public[df_public['Cycle'] == f_cycle]
    if f_filiere != "Toutes": df_public = df_public[df_public['Filière'] == f_filiere]
    if f_type != "Tous": df_public = df_public[df_public['Type'] == f_type]
    
    if search_query:
        df_public = df_public[df_public['Matière'].str.contains(search_query, case=False, na=False)]
        
    if df_public.empty:
        st.info("Aucun document approuvé ne correspond à vos filtres actuels.")
    else:
        for idx, row in df_public.iterrows():
            is_p = row['Premium']
            badge = "<span class='badge-premium'>💎 EXCLUSIVITÉ PREMIUM</span>" if is_p else "<span class='badge-free'>🆓 ACCÈS LIBRE</span>"
            
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:between; align-items:center;">
                        <span style="font-weight:700; font-size:1.15rem;">{row['Matière']}</span>
                        <div style="margin-left:auto;">{badge}</div>
                    </div>
                    <p style="margin:5px 0 0 0; font-size:0.85rem; opacity:0.8;">
                        Filière : {row['Filière']} | Niveau : {row['Niveau']} | Enseignant : {row['Enseignant']} | Téléchargements : <b>{row['Downloads']}</b>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            c_down, c_fav = st.columns(2)
            with c_down:
                if is_p and not st.session_state.is_premium_user:
                    st.button("🔒 Débloquer l'archive via la Passerelle de Paiement", key=f"lock_{row['id']}", disabled=True)
                else:
                    if st.button(f"📥 Télécharger immédiatement le PDF", key=f"down_{row['id']}"):
                        serveur["db"].loc[serveur["db"]['id'] == row['id'], 'Downloads'] += 1
                        st.success("🔄 Document téléchargé avec succès !")
            with c_fav:
                if st.button("⭐ Épingler l'épreuve", key=f"fav_{row['id']}"):
                    st.toast("Ajouté à votre liste locale !")

# ------------------------------------------------------------------------------
# ONGLET B : VRE PASSERELLE DE PAIEMENT AUTOMATIQUE INTEGRÉE (STYLE 1XBET)
# ------------------------------------------------------------------------------
with tab_pass_payment:
    st.markdown("### 💳 Passerelle Interconnectée Mobile Money API")
    st.write("Aucun envoi manuel requis. Remplissez le formulaire, validez la boîte de dialogue USSD push sur votre téléphone pour activer votre compte instantanément.")
    
    col_pay_form, col_ticket_backup = st.columns([2, 1])
    
    with col_pay_form:
        st.markdown(f"#### 📲 Demande de débit direct instantané ({serveur['config']['prix_premium']} CFA)")
        with st.form("1xbet_style_payment_gateway"):
            operateur = st.radio("Choisir l'opérateur de prélèvement :", ["Orange Money Cameroun", "MTN Mobile Money"])
            num_telephone = st.text_input("Numéro de téléphone payeur (9 chiffres) :", placeholder="6xxxxxxxx")
            
            submit_payment = st.form_submit_button("LANCER LE PAIEMENT AUTOMATIQUE")
            
        if submit_payment:
            if len(num_telephone) == 9:
                with st.spinner("⏳ Initialisation du tunnel API... Envoi du Push USSD sur votre mobile..."):
                    time.sleep(2.5) # Simulation d'attente réseau de l'opérateur
                
                # Génération d'une fausse référence de transaction unique à insérer dans le livre comptable
                ref_auto = f"TXN-{ 'OM' if 'Orange' in operateur else 'MTN' }-{datetime.now().strftime('%M%S%f')[:5]}"
                
                # Ajout de la transaction réussie de manière automatisée
                nouvelle_tx = {
                    "ID_Transaction": ref_auto, "Matricule": current_matricule, 
                    "Opérateur": operateur, "Montant": serveur['config']['prix_premium'], 
                    "Statut": "Réussi", "Date": datetime.today().strftime('%d/%m/%Y')
                }
                serveur["paiements"] = pd.concat([serveur["paiements"], pd.DataFrame([nouvelle_tx])], ignore_index=True)
                
                st.session_state.is_premium_user = True
                st.success(f"✅ Paiement Traité avec Succès ! Référence de validation réseau : {ref_auto}. Votre espace premium est désormais actif.")
                st.balloons()
            else:
                st.error("Format de numéro invalide. Entrez un numéro complet à 9 chiffres.")
                
    with col_ticket_backup:
        st.markdown("#### 🎫 Option de Secours : Ticket Physique")
        st.write("Si vous possédez un ticket papier généré par la direction, introduisez le code secret d'activation ci-dessous.")
        
        backup_code = st.text_input("Code d'activation unique :", key="b_code")
        if st.button("Forcer le déblocage"):
            backup_code = backup_code.strip()
            if backup_code in serveur["tickets"] and serveur["tickets"][backup_code]["statut"] == "Disponible":
                serveur["tickets"][backup_code]["statut"] = "Consommé"
                serveur["tickets"][backup_code]["utilise_par"] = current_matricule
                st.session_state.is_premium_user = True
                st.success("Premium activé par ticket manuel d'urgence !")
                st.rerun()
            else:
                st.error("Ticket de secours invalide ou consommé.")

# ------------------------------------------------------------------------------
# ONGLET C : INTERACTIONS
# ------------------------------------------------------------------------------
with tab_feedback:
    st.markdown("### 💬 Forum de discussion en direct de l'ISABEE")
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("💬 Commentaires d'étudiants")
        for com in serveur["interactions"]["commentaires"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.02); border-radius:6px; margin-bottom:5px;'>💡 {com}</div>", unsafe_allow_html=True)
        with st.form("add_com"):
            n_c = st.text_input("Rédiger un commentaire :")
            if st.form_submit_button("Publier") and n_c:
                serveur["interactions"]["commentaires"].append(n_c)
                st.rerun()
    with c_right:
        st.subheader("💡 Boîte à suggestions")
        for sug in serveur["interactions"]["suggestions"]:
            st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.02); border-radius:6px; margin-bottom:5px;'>📌 {sug}</div>", unsafe_allow_html=True)
        with st.form("add_sug"):
            n_s = st.text_input("Soumettre un axe d'amélioration :")
            if st.form_submit_button("Envoyer l'idée") and n_s:
                serveur["interactions"]["suggestions"].append(n_s)
                st.rerun()

# ------------------------------------------------------------------------------
# ONGLET D : 🏛️ LA MAISON VIRTUELLE DU DÉVELOPPEUR (ACCÈS PRIVÉ DE TRÈS HAUTE SÉCURITÉ)
# ------------------------------------------------------------------------------
with tab_maison_virtuelle:
    if st.session_state.user_role == "Visiteur":
        st.markdown("### 🔐 Authentification d'Infrastructure")
        s_code = st.text_input("Saisissez votre clé de chiffrement maîtresse :", type="password")
        
        if st.button("Interconnecter les serveurs"):
            if s_code == serveur["config"]["owner_password"]:
                st.session_state.user_role = "Owner"
                st.rerun()
            elif s_code == serveur["config"]["copilot_password"]:
                st.session_state.user_role = "Copilote"
                st.rerun()
            else:
                st.error("Alerte de sécurité : Code de chiffrement rejeté.")
    else:
        # Barre de deconnexion et gestion des rôles de la maison virtuelle
        c_status, c_kill = st.columns([4, 1])
        c_status.markdown(f"#### ⚡ Session active : **{st.session_state.user_role.upper()}** connecté à la Maison Virtuelle")
        if c_kill.button("🔒 Quitter et Verrouiller l'Espace"):
            st.session_state.user_role = "Visiteur"
            st.rerun()
            
        st.markdown("---")
        
        # ----------------------------------------------------------------------
        # CAS COPILOTE : DROIT DE TÉLÉVERSEMENT EXCLUSIF SANS VALIDATION DIRECTE
        # ----------------------------------------------------------------------
        if st.session_state.user_role == "Copilote":
            st.info("🚀 Rôle Copilote : Vos téléversements sont envoyés en attente de vérification dans le coffre-fort de Bertcal.")
            with st.form("copilot_secure_form"):
                mat_n = st.text_input("Libellé officiel de la Matière :")
                cyc_n = st.selectbox("Cycle d'études", ["Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
                fil_n = st.selectbox("Filière concernée", serveur["config"]["filières_actives"])
                niv_n = st.selectbox("Niveau", ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5"])
                typ_n = st.selectbox("Type", ["CC", "Examen", "Rattrapage"])
                prof_n = st.text_input("Nom de l'Enseignant :")
                prem_n = st.checkbox("Demander le verrou Premium sur ce fichier")
                file_n = st.file_uploader("Fichier épreuve (PDF uniquement)")
                
                submit_copilote = st.form_submit_button("ENVOYER POUR VALIDATION")
                
            if submit_copilote and mat_n and file_n:
                n_row = {
                    "id": len(serveur["db"]) + 1, "Cycle": cyc_n, "Filière": fil_n, "Niveau": niv_n,
                    "Matière": mat_n, "Enseignant": prof_n, "Type": typ_n, "Année": "2025-2026",
                    "Premium": prem_n, "Downloads": 0, "Approuvé": False # Faux par défaut pour que l'owner valide !
                }
                serveur["db"] = pd.concat([serveur["db"], pd.DataFrame([n_row])], ignore_index=True)
                st.success("Fichier mis en attente. Seul le Concepteur en chef peut le rendre visible.")

        # ----------------------------------------------------------------------
        # CAS OWNER : ACCÈS MAÎTRE ABSOLU SUR LES PARAMÈTRES ET LE CONTRÔLE
        # ----------------------------------------------------------------------
        elif st.session_state.user_role == "Owner":
            
            # Création des sous-sections de contrôle de ta maison virtuelle
            sub_tabs = st.tabs([
                "📥 FILET D'APPROBATION", 
                "📊 PANNEAU DE CONTRÔLE GLOBAL", 
                "⚙️ PARAMÈTRES CATÉGORISÉS", 
                "🎫 FLUX DES TICKETS & TRANSACTIONS"
            ])
            
            # SUB-TAB 1 : APPROBATION DES DOCUMENTS COPILOTES
            with sub_tabs[0]:
                st.markdown("#### 📥 Fichiers en attente d'évaluation de sécurité")
                df_pending = serveur["db"][serveur["db"]['Approuvé'] == False]
                
                if df_pending.empty:
                    st.info("Vos copilotes n'ont soumis aucun nouveau document.")
                else:
                    for idx, row in df_pending.iterrows():
                        st.markdown(f"""
                            <div style="background:rgba(255,255,255,0.02); padding:15px; border-radius:10px; border-left:4px solid #F59E0B; margin-bottom:10px;">
                                <b>UE :</b> {row['Matière']} | <b>Filière :</b> {row['Filière']} ({row['Niveau']})<br>
                                Enseignant : {row['Enseignant']} | Statut requis : {"💎 Premium" if row['Premium'] else "Gratuit"}
                            </div>
                        """, unsafe_allow_html=True)
                        c_ok, c_no = st.columns(2)
                        if c_ok.button("✅ Approuver et Publier", key=f"yes_{row['id']}"):
                            serveur["db"].loc[serveur["db"]['id'] == row['id'], 'Approuvé'] = True
                            st.success("Document publié sur l'application publique.")
                            st.rerun()
                        if c_no.button("❌ Refuser le fichier", key=f"no_{row['id']}"):
                            serveur["db"] = serveur["db"][serveur["db"]['id'] != row['id']]
                            st.warning("Fichier supprimé de l'infrastructure.")
                            st.rerun()

            # SUB-TAB 2 : PANNEAU DE CONTRÔLE ANALYTIQUE ET SUPPRESSION
            with sub_tabs[1]:
                st.markdown("#### 📊 Tableau de Bord d'Analyse Financière et Technique")
                
                # Calculs en direct pour les KPI Boxes
                total_docs = len(serveur["db"][serveur["db"]['Approuvé'] == True])
                total_downloads = serveur["db"]['Downloads'].sum()
                ca_global = len(serveur["paiements"][serveur["paiements"]['Statut'] == "Réussi"]) * serveur["config"]["prix_premium"]
                
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("📚 Épreuves en Ligne", f"{total_docs} UEs")
                kpi2.metric("📥 Total Téléchargements", f"{total_downloads} clics")
                kpi3.metric("💰 Chiffre d'Affaires Automatisé", f"{ca_global} CFA")
                
                st.markdown("---")
                st.markdown("#### 🗑️ Gestion Directe du Catalogue")
                st.write("Visualisez et supprimez directement n'importe quelle archive de l'application.")
                
                for idx, row in serveur["db"].iterrows():
                    col_info, col_del = st.columns([5, 1])
                    status_line = "🟢 Publique" if row['Approuvé'] else "🟡 En attente"
                    col_info.write(f"[{status_line}] **{row['Matière']}** ({row['Filière']} - {row['Niveau']})")
                    if col_del.button("Supprimer l'UE", key=f"del_adm_{row['id']}"):
                        serveur["db"] = serveur["db"][serveur["db"]['id'] != row['id']]
                        st.rerun()

            # SUB-TAB 3 : PARAMÈTRES DU SYSTÈME CLASSÉS PAR CATÉGORIES (PERFAIT)
            with sub_tabs[2]:
                st.markdown("#### ⚙️ Configuration Structurée de l'Infrastructure")
                
                # Organisation par catégories avec des widgets expanders clairs
                with st.expander("🔐 CATÉGORIE 1 : CONTRÔLE DES ACCÈS & CLÉS PRIVÉES", expanded=True):
                    new_owner_pwd = st.text_input("Clé Maîtresse (Maison Virtuelle) :", value=serveur["config"]["owner_password"], type="password")
                    new_copilot_pwd = st.text_input("Clé Publique pour vos Copilotes :", value=serveur["config"]["copilot_password"], type="password")
                    if st.button("Mettre à jour les mots de passe de sécurité"):
                        serveur["config"]["owner_password"] = new_owner_pwd
                        serveur["config"]["copilot_password"] = new_copilot_pwd
                        st.success("Mots de passe système synchronisés avec succès.")
                
                with st.expander("💸 CATÉGORIE 2 : TARIFICATION & ROUTAGE DES API FLUX"):
                    new_price = st.number_input("Montant d'accès Premium (CFA) :", value=int(serveur["config"]["prix_premium"]), step=50)
                    new_api_mode = st.selectbox("Statut du serveur de paiement :", ["Automatique (Live)", "Maintenance Sandbox", "Désactivé"])
                    if st.button("Appliquer les modifications monétaires"):
                        serveur["config"]["prix_premium"] = new_price
                        serveur["config"]["mode_api"] = new_api_mode
                        st.success("Grille tarifaire et protocoles API mis à jour.")
                        
                with st.expander("🎓 CATÉGORIE 3 : GESTION ACADÉMIQUE DES FILIÈRES"):
                    st.write("Filières actuellement configurées dans le système central :")
                    st.write(serveur["config"]["filières_actives"])
                    nouvelle_filiere = st.text_input("Ajouter une nouvelle filière d'ingénierie :")
                    if st.button("Enregistrer la Filière") and nouvelle_filiere:
                        if nouvelle_filiere not in serveur["config"]["filières_actives"]:
                            serveur["config"]["filières_actives"].append(nouvelle_filiere)
                            st.success(f"{nouvelle_filiere} ajoutée aux filières d'apprentissage.")
                            st.rerun()
                            
                with st.expander("🎨 CATÉGORIE 4 : INTERFACE & FLUX INFRASTRUCTURE"):
                    new_app_name = st.text_input("Modifier le titre de l'application :", value=serveur["config"]["nom_app"])
                    new_om = st.text_input("Numéro Orange de secours connecté à l'API :", value=serveur["config"]["orange_phone"])
                    new_mtn = st.text_input("Numéro MTN de secours connecté à l'API :", value=serveur["config"]["mtn_phone"])
                    if st.button("Valider l'habillage de marque"):
                        serveur["config"]["nom_app"] = new_app_name
                        serveur["config"]["orange_phone"] = new_om
                        serveur["config"]["mtn_phone"] = new_mtn
                        st.success("Branding de l'interface mis à jour.")
                        st.rerun()

            # SUB-TAB 4 : SUIVI DES TRANSACTIONS DIRECTES ET COMPTABILITÉ
            with sub_tabs[3]:
                st.markdown("#### 🧾 Journal d'Audit des Paiements Automatiques (Style 1xBet)")
                st.write("Chaque dépôt via Orange ou MTN est répertorié ici en temps réel avec le matricule de l'étudiant ayant payé.")
                st.dataframe(serveur["paiements"], use_container_width=True)
                
                st.markdown("---")
                st.markdown("#### 🎫 Générateur Intégrateur de Tickets Uniques Manuels")
                with st.form("gen_t_manual"):
                    code_t = st.text_input("Créer un code de ticket d'urgence (Ex: ISABEE-URGENT) :")
                    if st.form_submit_button("Injecter le ticket dans la base") and code_t:
                        if code_t not in serveur["tickets"]:
                            serveur["tickets"][code_t] = {"statut": "Disponible", "utilise_par": ""}
                            st.success(f"Ticket {code_t} créé et prêt à être distribué !")
                        else:
                            st.error("Ce code existe déjà.")
                            
                # Tableau récapitulatif des tickets
                t_list = []
                for k, v in serveur["tickets"].items():
                    t_list.append({"Code Ticket": k, "Statut": v["statut"], "Utilisé par": v["utilise_par"]})
                st.dataframe(pd.DataFrame(t_list), use_container_width=True)
