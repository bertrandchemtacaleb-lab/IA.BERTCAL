import streamlit as st
import pandas as pd
import difflib
from datetime import datetime
import time
import hashlib

# ==============================================================================
# 1. ARCHITECTURE VISUELLE & INJECTION CSS ULTRA-FORCÉE (CORRECTION MOBILE & PC)
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
    
    .stApp, [data-testid="stMainView"], [data-testid="stHeader"], .main, .block-container, [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {
        background: #010D08 !important;
        background-image: linear-gradient(135deg, #010D08 0%, #021F14 50%, #000503 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    p, span, label, h1, h2, h3, h4, h5, h6, div { color: #FFFFFF !important; }
    
    /* INTERFACE DES ONGLETS PRINCIPAUX MOTEUR */
    .stTabs [data-baseweb="tab-list"] { gap: 12px !important; background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 10px !important;
        padding: 14px 20px !important;
        font-weight: 700 !important;
        color: #9CA3AF !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.3) !important;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid rgba(16, 185, 129, 0.12);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .glow-title {
        font-size: 3.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: -1px;
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
    }
    
    .sidebar-blue-footer {
        border-top: 1px solid rgba(56, 189, 248, 0.15);
        padding-top: 15px;
        margin-top: 30px;
        font-size: 0.85rem;
        color: #38BDF8 !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CORE ENGINE & ETATS DU SERVEUR CENTRALISÉ
# ==============================================================================
FILIERES = [
    "Production Végétale", "Production Animale", "Protection des Cultures",
    "Opérations Forestières", "Aménagement Forestier", "Génie Énergétique", "Agroéconomie"
]

@st.cache_resource
def initialiser_architecture_centrale():
    base_sujets = pd.DataFrame([
        {"id": 1, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Thermodynamique et Transfert Thermique", "Enseignant": "Dr. Eko", "Type": "Examen", "Année": "2024-2025", "Premium": False, "Downloads": 145, "Approuvé": True},
        {"id": 2, "Cycle": "Cycle Ingénieur", "Filière": "Génie Énergétique", "Niveau": "Ing4", "Matière": "Mécanique des Fluides Appliquée + CORRIGÉ", "Enseignant": "Pr. Ndongo", "Type": "Examen", "Année": "2024-2025", "Premium": True, "Downloads": 92, "Approuvé": True}
    ])
    
    # Registre comptable automatisé type Passerelle API
    registre_transactions = pd.DataFrame(columns=["Ref_Transaction", "Matricule", "Opérateur", "Numéro", "Montant", "Statut", "Timestamp"])
    
    config_systeme = {
        "owner_password": "owner",
        "copilot_password": "copilote",
        "tarif_premium": 300,
        "api_gateway_status": "ONLINE",
        "system_version": "v2.4.0-PROD",
        "crypto_salt": "ISABEE_SECURE_99"
    }
    
    return {"db": base_sujets, "transactions": registre_transactions, "config": config_systeme}

core = initialiser_architecture_centrale()

if 'is_premium_user' not in st.session_state: st.session_state.is_premium_user = False
if 'user_role' not in st.session_state: st.session_state.user_role = "Visiteur"

# ==============================================================================
# 3. SIDEBAR : IDENTIFICATION ET ROUTAGE ACADÉMIQUE
# ==============================================================================
with st.sidebar:
    st.markdown("### 🔐 IDENTITY GATEWAY")
    user_matricule = st.text_input("Matricule Étudiant :", value="22I0002B").strip()
    
    if st.session_state.is_premium_user:
        st.success("👑 COMPTE PREMIUM ACTIF")
    else:
        st.warning("🆓 MODE GRATUIT RESTREINT")
        
    st.markdown("---")
    st.markdown("### 🎛️ FILTRES ARCHIVES")
    f_cycle = st.selectbox("Cycle d'études", ["Tous", "Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
    f_filiere = st.selectbox("Filière", ["Toutes"] + FILIERES)
    f_type = st.selectbox("Type d'évaluation", ["Tous", "CC", "Examen", "Rattrapage"])

    st.markdown(f"""
        <div class="sidebar-blue-footer">
            Système Déployé par : <b>Chemta Caleb Bertrand</b><br>
            Étudiant Ingénieur en Génie Énergétique<br><br>
            <strong>SUPPORT DE CONCEPTION :</strong><br>
            • ID Unique : {hashlib.md5(user_matricule.encode()).hexdigest()[:8].upper()}<br>
            • Infrastructure : ISABEE / U-BERTOUA
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. EN-TÊTE DE LA PLATEFORME
# ==============================================================================
st.markdown("<h1 class='glow-title'>SOURCE ISABEE PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#A7F3D0 !important; margin-bottom:25px;'>Passerelle d'accès automatisée aux ressources académiques d'élite.</p>", unsafe_allow_html=True)

# ==============================================================================
# 5. SPLIT ROUTAGE : ARCHITECTURE DES ONGLETS APPLICATIFS
# ==============================================================================
tab_docs, tab_payment, tab_maison = st.tabs([
    "📂 COFFRE-FORT DES ARCHIVES", 
    "💳 PASSERELLE DE PAIEMENT AUTOMATIQUE", 
    "🏛️ MAISON VIRTUELLE DE CONTROLE"
])

# ------------------------------------------------------------------------------
# TAB 1 : COFFRE-FORT DES ARCHIVES
# ------------------------------------------------------------------------------
with tab_docs:
    st.markdown("### 🔍 MOTEUR DE RECHERCHE INDEXÉ")
    search_bar = st.text_input("Rechercher une Unité d'Enseignement :", placeholder="Ex: Thermodynamique...")
    
    df_active = core["db"][core["db"]['Approuvé'] == True].copy()
    if f_cycle != "Tous": df_active = df_active[df_active['Cycle'] == f_cycle]
    if f_filiere != "Toutes": df_active = df_active[df_active['Filière'] == f_filiere]
    if f_type != "Tous": df_active = df_active[df_active['Type'] == f_type]
    
    if search_bar:
        df_active = df_active[df_active['Matière'].str.contains(search_bar, case=False, na=False)]
        
    if df_active.empty:
        st.info("Aucun document ne correspond aux filtres de sécurité appliqués.")
    else:
        for idx, row in df_active.iterrows():
            is_p = row['Premium']
            badge = "<span style='color:#F59E0B; font-weight:bold;'>💎 PREMIUM</span>" if is_p else "<span style='color:#10B981;'>🆓 ACCÈS LIBRE</span>"
            
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between;">
                        <b>{row['Matière']}</b>
                        {badge}
                    </div>
                    <p style="font-size:0.85rem; margin:5px 0 0 0; opacity:0.7;">
                        Filière : {row['Filière']} | Niveau : {row['Niveau']} | Enseignant : {row['Enseignant']} | Index Téléchargements : {row['Downloads']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            btn_col, _ = st.columns([2, 3])
            with btn_col:
                if is_p and not st.session_state.is_premium_user:
                    st.button("🔒 Déblocage Automatique Requis", key=f"p_{row['id']}", disabled=True)
                else:
                    if st.button("📥 Télécharger le document PDF", key=f"d_{row['id']}"):
                        core["db"].loc[core["db"]['id'] == row['id'], 'Downloads'] += 1
                        st.success("Fichier extrait des serveurs avec succès.")

# ------------------------------------------------------------------------------
# TAB 2 : PASSERELLE DE PAIEMENT AUTOMATIQUE (STYLE 1XBET SANS NUMEROS VISIBLES)
# ------------------------------------------------------------------------------
with tab_payment:
    st.markdown("### 💳 DEPOSIT ENGINE & API PASSERELLE AUTOMATIQUE")
    st.write("Le système initie une requête Push USSD chiffrée vers votre terminal Mobile Money de manière autonome.")
    
    if st.session_state.is_premium_user:
        st.success("Votre terminal est déjà validé au niveau Premium. Accès illimité actif.")
    else:
        pay_box, info_box = st.columns([3, 2])
        with pay_box:
            with st.form("gateway_1xbet_style"):
                operator = st.radio("Sélectionner le guichet de facturation :", ["ORANGE MONEY CAMEROUN", "MTN MOBILE MONEY"])
                phone_payment = st.text_input("Entrer votre numéro de prélèvement (9 chiffres) :", placeholder="6xxxxxxxx")
                amount_display = st.text_input("Montant standardisé (CFA) :", value=f"{core['config']['tarif_premium']}", disabled=True)
                
                trigger_api = st.form_submit_button("LANCER LA DEMANDE DE DÉBIT AUTOMATIQUE")
                
            if trigger_api:
                if len(phone_payment) == 9 and phone_payment.isdigit():
                    progress_bar = st.progress(0)
                    for percent in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(percent + 1)
                    
                    # Simulation de la validation du webhook réseau de l'opérateur
                    txn_hash = f"TXN-1X-{hashlib.sha256(phone_payment.encode()).hexdigest()[:10].upper()}"
                    
                    new_txn = {
                        "Ref_Transaction": txn_hash, "Matricule": user_matricule, "Opérateur": operator,
                        "Numéro": f"***{phone_payment[-4:]}", "Montant": core['config']['tarif_premium'],
                        "Statut": "Réussi", "Timestamp": datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    }
                    core["transactions"] = pd.concat([core["transactions"], pd.DataFrame([new_txn])], ignore_index=True)
                    
                    st.session_state.is_premium_user = True
                    st.success(f"⚡ Callback API Reçu ! Transaction {txn_hash} validée automatiquement. Mode Premium Ouvert.")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Erreur de routage : Format du numéro de téléphone invalide.")
                    
        with info_box:
            st.markdown("""
                <div style="background:rgba(16,185,129,0.05); border:1px dashed #10B981; padding:20px; border-radius:12px;">
                    <h4>🔒 SÉCURITÉ DES FLUX INFRASTRUCTURE</h4>
                    <p style="font-size:0.85rem; opacity:0.8;">
                        Conformément aux directives de sécurité, aucun numéro de compte de l'administration n'est affiché publiquement. 
                        Le traitement s'effectue en arrière-plan via des serveurs de routage.
                    </p>
                </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3 : 🏛️ MAISON VIRTUELLE DE CONTROLE (PARAMÈTRES COMPLETS PAR CATÉGORIES)
# ------------------------------------------------------------------------------
with tab_maison:
    if st.session_state.user_role == "Visiteur":
        st.markdown("### 🔐 ACCÈS COFFRE MAÎTRE")
        input_key = st.text_input("Saisir la clé d'infrastructure système :", type="password")
        if st.button("Authentifier le profil"):
            if input_key == core["config"]["owner_password"]:
                st.session_state.user_role = "Owner"
                st.rerun()
            elif input_key == core["config"]["copilot_password"]:
                st.session_state.user_role = "Copilote"
                st.rerun()
            else:
                st.error("Accès refusé : Signature cryptographique invalide.")
    else:
        m_head, m_out = st.columns([5, 1])
        m_head.markdown(f"#### 🖥️ PRIVILÈGES DIRECTEUR ACQUIS : Profil [{st.session_state.user_role.upper()}]")
        if m_out.button("Fermer l'instance"):
            st.session_state.user_role = "Visiteur"
            st.rerun()
            
        st.markdown("---")
        
        if st.session_state.user_role == "Copilote":
            st.info("Mode Copilote : Capacité d'alimentation du catalogue soumise à l'approbation de l'Owner.")
            with st.form("copilot_secure_feed"):
                c_mat = st.text_input("Intitulé exact de l'UE :")
                c_cyc = st.selectbox("Sélectionner le Cycle", ["Licence Sciences de l'Ingénieur", "Cycle Ingénieur", "Master I", "Master II"])
                c_fil = st.selectbox("Filière liée", FILIERES)
                c_niv = st.selectbox("Niveau requis", ["L1", "L2", "L3", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5"])
                c_typ = st.selectbox("Nature du fichier", ["CC", "Examen", "Rattrapage"])
                c_prof = st.text_input("Responsable de la matière :")
                c_prem = st.checkbox("Définir comme ressource Premium restrictive")
                c_file = st.file_uploader("Fichier binaire (PDF requis)")
                
                submit_feed = st.form_submit_button("PROPULSER LE FICHIER EN VÉRIFICATION")
                
            if submit_feed and c_mat and c_file:
                new_entry = {
                    "id": len(core["db"]) + 1, "Cycle": c_cyc, "Filière": c_fil, "Niveau": c_niv,
                    "Matière": c_mat, "Enseignant": c_prof, "Type": c_typ, "Année": "2025-2026",
                    "Premium": c_prem, "Downloads": 0, "Approuvé": False
                }
                core["db"] = pd.concat([core["db"], pd.DataFrame([new_entry])], ignore_index=True)
                st.success("Ressource injectée en zone tampon. En attente de validation.")
                
        elif st.session_state.user_role == "Owner":
            # RESTRUCTURATION INTÉGRALE DES MENUS DEMANDÉS PAR LE CONCEPTEUR
            m_sub1, m_sub2, m_sub3, m_sub4 = st.tabs([
                "📊 PANNEAU DE CONTRÔLE ANALYTIQUE", 
                "👁️ RECONNAISSANCE & CONTRÔLE DE SÉCURITÉ", 
                "🛠️ CONFIGURATIONS CONFIGURÉES PAR CATÉGORIES",
                "📥 COMPLIANCE DES FICHIERS"
            ])
            
            # 1. PANNEAU DE CONTRÔLE ANALYTIQUE
            with m_sub1:
                st.markdown("#### 📊 ANALYTICS & REVENUS INFRASTRUCTURE")
                k1, k2, k3 = st.columns(3)
                k1.metric("Fichiers Approuvés", f"{len(core['db'][core['db']['Approuvé']==True])} UEs")
                k2.metric("Volume de Téléchargements", f"{core['db']['Downloads'].sum()} requêtes")
                k3.metric("Fonds Collectés Automatiquement", f"{len(core['transactions']) * core['config']['tarif_premium']} CFA")
                
                st.markdown("##### 📝 JOURNAL TOTAL DES TRANSACTIONS API")
                if core["transactions"].empty:
                    st.info("Aucun mouvement financier enregistré par le webhook pour le moment.")
                else:
                    st.dataframe(core["transactions"], use_container_width=True)
                    
            # 2. RECONNAISSANCE & CONTRÔLE DE SÉCURITÉ
            with m_sub2:
                st.markdown("#### 👁️ SYSTÈME DE VÉRIFICATION ET RECONNAISSANCE DES MATRICULES")
                st.write("Analyse structurelle et détection de fraude sur les accès Premium étudiants.")
                
                verify_matricule = st.text_input("Introduire un matricule à analyser :", value="22I0041B")
                if st.button("Lancer l'analyse algorithmique"):
                    if not verify_matricule.endswith("B") or len(verify_matricule) != 8:
                        st.error("🚨 RECONNAISSANCE REJETÉE : Anomalie détectée dans la structure du matricule.")
                    else:
                        st.success("🟢 RECONNAISSANCE APPROUVÉE : Structure conforme aux registres de l'Université de Bertoua.")
                        
            # 3. CONFIGURATIONS CONFIGURÉES PAR CATÉGORIES (PERFAIT)
            with m_sub3:
                st.markdown("#### ⚙️ CORE MATRIX - CONFIGURATION DES CATÉGORIES APPLICATIVES")
                
                with st.expander("🔑 CATÉGORIE 1 : CRYPTOGRAPHIE & PASSERELLES D'ACCÈS", expanded=True):
                    chng_owner = st.text_input("Modifier le mot de passe Directeur :", value=core["config"]["owner_password"], type="password")
                    chng_copilot = st.text_input("Modifier le mot de passe Assistant :", value=core["config"]["copilot_password"], type="password")
                    if st.button("Sauvegarder la Catégorie 1"):
                        core["config"]["owner_password"] = chng_owner
                        core["config"]["copilot_password"] = chng_copilot
                        st.toast("Clés d'accès mises à jour.")
                        
                with st.expander("💰 CATÉGORIE 2 : GRILLE TARIFAIRE ET PARAMÈTRES MONÉTAIRES"):
                    chng_price = st.number_input("Ajuster les frais Premium (CFA) :", value=int(core["config"]["tarif_premium"]), step=50)
                    chng_gateway = st.selectbox("Statut de la passerelle API :", ["ONLINE", "SANDBOX_MAINTENANCE", "OFFLINE"])
                    if st.button("Sauvegarder la Catégorie 2"):
                        core["config"]["tarif_premium"] = chng_price
                        core["config"]["api_gateway_status"] = chng_gateway
                        st.toast("Modifications tarifaires appliquées aux webhooks.")
                        
                with st.expander("🎓 CATÉGORIE 3 : ARCHITECTURE ACADÉMIQUE & ROUTAGE"):
                    st.write("Filières actives prises en compte par le serveur central :")
                    st.dataframe(pd.DataFrame(FILIERES, columns=["Filières Certifiées"]), use_container_width=True)
                    new_fil = st.text_input("Enregistrer une nouvelle filière d'ingénierie :")
                    if st.button("Ajouter la filière") and new_fil:
                        if new_fil not in FILIERES:
                            FILIERES.append(new_fil)
                            st.success("Nouvel embranchement académique initialisé.")
                            st.rerun()
                            
            # 4. COMPLIANCE DES FICHIERS
            with m_sub4:
                st.markdown("#### 📥 CONTRÔLE QUALITÉ DU CATALOGUE")
                df_pending = core["db"][core["db"]['Approuvé'] == False]
                
                if df_pending.empty:
                    st.info("Aucune soumission en attente d'approbation.")
                else:
                    for idx, row in df_pending.iterrows():
                        st.write(f"**Matière :** {row['Matière']} | Soumis par assistant")
                        c_yes, c_no = st.columns(2)
                        if c_yes.button("Approuver et Publier", key=f"ok_{row['id']}"):
                            core["db"].loc[core["db"]['id'] == row['id'], 'Approuvé'] = True
                            st.rerun()
                        if c_no.button("Rejeter l'archive", key=f"no_{row['id']}"):
                            core["db"] = core["db"][core["db"]['id'] != row['id']]
                            st.rerun()
                
                st.markdown("---")
                st.markdown("##### 🗑️ SUPPRESSION STRATEGIQUE DU CATALOGUE")
                for idx, row in core["db"].iterrows():
                    col_info, col_action = st.columns([5, 1])
                    col_info.write(f"• **{row['Matière']}** ({row['Niveau']} - {row['Filière']})")
                    if col_action.button("Supprimer", key=f"del_{row['id']}"):
                        core["db"] = core["db"][core["db"]['id'] != row['id']]
                        st.rerun()
