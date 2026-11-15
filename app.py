"""
Outil Complet de Simulation Métallurgique – Version Finale Intégrée
Extraction • Affinage • Thermodynamique • Cinétiques • Diffusion • Scories • Ellingham • Minerais • Finances
Auteur : Dr Ulrich Landry Compaoré – Génie Métallurgique – EPO Ouagadougou
Version Finale Unifiée – Novembre 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from math import erf

st.set_page_config(page_title="Métallurgie Complet – Dr Compaoré", page_icon="⚙️", layout="wide")

st.title("⚙️ Outil Complet de Simulation Métallurgique")
st.markdown("""
**Extraction primaire • Affinage • Équilibres • Cinétiques • Diffusion • Scories • Thermodynamique avancée • Minerais • Finances**  
**Auteur : Dr Ulrich Landry Compaoré – Génie Métallurgique – EPO Ouagadougou**
""")

# ==================== SIDEBAR ====================
st.sidebar.header("Module")
module = st.sidebar.radio("Choisir", [
    "1. Caractéristiques des Minerais",
    "2. Extraction Primaire",
    "3. Affinage Secondaire",
    "4. Équilibres Thermodynamiques",
    "5. Cinétiques de Réaction",
    "6. Diffusion & Transfert de Masse",
    "7. Optimisation Q/K & Récupération",
    "8. Thermodynamique des Scories",
    "9. Modélisation Thermodynamique Avancée",
    "10. Réacteurs Catalytiques",
    "11. Bilans Énergétiques & Financiers"
])

metal = st.sidebar.selectbox("Métal", 
    ["Fer (Fe)", "Aluminium (Al)", "Gallium (Ga)", "Manganèse (Mn)", "Zinc (Zn)", "Cuivre (Cu)"])

# ==================== FONCTIONS ====================
def show_image(name, caption):
    path = f"images/{name}"
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)

def show_sankey(labels, sources, targets, values, title):
    fig = go.Figure(go.Sankey(node=dict(pad=12, thickness=18, label=labels, color="#1a5276"),
                              link=dict(source=sources, target=targets, value=values)))
    fig.update_layout(title=title, height=380, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

def arrhenius(T_C, Ea_kJ, k0):
    return k0 * np.exp(-Ea_kJ * 1000 / (8.314 * (T_C + 273.15)))

def get_metal_params(metal):
    """Paramètres cinétiques et de diffusion typiques selon le métal"""
    params = {
        "Fer (Fe)": {"Ea": 125, "k0": 5e5, "D_Ea": 150, "D0": 1.5e-4, "base_rec": 94},
        "Aluminium (Al)": {"Ea": 180, "k0": 2e6, "D_Ea": 200, "D0": 8e-5, "base_rec": 88},
        "Gallium (Ga)": {"Ea": 140, "k0": 1e5, "D_Ea": 160, "D0": 5e-5, "base_rec": 75},
        "Manganèse (Mn)": {"Ea": 145, "k0": 3e5, "D_Ea": 165, "D0": 1e-4, "base_rec": 90},
        "Zinc (Zn)": {"Ea": 110, "k0": 8e5, "D_Ea": 130, "D0": 2e-4, "base_rec": 92},
        "Cuivre (Cu)": {"Ea": 95, "k0": 1e6, "D_Ea": 120, "D0": 2.5e-4, "base_rec": 95},
    }
    return params.get(metal, params["Fer (Fe)"])

def get_ore_constants(mineral):
    """Constantes spécifiques selon le minerai"""
    ores = {
        "Hématite": {"k_factor": 1.0, "D_factor": 1.0, "rec_factor": 1.0, "note": "Réduction relativement facile"},
        "Magnétite": {"k_factor": 0.85, "D_factor": 0.9, "rec_factor": 0.97, "note": "Structure spinelle, cinétique légèrement plus lente"},
        "Pyrolusite": {"k_factor": 1.1, "D_factor": 1.05, "rec_factor": 0.95, "note": "Bonne réactivité"},
        "Chalcopyrite": {"k_factor": 0.7, "D_factor": 0.8, "rec_factor": 0.92, "note": "Cinétique plus lente, nécessite conditions oxydantes"},
        "Sphalérite": {"k_factor": 0.9, "D_factor": 0.95, "rec_factor": 0.94, "note": "Réactivité intermédiaire"},
        "Bauxite (Gibbsite)": {"k_factor": 0.6, "D_factor": 0.7, "rec_factor": 0.85, "note": "Procédé Bayer, cinétique lente à basse température"},
    }
    return ores.get(mineral, ores["Hématite"])

def show_interpretation(title, text):
    with st.expander(f"Interprétation technique : {title}", expanded=False):
        st.markdown(text)
    st.subheader("Données de marché indicatives (FCFA / t)")
    market = pd.DataFrame({
        "Métal": ["Fer (acier)", "Aluminium", "Manganèse (FeMn)", "Zinc", "Cuivre"],
        "Prix indicatif (FCFA/t)": [450_000, 1_800_000, 1_200_000, 2_100_000, 6_500_000],
        "Tendance": ["Stable", "Hausse modérée", "Stable", "Hausse", "Forte hausse"]
    })
    st.dataframe(market, hide_index=True)
    st.caption("Prix approximatifs – à actualiser selon les cours LME / marchés locaux (novembre 2026).")

# ==================== 1. EXTRACTION PRIMAIRE ====================
if module == "2. Extraction Primaire":
    st.header(f"Extraction Primaire – {metal}")
    with st.expander("Explication scientifique du module", expanded=False):
        st.markdown("""
        **Objectif :** Estimer la masse de minerai nécessaire et la quantité de laitier formé.
        
        **Paramètres :**
        - Teneur en métal : détermine la quantité de minerai à traiter (relation inverse).
        - Rendement : tient compte des pertes réelles du procédé.
        - Composition de la gangue : permet d’estimer la masse et la composition du laitier.
        
        **Modèle :** Bilan matière simple basé sur la conservation de la masse.
        
        **Limitations :**
        - Ne tient pas compte des cinétiques ni des équilibres thermodynamiques fins.
        - La composition du laitier est approximative.
        
        **Cas d’utilisation :** Dimensionnement préliminaire, comparaison de minerais, estimation de flux.
        """)
    st.info("Calcul de la masse de minerai nécessaire et composition du laitier. Adapté à Fe, Al, Mn, Zn, Cu et Ga.")

    # ==================== PRÉPARATION DU MINERAI ====================
    st.subheader("1. Préparation du minerai")
    mineral_ext = st.selectbox("Type de minerai", 
        ["Hématite (Fe)", "Magnétite (Fe)", "Pyrolusite (Mn)", "Chalcopyrite (Cu)", "Sphalérite (Zn)", "Bauxite (Al)"], key="min_prep")
    
    c_prep1, c_prep2 = st.columns(2)
    with c_prep1:
        taille_cible = st.slider("Taille cible après broyage (µm)", 30, 400, 120)
        prechauffage = st.slider("Température de préchauffage (°C)", 150, 900, 450)
        duree_prechauffage = st.slider("Durée de préchauffage (min)", 10, 180, 45)
    with c_prep2:
        sechage = st.checkbox("Appliquer un séchage", value=True)
        agglomeration = st.checkbox("Agglomération / pelletisation", value=False)
        atmosphere = st.selectbox("Atmosphère de préchauffage", ["Air", "Gaz neutre", "Réductrice faible"])
    
    st.write(f"**Préparation** : {taille_cible} µm | Préchauffage {prechauffage} °C pendant {duree_prechauffage} min ({atmosphere})")
    
    with st.expander("Rôle du préchauffage"):
        st.markdown("""
        **Objectifs du préchauffage :**
        - Éliminer l’humidité résiduelle
        - Préparer thermiquement le minerai avant le four de réduction ou le grillage
        - Réduire le choc thermique
        - Dans certains cas, initier une décomposition partielle (carbonates, hydrates)
        
        **Paramètres importants :**
        - Température : dépend du minerai (plus élevée pour les minerais réfractaires)
        - Durée : doit être suffisante pour une chauffe homogène
        - Atmosphère : air pour séchage/grillage, neutre ou légèrement réductrice selon le procédé
        """)
    
    with st.expander("Détails sur l’atmosphère de préchauffage"):
        st.markdown("""
        **Choix de l’atmosphère selon l’objectif :**
        
        **1. Air (oxydante)**
        - Utilisée pour le séchage simple et le grillage oxydant
        - Permet l’oxydation des sulfures (ex. chalcopyrite, sphalérite)
        - Risque d’oxydation non désirée pour certains oxydes
        
        **2. Gaz neutre (N₂, Ar)**
        - Évite les réactions d’oxydation ou de réduction
        - Adapté au préchauffage de minerais sensibles
        - Plus coûteux
        
        **3. Atmosphère réductrice faible (CO/CO₂ contrôlé, gaz de haut fourneau dilué)**
        - Permet un début de réduction ou évite la réoxydation
        - Utilisée avant certains procédés de réduction directe
        - Nécessite un contrôle précis du potentiel d’oxygène
        
        **Recommandations :**
        - Minerais de fer (hématite, magnétite) : air ou légèrement réductrice selon le procédé aval
        - Sulfures (Cu, Zn) : air pour le grillage
        - Bauxite : air (séchage / calcination)
        - Éviter une atmosphère trop réductrice si l’objectif est uniquement le séchage
        """)
    
    with st.expander("Types de fours industriels"):
        st.markdown("""
        **Principaux fours utilisés en métallurgie extractive :**
        
        **1. Haut fourneau**
        - Réduction des minerais de fer (et parfois de manganèse)
        - Fonctionne en continu avec coke et vent chaud
        - Produit de la fonte
        
        **2. Four à arc électrique (EAF)**
        - Fusion de ferrailles ou de preréduits
        - Flexible, utilisé pour l’acier
        - Peut être couplé à une réduction directe
        
        **3. Four rotatif**
        - Grillage, calcination, réduction directe (SL/RN, etc.)
        - Bon mélange et transfert thermique
        - Utilisé pour Zn, certains procédés de Fe et Mn
        
        **4. Four flash / Four de fusion flash**
        - Traitement des concentrés de sulfures (Cu, Ni)
        - Réaction très rapide grâce à la finesse des particules
        
        **5. Cellule d’électrolyse**
        - Aluminium (Hall-Héroult), zinc, cuivre (affinage)
        - Réduction électrolytique
        
        **6. Four de préchauffage / séchoir rotatif**
        - Préparation thermique du minerai avant le four principal
        
        **Choix du four selon le minerai :**
        - Fer : haut fourneau ou réduction directe + EAF
        - Manganèse : haut fourneau ou four à arc (FeMn)
        - Cuivre : four flash ou four à réverbère + convertisseur
        - Zinc : four rotatif ou hydrométallurgie + électrolyse
        - Aluminium : cellule Hall-Héroult après Bayer
        """)
    
    with st.expander("Techniques de séchage du minerai"):
        st.markdown("""
        **Principales techniques de séchage :**
        
        1. **Séchage à l’air libre / solaire**  
           - Simple et peu coûteux  
           - Lent, dépend des conditions climatiques  
           - Adapté aux climats secs (ex. Sahel)
        
        2. **Séchoirs rotatifs**  
           - Couramment utilisés en métallurgie  
           - Bon contact gaz-solide  
           - Température contrôlée (100–400 °C)
        
        3. **Séchoirs à lit fluidisé**  
           - Excellent transfert thermique  
           - Adapté aux fines particules  
           - Consommation énergétique modérée
        
        4. **Séchoirs à bande ou à plateaux**  
           - Pour des débits plus faibles ou des minerais sensibles
        
        **Objectifs du séchage :**
        - Réduire l’humidité avant le préchauffage ou le grillage
        - Éviter les explosions de vapeur dans les fours
        - Améliorer l’efficacité énergétique du procédé principal
        - Faciliter le transport et le stockage
        """)
    
    st.subheader("Étapes de séchage")
    etapes_sechage = [
        "1. Réception et stockage du minerai humide",
        "2. Alimentation du séchoir (rotatif, lit fluidisé ou bande)",
        "3. Chauffage progressif (80–250 °C selon le minerai)",
        "4. Évacuation de la vapeur d’eau",
        "5. Contrôle de l’humidité résiduelle (< 1–2 % en général)",
        "6. Refroidissement éventuel avant préchauffage ou stockage"
    ]
    for etape in etapes_sechage:
        st.write(f"• {etape}")
    
    humidite_finale = st.slider("Humidité résiduelle cible (%)", 0.2, 5.0, 1.0)
    humidite_in = st.slider("Humidité initiale du minerai (%)", 1.0, 15.0, 6.0, key="hum_in_sech")
    st.caption(f"Objectif de séchage : humidité ≤ {humidite_finale} %")
    
    if st.button("Optimiser les paramètres de séchage"):
        # Recommandations simples selon humidité initiale et taille
        if humidite_in > 8:
            T_sech = 220
            duree_sech = 60
            st.warning("Humidité élevée → température et durée plus importantes")
        elif humidite_in > 4:
            T_sech = 180
            duree_sech = 40
            st.info("Humidité moyenne → paramètres standards")
        else:
            T_sech = 140
            duree_sech = 25
            st.success("Humidité faible → séchage léger suffisant")
        
        if taille_cible < 80:
            duree_sech = int(duree_sech * 0.8)
            st.write("Particules fines → temps de séchage réduit")
        
        st.metric("Température de séchage recommandée", f"{T_sech} °C")
        st.metric("Durée de séchage optimisée", f"{duree_sech} min")
        st.metric("Humidité résiduelle optimisée", f"{humidite_finale} %")
        
        # Ajustement de l'humidité cible selon le minerai
        if "Bauxite" in mineral_ext:
            hum_opt = max(0.5, humidite_finale)
            st.info("Bauxite : humidité résiduelle un peu plus élevée acceptable avant Bayer")
        elif "Chalcopyrite" in mineral_ext or "Sphalérite" in mineral_ext:
            hum_opt = min(1.0, humidite_finale)
            st.info("Sulfures : humidité basse recommandée avant grillage")
        else:
            hum_opt = humidite_finale
        
        st.success(f"Paramètres optimisés : {T_sech} °C pendant {duree_sech} min → humidité cible {hum_opt} %")
        st.caption("Recommandations indicatives basées sur l’humidité initiale, la taille des particules et le type de minerai.")
    
    # Route spécifique
    st.subheader("2. Route d’extraction selon le minerai")
    if "Hématite" in mineral_ext or "Magnétite" in mineral_ext:
        st.success("Route **Fer** : Réduction carbothermique (coke + chaux)")
        route_txt = "Réduction carbothermique"
    elif "Pyrolusite" in mineral_ext:
        st.success("Route **Manganèse** : Réduction carbothermique → ferromanganèse")
        route_txt = "Réduction carbothermique (FeMn)"
    elif "Chalcopyrite" in mineral_ext:
        st.warning("Route **Cuivre** : Grillage oxydant puis fusion ou hydrométallurgie")
        route_txt = "Grillage + pyrométallurgie / hydrométallurgie"
    elif "Sphalérite" in mineral_ext:
        st.warning("Route **Zinc** : Grillage puis réduction ou lixiviation-électrolyse")
        route_txt = "Grillage + réduction ou hydrométallurgie"
    else:
        st.info("Route **Aluminium** : Bayer (lixiviation) puis Hall-Héroult")
        route_txt = "Bayer + électrolyse"
    
    st.caption(f"Route retenue : {route_txt}")

    st.subheader("3. Composition selon le minerai")
    c1, c2, c3 = st.columns(3)
    with c1:
        if "Hématite" in mineral_ext or "Magnétite" in mineral_ext:
            main = st.slider("Fe %", 55., 67., 63.)
            label_main = "Fe"
        elif "Pyrolusite" in mineral_ext:
            main = st.slider("Mn %", 38., 52., 46.)
            label_main = "Mn"
        elif "Chalcopyrite" in mineral_ext:
            main = st.slider("Cu %", 22., 35., 28.)
            label_main = "Cu"
        elif "Sphalérite" in mineral_ext:
            main = st.slider("Zn %", 48., 60., 54.)
            label_main = "Zn"
        else:
            main = st.slider("Al₂O₃ %", 45., 58., 51.)
            label_main = "Al₂O₃"
        sio2 = st.slider("SiO₂ %", 1., 20., 6.0)
    with c2:
        cao = st.slider("CaO %", 0., 12., 2.5)
        if "Pyrolusite" in mineral_ext:
            impurete = st.slider("Fe₂O₃ %", 0., 15., 5.0)
        elif "Chalcopyrite" in mineral_ext:
            impurete = st.slider("Fe %", 5., 25., 12.0)
        elif "Sphalérite" in mineral_ext:
            impurete = st.slider("Fe %", 0., 15., 6.0)
        else:
            impurete = st.slider("Autres oxydes %", 0., 10., 3.0)
    with c3:
        mgo = st.slider("MgO %", 0., 8., 1.2)
        # Rendement influencé par la préparation
        base_rec = 88.0
        # Effet taille (plus fin = meilleur, jusqu'à un certain point)
        if taille_cible < 80:
            base_rec += 3.5
        elif taille_cible < 150:
            base_rec += 1.5
        elif taille_cible > 250:
            base_rec -= 2.5
        # Effet préchauffage
        if prechauffage > 500:
            base_rec += 2.0
        elif prechauffage < 300:
            base_rec -= 1.5
        # Effet séchage et agglomération
        if sechage:
            base_rec += 1.0
        if agglomeration:
            base_rec += 1.8
        recovery = min(98.5, max(75.0, base_rec))
        st.metric("Rendement estimé (après préparation)", f"{recovery:.1f} %")
        st.caption("Le rendement dépend de la taille, du préchauffage, du séchage et de l’agglomération.")

    # ==================== IMPACT GRANULOMÉTRIE & OPTIMISATION BROYAGE ====================
    st.subheader("Impact de la granulométrie et optimisation du broyage")
    
    tailles = np.array([30, 50, 80, 120, 180, 250, 350])
    # Modèle simple : rendement vs taille
    rec_granulo = 92 - 0.04*(tailles - 80) - 0.0003*(tailles - 80)**2
    rec_granulo = np.clip(rec_granulo, 78, 97)
    
    fig_gran = go.Figure()
    fig_gran.add_trace(go.Scatter(x=tailles, y=rec_granulo, mode="lines+markers", 
                                  line=dict(width=3, color="#1a5276"), name="Rendement"))
    fig_gran.add_vline(x=taille_cible, line_dash="dash", line_color="red", annotation_text="Taille actuelle")
    fig_gran.update_layout(title="Impact de la taille des particules sur le rendement",
                           xaxis_title="Taille (µm)", yaxis_title="Rendement estimé (%)", height=400)
    st.plotly_chart(fig_gran, use_container_width=True)
    show_interpretation("Granulométrie et rendement", """
    **Lecture de la courbe :**
    - Le rendement passe par un optimum autour de 80–120 µm.
    - En dessous : gains limités et énergie de broyage très élevée.
    - Au-dessus : la cinétique ralentit car la surface spécifique diminue.
    
    **Recommandation :** viser la zone où la pente commence à s’aplatir pour optimiser le compromis rendement / coût énergétique.
    """)
    
    # Énergie de broyage (Bond simplifié)
    Wi = 14.0  # kWh/t indicatif
    F80 = 2000  # µm alimentation
    P80 = taille_cible
    E_broyage = Wi * (10/np.sqrt(P80) - 10/np.sqrt(F80))
    st.metric("Énergie de broyage indicative", f"{E_broyage:.1f} kWh/t")
    
    if taille_cible < 60:
        st.warning("Taille très fine → bon rendement mais énergie de broyage élevée et risque de boues")
    elif taille_cible < 120:
        st.success("Taille favorable : bon compromis rendement / énergie")
    else:
        st.info("Taille plus grossière → énergie plus faible mais rendement légèrement réduit")
    
    st.caption("L’optimisation consiste à trouver le meilleur compromis entre rendement métallurgique et coût énergétique du broyage.")
    
    # ==================== CONDUCTIVITÉ THERMIQUE DES SCORIES ====================
    st.subheader("Conductivité thermique du laitier")
    st.markdown("Estimation de la conductivité thermique en fonction de la composition et de la température.")
    
    T_cond = st.slider("Température pour conductivité (°C)", 1300, 1600, 1450, key="T_cond")
    # Modèle simplifié de conductivité (W/m·K)
    # Base + effet basicité + effet température
    k_therm = 0.8 + 0.4 * B2 + 0.001 * (T_cond - 1400)
    k_therm = max(0.5, min(2.5, k_therm))
    
    st.metric("Conductivité thermique estimée", f"{k_therm:.2f} W/m·K")
    
    T_range_cond = np.linspace(1300, 1600, 30)
    k_range = 0.8 + 0.4 * B2 + 0.001 * (T_range_cond - 1400)
    fig_cond = go.Figure(go.Scatter(x=T_range_cond, y=k_range, mode="lines", 
                                    line=dict(width=3, color="#c0392b"), name="k thermique"))
    fig_cond.update_layout(title="Conductivité thermique vs Température",
                           xaxis_title="Température (°C)", yaxis_title="Conductivité (W/m·K)",
                           height=380, showlegend=True)
    st.plotly_chart(fig_cond, use_container_width=True)
    
    show_interpretation("Conductivité thermique", """
    **Interprétation :**
    - La conductivité thermique des laitiers silicatés est généralement faible (0,5 – 2 W/m·K).
    - Elle augmente légèrement avec la température et la basicité.
    - Une faible conductivité ralentit les transferts thermiques dans le four et influence le profil de température.
    
    Cette valeur est utile pour les bilans thermiques et la modélisation des fours.
    """)
    
    st.latex(r"k_{\text{therm}} \approx 0{,}8 + 0{,}4 \cdot B + 0{,}001 \cdot (T - 1400)")
    st.caption("Modèle empirique simplifié (B = basicité CaO/SiO₂).")

    gangue = sio2 + cao + mgo + impurete
    st.write(f"**{label_main}** : {main:.1f} %  |  **Gangue + impuretés** : {gangue:.1f} %")
    st.caption("""
    Plages pratiques industrielles :
    • Fe (concentré) : 55–67 %  
    • Mn (minerai riche) : 38–52 %  
    • Cu (concentré) : 22–35 %  
    • Zn (concentré) : 48–60 %  
    • Al₂O₃ (bauxite) : 45–58 %
    """)

    if st.button("Calculer extraction après préparation"):
        m_product = 1000.0
        if "Ga" in metal:
            m_ore = 2500
        else:
            m_ore = (m_product / (recovery/100)) / (main/100 if "Al" not in metal else 0.53)
        
        st.metric("Masse de minerai (après préparation)", f"{m_ore:,.0f} kg / t de métal")
        st.success(f"Route appliquée : {route_txt}")
        
        # Teneur en métal après extraction primaire
        if "Hématite" in mineral_ext or "Magnétite" in mineral_ext:
            teneur_produit = 94.5   # fonte / fer spongieux typique
            nom_produit = "Fonte / Fer préréduit"
        elif "Pyrolusite" in mineral_ext:
            teneur_produit = 75.0   # FeMn typique
            nom_produit = "Ferromanganèse"
        elif "Chalcopyrite" in mineral_ext:
            teneur_produit = 98.5   # blister copper
            nom_produit = "Cuivre blister"
        elif "Sphalérite" in mineral_ext:
            teneur_produit = 98.0
            nom_produit = "Zinc primaire"
        else:
            teneur_produit = 99.7
            nom_produit = "Aluminium primaire"
        
        st.metric(f"Teneur en métal après extraction ({nom_produit})", f"{teneur_produit} %")
        st.caption("Teneur typique du produit issu de l’extraction primaire (avant affinage secondaire).")
        st.write(f"Taille : {taille_cible} µm | Préchauffage : {prechauffage} °C pendant {duree_prechauffage} min | Séchage : {'Oui' if sechage else 'Non'}")
        m_slag = m_ore * (gangue/100) * 1.18
        st.metric("Masse laitier", f"{m_slag:.0f} kg/t métal")
        
        slag_comp = pd.DataFrame({
            "Constituant": ["SiO₂", "CaO", "MgO", "Impuretés principales", label_main + " (résiduel)"],
            "% dans laitier (approx)": [
                round(sio2/gangue*100,1) if gangue else 0,
                round(cao/gangue*100,1) if gangue else 0,
                round(mgo/gangue*100,1) if gangue else 0,
                round(impurete/gangue*100,1) if gangue else 0,
                round(5,1)
            ]
        })
        st.subheader("Composition estimée du laitier")
        st.dataframe(slag_comp, hide_index=True)
        
        # Bouton téléchargement
        st.download_button(
            label="Télécharger composition laitier (CSV)",
            data=slag_comp.to_csv(index=False).encode("utf-8"),
            file_name="composition_laitier.csv",
            mime="text/csv"
        )
        
        show_sankey(["Minerai","Flux","Procédé","Métal","Laitier"], [0,1,2,2],[2,2,3,4],
                    [m_ore, 150, 1000, m_slag], "Flux avec laitier multi-oxydes")
        
        st.subheader("Interprétation")
        st.info(f"""
        - Masse de minerai nécessaire : {m_ore:,.0f} kg pour 1 t de métal  
        - Rendement après préparation : {recovery:.1f} %  
        - Une préparation optimale (taille fine, préchauffage, séchage, agglomération) améliore le rendement
        """)
        
        # Bilan matière détaillé
        st.subheader("Bilan matière détaillé")
        bilan = pd.DataFrame({
            "Flux": ["Minerai", "Flux (chaux, etc.)", "Métal produit", "Laitier", "Gaz / pertes"],
            "Masse (kg/t métal)": [round(m_ore,0), 150, 1000, round(m_slag,0), round(m_ore*0.05,0)]
        })
        st.dataframe(bilan, hide_index=True)
        
        # Énergie indicative
        energy_ext = 2.5 if "Fer" in metal else 12 if "Al" in metal else 4.5
        st.metric("Énergie indicative du procédé", f"{energy_ext} MWh/t")
        
        with st.expander("Réactifs chimiques utilisés en extraction primaire"):
            st.markdown("""
            **Principaux réactifs selon le métal :**
            
            - **Fer** : Coke (C), Chaux (CaO), Air/Oxygène  
              → Réduction de Fe₂O₃ / Fe₃O₄ et formation de laitier
            
            - **Aluminium** : Soude (NaOH) pour le procédé Bayer, puis électrolyse (Al₂O₃ + cryolithe)  
              → Dissolution de la bauxite puis réduction électrolytique
            
            - **Manganèse** : Coke + Chaux  
              → Réduction carbothermique de MnO₂
            
            - **Cuivre** : Oxygène (grillage), puis réducteur ou électrolyse  
              → Oxydation des sulfures puis affinage
            
            - **Zinc** : Coke ou électrolyse après grillage  
              → Réduction de ZnO ou électrolyse de ZnSO₄
            """)

# ==================== 2. AFFINAGE SECONDAIRE ====================
elif module == "3. Affinage Secondaire":
    st.header(f"Affinage Secondaire – {metal}")
    st.info("Choisissez le métal à affiner. Les étapes et réactifs s’adaptent automatiquement.")
    
    # Pureté et impuretés selon le métal
    if "Fer" in metal:
        purity_in = st.slider("Pureté entrée %", 92., 99., 96.5)
        purity_target = st.slider("Pureté cible %", 98.5, 99.99, 99.7)
        impurity = st.slider("Soufre entrée (ppm)", 50, 800, 200)
        impurity_target = st.slider("Soufre cible (ppm)", 5, 50, 15)
        impurity_name = "S"
    elif "Mn" in metal:
        purity_in = st.slider("Teneur Mn entrée %", 70., 85., 75.)
        purity_target = st.slider("Teneur Mn cible %", 78., 90., 82.)
        impurity = st.slider("C entrée %", 1., 8., 6.5)
        impurity_target = st.slider("C cible %", 0.5, 2.5, 1.5)
        impurity_name = "C"
    elif "Cu" in metal:
        purity_in = st.slider("Pureté entrée %", 97., 99.5, 98.5)
        purity_target = st.slider("Pureté cible %", 99.5, 99.99, 99.95)
        impurity = st.slider("O entrée (ppm)", 100, 2000, 500)
        impurity_target = st.slider("O cible (ppm)", 10, 100, 30)
        impurity_name = "O"
    elif "Zn" in metal:
        purity_in = st.slider("Pureté entrée %", 98., 99.8, 99.0)
        purity_target = st.slider("Pureté cible %", 99.5, 99.995, 99.99)
        impurity = st.slider("Pb entrée (ppm)", 10, 500, 100)
        impurity_target = st.slider("Pb cible (ppm)", 1, 20, 5)
        impurity_name = "Pb"
    elif "Al" in metal:
        purity_in = st.slider("Pureté entrée %", 99.0, 99.8, 99.5)
        purity_target = st.slider("Pureté cible %", 99.7, 99.99, 99.85)
        impurity = st.slider("Fe entrée (ppm)", 100, 2000, 500)
        impurity_target = st.slider("Fe cible (ppm)", 50, 300, 100)
        impurity_name = "Fe"
    else:
        purity_in = st.slider("Pureté entrée %", 95., 99., 97.)
        purity_target = st.slider("Pureté cible %", 98., 99.9, 99.5)
        impurity = st.slider("Impureté principale (ppm)", 50, 1000, 200)
        impurity_target = st.slider("Impureté cible (ppm)", 5, 50, 20)
        impurity_name = "Impureté"
    
    st.subheader("Étapes d’affinage adaptées")
    if "Fer" in metal:
        st.markdown("""
        1. Désulfuration (CaO, Mg)  
        2. Déphosphoration  
        3. Dégazage (argon)  
        4. Alliage et contrôle des inclusions
        """)
    elif "Mn" in metal:
        st.markdown("""
        1. Affinage du ferromanganèse  
        2. Contrôle du carbone  
        3. Ajustement de la composition  
        4. Décantation du laitier
        """)
    elif "Cu" in metal:
        st.markdown("""
        1. Affinage au feu (oxydation des impuretés)  
        2. Réduction (poling ou gaz)  
        3. Coulée de anodes  
        4. Électrolyse (affinage électrolytique)
        """)
    elif "Zn" in metal:
        st.markdown("""
        1. Distillation ou électrolyse  
        2. Élimination du plomb et du cadmium  
        3. Affinage final
        """)
    elif "Al" in metal:
        st.markdown("""
        1. Affinage électrolytique (cellule à trois couches) ou  
        2. Traitement au chlore / flux  
        3. Contrôle des impuretés (Fe, Si)
        """)
    else:
        st.markdown("Étapes d’affinage spécifiques au métal sélectionné.")
    
    if st.button("Simuler affinage"):
        st.success(f"Pureté / teneur finale : **{purity_target} %**")
        st.write(f"{impurity_name} final : **{impurity_target}**")
        st.metric("Métal affiné", metal)
        if purity_target >= 99.5 or ("Mn" in metal and purity_target >= 80):
            st.success("Niveau de pureté élevé atteint")
        else:
            st.info("Pureté intermédiaire")

# ==================== 3. ÉQUILIBRES THERMODYNAMIQUES ====================
elif module == "4. Équilibres Thermodynamiques":
    st.header("Équilibres Thermodynamiques")
    T = st.slider("Température (°C)", 800, 1700, 1200)
    reaction = st.selectbox("Réaction", [
        "FeO + CO ⇌ Fe + CO₂",
        "MnO + C ⇌ Mn + CO",
        "Cu₂S + O₂ ⇌ 2Cu + SO₂",
        "CaO + [S] ⇌ CaS + [O]"
    ])
    
    if "FeO" in reaction:
        K = np.exp(15000/(T+273) - 8.5)
        Q = st.slider("Q (P_CO2/P_CO)", 0.1, 5.0, 0.4)
    elif "MnO" in reaction:
        K = np.exp(20000/(T+273) - 12)
        Q = st.slider("Q", 0.05, 3.0, 0.3)
    else:
        K = np.exp(10000/(T+273) - 6)
        Q = st.slider("Q", 0.01, 2.0, 0.2)
    
    st.metric("Constante d’équilibre K", f"{K:.3e}")
    st.metric("Quotient Q", f"{Q:.3f}")
    
    if Q < K:
        st.success("✅ Q < K → Réaction favorisée dans le sens direct")
        st.info("Interprétation : les conditions thermodynamiques sont favorables. Maintenir un excès de réducteur ou retirer les produits pour conserver Q < K.")
    else:
        st.error("❌ Q ≥ K → Réaction non favorisée")
        st.warning("Interprétation : la réaction n’est pas spontanée. Augmenter la température (si endothermique), baisser la pression partielle des produits ou modifier la composition du laitier.")
    
    st.subheader("Comment maintenir Q < K")
    st.markdown("""
    - Augmenter l’activité des réactifs  
    - Retirer les produits en continu  
    - Augmenter la température si endothermique  
    - Baisser la pression partielle des produits gazeux  
    - Utiliser un excès de réducteur ou de flux
    """)

# ==================== 4. CINÉTIQUES DE RÉACTION ====================
elif module == "5. Cinétiques de Réaction":
    st.header(f"Cinétiques de Réaction – {metal}")
    with st.expander("Explication scientifique du module", expanded=False):
        st.markdown("""
        **Objectif :** Simuler la vitesse des réactions et l’évolution de la conversion.
        
        **Paramètres clés :**
        - Ea (énergie d’activation) : barrière énergétique à franchir. Plus Ea est élevée, plus la réaction est sensible à la température.
        - k₀ : facteur pré-exponentiel lié à la fréquence des collisions efficaces.
        - Ordre de réaction : traduit la dépendance de la vitesse aux concentrations.
        
        **Modèle d’Arrhenius :** \( k = k_0 \exp(-E_a/RT) \)
        - Justification : issu de la théorie des collisions et de l’état de transition.
        - Limitations : suppose Ea constante, ne capture pas les changements de mécanisme.
        
        **Cas d’utilisation :**
        - Comparaison de réactivités.
        - Estimation de l’effet de la température.
        - Choix entre différents modèles (contracting, nucléation, etc.) selon la forme des courbes expérimentales.
        """)
    params = get_metal_params(metal)
    mineral = st.selectbox("Minerai", ["Hématite", "Magnétite", "Pyrolusite", "Chalcopyrite", "Sphalérite", "Bauxite (Gibbsite)"], key="min_cin")
    ore = get_ore_constants(mineral)
    st.info(f"Métal : {metal} | Minerai : {mineral} → {ore['note']}")
    
    T = st.slider("Température (°C)", 700, 1600, 1100)
    Ea = st.number_input("Énergie d’activation Ea (kJ/mol)", 60., 220., float(params["Ea"]))
    k0 = st.number_input("Facteur pré-exponentiel k₀", 1e4, 1e7, float(params["k0"] * ore["k_factor"]), format="%.0e")
    order = st.slider("Ordre n", 0.5, 2.0, 1.0, 0.1)
    tmax = st.slider("Temps (min)", 30, 240, 90)
    
    k = arrhenius(T, Ea, k0)
    st.latex(r"k = k_0 \exp\left(-\frac{E_a}{RT}\right)")
    st.markdown("**Équations cinétiques détaillées :**")
    st.latex(r"\frac{d\alpha}{dt} = k \cdot (1 - \alpha)^n")
    st.latex(r"t = \frac{1}{k} \ln\left(\frac{1}{1-\alpha}\right) \quad \text{(ordre 1)}")
    st.caption("Ces équations décrivent l’évolution de la conversion en fonction du temps selon l’ordre de réaction.")
    st.metric("Constante de vitesse k", f"{k:.3e} min⁻¹")
    
    t = np.linspace(0, tmax, 120)
    if abs(order - 1) < 0.05:
        alpha = 1 - np.exp(-k * t)
        st.latex(r"\alpha = 1 - e^{-kt}")
    else:
        alpha = 1 - np.power(1 + (order-1)*k*t, 1/(1-order))
        alpha = np.clip(alpha, 0, 0.995)
        st.latex(r"\alpha = 1 - [1+(n-1)kt]^{1/(1-n)}")
    
    fig = go.Figure(go.Scatter(x=t, y=alpha*100, mode="lines", line=dict(width=3, color="#1a5276")))
    fig.update_layout(title=f"Conversion (ordre {order})", xaxis_title="Temps (min)", yaxis_title="Conversion (%)", height=420)
    st.plotly_chart(fig, use_container_width=True)
    
    # ==================== ANALYSE DES PARAMÈTRES D'ACTIVATION ====================
    st.subheader("Analyse des paramètres d’activation")
    st.markdown("Étude de la sensibilité de la constante de vitesse aux paramètres d’Arrhenius.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        Ea_range = st.slider("Plage Ea (kJ/mol)", 60., 220., (80., 160.))
        k0_fixed = st.number_input("k₀ fixe pour analyse Ea", 1e4, 1e7, 5e5, format="%.0e", key="k0_fix")
    with col_b:
        k0_range = st.slider("Plage k₀ (facteur)", 0.1, 10., (0.5, 5.))
        T_fixed = st.slider("Température fixe pour analyse k₀ (°C)", 800, 1500, 1100)
    
    # Courbe k vs Ea
    Eas = np.linspace(Ea_range[0], Ea_range[1], 40)
    ks_Ea = arrhenius(T, Eas, k0_fixed)
    
    fig_Ea = go.Figure()
    fig_Ea.add_trace(go.Scatter(x=Eas, y=ks_Ea, mode="lines", line=dict(width=3, color="#1a5276")))
    fig_Ea.add_vline(x=Ea, line_dash="dash", line_color="red", annotation_text="Ea actuelle")
    fig_Ea.update_layout(title="Sensibilité de k à l’énergie d’activation",
                         xaxis_title="Ea (kJ/mol)", yaxis_title="k (min⁻¹)",
                         yaxis_type="log", height=400)
    st.plotly_chart(fig_Ea, use_container_width=True)
    
    # Courbe k vs k0
    k0s = np.logspace(np.log10(k0*k0_range[0]), np.log10(k0*k0_range[1]), 40)
    ks_k0 = arrhenius(T_fixed, Ea, k0s)
    
    fig_k0 = go.Figure()
    fig_k0.add_trace(go.Scatter(x=k0s, y=ks_k0, mode="lines", line=dict(width=3, color="#27ae60")))
    fig_k0.add_vline(x=k0, line_dash="dash", line_color="red", annotation_text="k₀ actuel")
    fig_k0.update_layout(title=f"Sensibilité de k au facteur pré-exponentiel (T = {T_fixed} °C)",
                         xaxis_title="k₀", yaxis_title="k (min⁻¹)",
                         xaxis_type="log", yaxis_type="log", height=400)
    st.plotly_chart(fig_k0, use_container_width=True)
    
    # Diagramme d'Arrhenius
    st.subheader("Diagramme d’Arrhenius")
    Ts_arr = np.linspace(800, 1500, 30)
    inv_T = 1000 / (Ts_arr + 273)
    ln_k = np.log(arrhenius(Ts_arr, Ea, k0))
    
    fig_arr = go.Figure()
    fig_arr.add_trace(go.Scatter(x=inv_T, y=ln_k, mode="lines+markers", 
                                 line=dict(width=2.5, color="#c0392b")))
    fig_arr.update_layout(title="Diagramme d’Arrhenius (ln k vs 1/T)",
                          xaxis_title="1000/T (K⁻¹)", yaxis_title="ln k",
                          height=420)
    st.plotly_chart(fig_arr, use_container_width=True)
    show_interpretation("Diagramme d’Arrhenius", """
    **Lecture :**
    - La pente de la droite est égale à −Ea/R.
    - Plus la pente est forte (en valeur absolue), plus l’énergie d’activation est élevée.
    - Ce diagramme permet de vérifier la cohérence du modèle d’Arrhenius et d’extraire Ea expérimentalement.
    """)
    
    slope = -Ea * 1000 / 8.314
    st.caption(f"Pente théorique = -Ea/R = {slope:.1f} K")
    
    # ==================== EFFET DE LA TEMPÉRATURE ====================
    st.subheader("Effet de la température")
    st.markdown("Influence de la température sur la constante de vitesse et le temps de réaction.")
    
    T_min, T_max = st.slider("Plage de température (°C)", 700, 1600, (800, 1400), key="T_range_eff")
    target_alpha = st.slider("Conversion cible (%)", 50, 95, 80) / 100
    
    Ts_eff = np.linspace(T_min, T_max, 40)
    ks_eff = arrhenius(Ts_eff, Ea, k0)
    
    # Temps pour atteindre la conversion cible (ordre 1)
    t_target = -np.log(1 - target_alpha) / ks_eff
    
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=Ts_eff, y=ks_eff, mode="lines", name="k", 
                                  line=dict(width=3, color="#1a5276")))
    fig_temp.update_layout(title="Constante de vitesse en fonction de la température",
                           xaxis_title="Température (°C)", yaxis_title="k (min⁻¹)",
                           yaxis_type="log", height=400)
    st.plotly_chart(fig_temp, use_container_width=True)
    show_interpretation("Impact thermique sur la cinétique", """
    **Effet de la température :**
    - La constante de vitesse k augmente exponentiellement avec T (loi d’Arrhenius).
    - Une augmentation de 50–100 °C peut multiplier k par 2 à 10 selon la valeur de Ea.
    - Cet effet thermique est l’un des leviers les plus puissants pour accélérer une réaction.
    
    Attention : une température trop élevée peut aussi favoriser des réactions secondaires ou dégrader les réfractaires.
    """)
    
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(x=Ts_eff, y=t_target, mode="lines", name="Temps",
                                  line=dict(width=3, color="#e67e22")))
    fig_time.update_layout(title=f"Temps pour atteindre {target_alpha*100:.0f} % de conversion",
                           xaxis_title="Température (°C)", yaxis_title="Temps (min)",
                           yaxis_type="log", height=400)
    st.plotly_chart(fig_time, use_container_width=True)
    
    st.info("Une augmentation de température accélère fortement la réaction (effet exponentiel d’Arrhenius).")
    
    # ==================== CINÉTIQUE HÉTÉROGÈNE ====================
    st.subheader("Cinétique hétérogène (réaction solide-gaz)")
    st.markdown("Simulation d’une réaction du type : solide + gaz → produits")
    
    P_gas = st.slider("Pression partielle du gaz réactif (bar)", 0.1, 5.0, 1.0)
    n_order = st.slider("Ordre par rapport au gaz", 0.5, 2.0, 1.0, 0.1)
    alpha_max = st.slider("Conversion maximale simulée (%)", 50, 99, 90)
    
    # Modèle simple : dα/dt = k * P^n * (1-α)^m
    m_solid = 1.0  # ordre par rapport au solide
    t_het = np.linspace(0, tmax, 100)
    # Intégration numérique simple
    alpha_het = np.zeros_like(t_het)
    dt = t_het[1] - t_het[0]
    k_het = k * (P_gas ** n_order)
    for i in range(1, len(t_het)):
        rate = k_het * (1 - alpha_het[i-1])**m_solid
        alpha_het[i] = min(alpha_het[i-1] + rate * dt, alpha_max/100)
    
    fig_het = go.Figure(go.Scatter(x=t_het, y=alpha_het*100, mode="lines", 
                                   line=dict(width=3, color="#8e44ad")))
    fig_het.update_layout(title=f"Cinétique hétérogène (ordre gaz = {n_order})",
                          xaxis_title="Temps (min)", yaxis_title="Conversion (%)", height=420)
    st.plotly_chart(fig_het, use_container_width=True)
    
    st.caption("La vitesse dépend de la pression partielle du gaz et de la surface solide restante (1-α).")
    
    with st.expander("Mécanismes réactionnels typiques"):
        st.markdown("""
        **Exemples de mécanismes en métallurgie :**
        
        - **Réduction des oxydes de fer** :  
          Fe₂O₃ → Fe₃O₄ → FeO → Fe (étapes successives)
        
        - **Réduction carbothermique** :  
          MO + C → M + CO (contrôle souvent mixte chimique/diffusion)
        
        - **Grillage des sulfures** :  
          2MS + 3O₂ → 2MO + 2SO₂
        
        - **Désulfuration** :  
          CaO + [S] → CaS + [O]
        
        Les mécanismes peuvent être limités par la réaction chimique, la diffusion ou le transfert de masse.
        """)
    
    # ==================== MODÈLES CONTRACTING ====================
    st.subheader("Modèles Contracting")
    st.markdown("Modèles géométriques de contraction de l’interface réactionnelle.")
    
    model_contr = st.radio("Modèle", ["Contracting Volume (sphérique, 3D)", "Contracting Area (cylindrique, 2D)", "Comparaison"])
    
    k_contr = st.number_input("Constante de vitesse k (min⁻¹)", 0.001, 0.1, 0.015, format="%.3f", key="k_contr")
    t_contr = np.linspace(0, 120, 80)
    
    if model_contr == "Contracting Volume (sphérique, 3D)":
        # g(α) = 1 - (1-α)^{1/3}
        alpha_cv = 1 - (1 - k_contr * t_contr)**3
        alpha_cv = np.clip(alpha_cv, 0, 0.99)
        fig_cv = go.Figure(go.Scatter(x=t_contr, y=alpha_cv*100, mode="lines", line=dict(width=3, color="#1a5276")))
        fig_cv.update_layout(title="Contracting Volume – Interface sphérique",
                             xaxis_title="Temps (min)", yaxis_title="Conversion (%)", height=400)
        st.plotly_chart(fig_cv, use_container_width=True)
        st.latex(r"g(\alpha) = 1 - (1-\alpha)^{1/3}")
        st.caption("Typique des particules sphériques sous contrôle chimique.")
        
    elif model_contr == "Contracting Area (cylindrique, 2D)":
        # g(α) = 1 - (1-α)^{1/2}
        alpha_ca = 1 - (1 - k_contr * t_contr)**2
        alpha_ca = np.clip(alpha_ca, 0, 0.99)
        fig_ca = go.Figure(go.Scatter(x=t_contr, y=alpha_ca*100, mode="lines", line=dict(width=3, color="#27ae60")))
        fig_ca.update_layout(title="Contracting Area – Interface cylindrique",
                             xaxis_title="Temps (min)", yaxis_title="Conversion (%)", height=400)
        st.plotly_chart(fig_ca, use_container_width=True)
        st.latex(r"g(\alpha) = 1 - (1-\alpha)^{1/2}")
        st.caption("Typique des particules cylindriques ou des plaques sous contrôle chimique.")
        
    else:
        alpha_cv = 1 - (1 - k_contr * t_contr)**3
        alpha_ca = 1 - (1 - k_contr * t_contr)**2
        alpha_cv = np.clip(alpha_cv, 0, 0.99)
        alpha_ca = np.clip(alpha_ca, 0, 0.99)
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(x=t_contr, y=alpha_cv*100, mode="lines", name="Contracting Volume", line=dict(width=3)))
        fig_comp.add_trace(go.Scatter(x=t_contr, y=alpha_ca*100, mode="lines", name="Contracting Area", line=dict(width=3)))
        fig_comp.update_layout(title="Comparaison Contracting Volume vs Area",
                               xaxis_title="Temps (min)", yaxis_title="Conversion (%)", height=420)
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # ==================== MÉCANISMES DE NUCLÉATION ====================
    st.subheader("Mécanismes de nucléation")
    st.markdown("Modèles de nucléation et croissance (Avrami, Prout-Tompkins, etc.).")
    st.info("Explorez les différents modèles de nucléation-croissance ci-dessous.")
    
    with st.expander("Nucléation homogène – Explication", expanded=False):
        st.markdown(r"""
        **Nucléation homogène**
        
        La nucléation homogène se produit **dans le volume** de la phase mère, sans l’aide de surfaces, d’impuretés ou de défauts préexistants.
        
        **Caractéristiques :**
        - Nécessite une **sursaturation** (ou surfusion) importante
        - Barrière énergétique élevée (formation d’une interface)
        - Taille critique du germe : \( r^* = \frac{2\gamma}{\Delta G_v} \)
        - Fréquence de nucléation très sensible à la température et à la sursaturation
        
        **Énergie d’activation de formation d’un germe :**
        \[
        \Delta G^* = \frac{16\pi \gamma^3}{3 (\Delta G_v)^2}
        \]
        
        **En métallurgie :**
        - Rare dans les solides à cause de la présence de défauts
        - Plus fréquente dans les liquides ou les gaz sursaturés
        - Les modèles Avrami supposent souvent une nucléation aléatoire (proche de l’homogène) suivie d’une croissance
        
        **Différence avec la nucléation hétérogène :**
        - Hétérogène : se produit sur des surfaces, joints de grains, inclusions → barrière plus faible
        - Homogène : dans le volume → barrière plus élevée, nécessite une force motrice plus grande
        """)
    
    nuc_model = st.selectbox("Modèle de nucléation", 
        ["Avrami-Erofeev (n=2)", "Avrami-Erofeev (n=3)", "Prout-Tompkins", "Power law (n=2)", "Comparaison"])
    
    k_nuc = st.number_input("Constante k (min⁻¹)", 0.001, 0.08, 0.012, format="%.3f", key="k_nuc")
    t_nuc = np.linspace(0.1, 150, 80)
    
    if nuc_model == "Avrami-Erofeev (n=2)":
        alpha_n = 1 - np.exp(-(k_nuc * t_nuc)**2)
        fig_n = go.Figure(go.Scatter(x=t_nuc, y=alpha_n*100, mode="lines", line=dict(width=3)))
        fig_n.update_layout(title="Avrami-Erofeev n=2 (nucléation 2D)", height=400)
        st.plotly_chart(fig_n, use_container_width=True)
        st.latex(r"\alpha = 1 - \exp[-(kt)^2]")
        
    elif nuc_model == "Avrami-Erofeev (n=3)":
        alpha_n = 1 - np.exp(-(k_nuc * t_nuc)**3)
        fig_n = go.Figure(go.Scatter(x=t_nuc, y=alpha_n*100, mode="lines", line=dict(width=3)))
        fig_n.update_layout(title="Avrami-Erofeev n=3 (nucléation 3D)", height=400)
        st.plotly_chart(fig_n, use_container_width=True)
        st.latex(r"\alpha = 1 - \exp[-(kt)^3]")
        
    elif nuc_model == "Prout-Tompkins":
        alpha_n = 1 / (1 + np.exp(-k_nuc * (t_nuc - 60)))
        fig_n = go.Figure(go.Scatter(x=t_nuc, y=alpha_n*100, mode="lines", line=dict(width=3, color="#c0392b")))
        fig_n.update_layout(title="Prout-Tompkins (nucléation en chaîne)", height=400)
        st.plotly_chart(fig_n, use_container_width=True)
        st.caption("Modèle de nucléation autocatalytique / en chaîne.")
        
    elif nuc_model == "Power law (n=2)":
        alpha_n = (k_nuc * t_nuc)**2
        alpha_n = np.clip(alpha_n, 0, 0.95)
        fig_n = go.Figure(go.Scatter(x=t_nuc, y=alpha_n*100, mode="lines", line=dict(width=3)))
        fig_n.update_layout(title="Power law n=2", height=400)
        st.plotly_chart(fig_n, use_container_width=True)
        
    else:
        a2 = 1 - np.exp(-(k_nuc * t_nuc)**2)
        a3 = 1 - np.exp(-(k_nuc * t_nuc)**3)
        apt = 1 / (1 + np.exp(-k_nuc * (t_nuc - 60)))
        fig_comp_n = go.Figure()
        fig_comp_n.add_trace(go.Scatter(x=t_nuc, y=a2*100, mode="lines", name="Avrami n=2"))
        fig_comp_n.add_trace(go.Scatter(x=t_nuc, y=a3*100, mode="lines", name="Avrami n=3"))
        fig_comp_n.add_trace(go.Scatter(x=t_nuc, y=apt*100, mode="lines", name="Prout-Tompkins"))
        fig_comp_n.update_layout(title="Comparaison des modèles de nucléation", height=450)
        st.plotly_chart(fig_comp_n, use_container_width=True)
    
    # ==================== CROISSANCE CRISTALLINE ====================
    st.subheader("Analyse de la croissance cristalline")
    st.markdown("Modèles de croissance de germes (linéaire, parabolique, diffusion-limitée).")
    
    growth_type = st.selectbox("Type de croissance", 
        ["Linéaire (contrôle interfacial)", "Parabolique (diffusion)", "Comparaison"])
    
    G = st.number_input("Vitesse de croissance G (µm/min)", 0.01, 5.0, 0.3, key="G_growth")
    t_g = np.linspace(0, 60, 50)
    
    if growth_type == "Linéaire (contrôle interfacial)":
        r = G * t_g
        fig_g = go.Figure(go.Scatter(x=t_g, y=r, mode="lines", line=dict(width=3)))
        fig_g.update_layout(title="Croissance linéaire – r = G·t", xaxis_title="Temps (min)", 
                            yaxis_title="Rayon (µm)", height=380)
        st.plotly_chart(fig_g, use_container_width=True)
        st.caption("Typique d’un contrôle par la réaction à l’interface cristal/matrice.")
        
    elif growth_type == "Parabolique (diffusion)":
        r = np.sqrt(2 * G * t_g)   # approximation
        fig_g = go.Figure(go.Scatter(x=t_g, y=r, mode="lines", line=dict(width=3, color="#27ae60")))
        fig_g.update_layout(title="Croissance parabolique – r ∝ √t", xaxis_title="Temps (min)", 
                            yaxis_title="Rayon (µm)", height=380)
        st.plotly_chart(fig_g, use_container_width=True)
        st.caption("Typique d’une croissance limitée par la diffusion dans la matrice.")
        
    else:
        r_lin = G * t_g
        r_par = np.sqrt(2 * G * t_g)
        fig_gc = go.Figure()
        fig_gc.add_trace(go.Scatter(x=t_g, y=r_lin, mode="lines", name="Linéaire"))
        fig_gc.add_trace(go.Scatter(x=t_g, y=r_par, mode="lines", name="Parabolique"))
        fig_gc.update_layout(title="Comparaison croissance linéaire vs parabolique", height=400)
        st.plotly_chart(fig_gc, use_container_width=True)

# ==================== 5. DIFFUSION & TRANSFERT DE MASSE ====================
elif module == "6. Diffusion & Transfert de Masse":
    st.header(f"Phénomènes de Transport de Matière – {metal}")
    with st.expander("Explication scientifique du module", expanded=False):
        st.markdown("""
        **Objectif :** Identifier et simuler les limitations par le transport de matière.
        
        **Modèles :**
        - Diffusion solide (Fick) : transport dans le réseau cristallin.
        - Shrinking-core : décrit les réactions fluide-solide avec formation d’une couche de produit.
        - Couche limite : résistance au transfert dans le fluide.
        
        **Pourquoi ces modèles ?**
        - Ils correspondent aux régimes limitants classiquement observés en métallurgie extractive.
        
        **Limitations :**
        - Géométrie idéalisée (sphères, cylindres).
        - Paramètres (D, k_s, k_g) souvent difficiles à mesurer précisément.
        
        **Cas d’utilisation :** Diagnostic du régime limitant, optimisation de la taille des particules ou de l’agitation.
        """)
    params = get_metal_params(metal)
    mineral = st.selectbox("Minerai", ["Hématite", "Magnétite", "Pyrolusite", "Chalcopyrite", "Sphalérite", "Bauxite (Gibbsite)"], key="min_diff")
    ore = get_ore_constants(mineral)
    st.info(f"Minerai : {mineral} → facteur de diffusion ×{ore['D_factor']:.2f}")
    
    with st.expander("Explication des mécanismes de diffusion", expanded=True):
        st.markdown(r"""
        **Principaux mécanismes de diffusion en métallurgie :**
        
        1. **Diffusion solide (Fick)**  
           Transport d’atomes ou d’ions à l’intérieur du solide.  
           Loi de Fick : \(\displaystyle \frac{\partial C}{\partial t} = D \nabla^2 C\)  
           Typique des réactions solide-solide ou de la croissance de couches d’oxyde.
        
        2. **Diffusion dans la couche de cendre (shrinking core)**  
           Après réaction, une couche de produit solide se forme.  
           Les réactifs gazeux doivent diffuser à travers cette couche.  
           Souvent limitante à haute conversion.
        
        3. **Couche limite / Film fluide**  
           Résistance au transfert de masse dans le fluide autour de la particule.  
           Flux : \(N = k_g (C_b - C_s)\)  
           Dépend de l’agitation et de la taille des particules.
        
        4. **Diffusion gazeuse dans les pores**  
           Importante pour les minerais poreux ou les catalyseurs.  
           Peut être moléculaire ou de Knudsen selon la taille des pores.
        
        **Comment identifier le mécanisme limitant ?**  
        - Contrôle chimique → temps ~ \(1 - (1-\alpha)^{1/3}\)  
        - Diffusion dans la couche → temps ~ \(1 - 3(1-\alpha)^{2/3} + 2(1-\alpha)\)  
        - Couche limite → dépendance forte à l’agitation
        """)
    
    mechanism = st.radio("Mécanisme limitant", 
        ["Diffusion solide (Fick)", 
         "Limitation chimique (réaction de surface)", 
         "Couche limite / Film (transfert de masse)",
         "Shrinking-core complet",
         "Comparaison des régimes"])
    
    T = st.slider("Température (°C)", 700, 1400, 980)
    time_h = st.slider("Temps (h)", 0.5, 24., 4.)
    
    if mechanism == "Diffusion solide (Fick)":
        D = arrhenius(T, params["D_Ea"], params["D0"] * ore["D_factor"])
        st.latex(r"\frac{\partial C}{\partial t} = D \nabla^2 C")
        x = np.linspace(0, 3e-3, 80)
        C = 1 - 0.8 * np.array([erf(xi / (2*np.sqrt(D*time_h*3600))) for xi in x])
        fig = go.Figure(go.Scatter(x=x*1000, y=C, mode="lines", line=dict(width=3)))
        fig.update_layout(title="Profil de concentration – Diffusion solide (Fick)",
                          xaxis_title="Distance (mm)", yaxis_title="Concentration relative", height=420)
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Coefficient de diffusion D", f"{D:.2e} m²/s")
        st.info("Limitation par diffusion dans le solide. La vitesse dépend de √t.")
        
    elif mechanism == "Limitation chimique (réaction de surface)":
        st.markdown("**Contrôle par la cinétique chimique de surface**")
        st.latex(r"t^* = 1 - (1-\alpha)^{1/3}")
        alpha = np.linspace(0.05, 0.95, 40)
        t_rel = 1 - (1-alpha)**(1/3)
        fig = go.Figure(go.Scatter(x=alpha*100, y=t_rel, mode="lines+markers", line=dict(width=3, color="#c0392b")))
        fig.update_layout(title="Temps relatif – Contrôle chimique (shrinking core)",
                          xaxis_title="Conversion (%)", yaxis_title="Temps relatif t*", height=420)
        st.plotly_chart(fig, use_container_width=True)
        st.info("La vitesse est limitée par la réaction chimique à la surface. Indépendante de la taille des particules (dans une certaine mesure).")
        
    elif mechanism == "Couche limite / Film (transfert de masse)":
        st.markdown("**Contrôle par le film de diffusion (couche limite)**")
        kg = st.slider("Coefficient de transfert de masse kg (m/s)", 0.005, 0.1, 0.025, 0.005)
        delta_c = st.slider("Écart de concentration (kmol/m³)", 0.1, 2.0, 0.4)
        flux = kg * delta_c
        st.metric("Flux de masse", f"{flux:.4f} kmol/m²·s")
        
        # Courbe flux vs kg
        kgs = np.linspace(0.005, 0.1, 40)
        fluxes = kgs * delta_c
        fig_film = go.Figure(go.Scatter(x=kgs, y=fluxes, mode="lines", line=dict(width=3, color="#27ae60")))
        fig_film.add_vline(x=kg, line_dash="dash", line_color="red", annotation_text="kg actuel")
        fig_film.update_layout(title="Flux de masse en fonction de kg (couche limite)",
                               xaxis_title="kg (m/s)", yaxis_title="Flux (kmol/m²·s)", height=400)
        st.plotly_chart(fig_film, use_container_width=True)
        st.info("Limitation par le transport dans le film fluide autour de la particule. kg dépend de l’agitation et de la taille des particules.")
        
    elif mechanism == "Shrinking-core complet":
        st.subheader("Modèle Shrinking-Core")
        st.markdown("Simulation des trois régimes classiques du modèle du cœur rétrécissant.")
        
        regime = st.selectbox("Régime limitant", 
            ["Contrôle chimique", "Diffusion dans la couche de cendre", "Contrôle par le film"])
        
        R = st.slider("Rayon initial de particule (mm)", 0.1, 5.0, 1.0)
        k_s = st.number_input("Constante de surface k_s (m/s)", 1e-6, 1e-3, 1e-5, format="%.1e")
        D_e = st.number_input("Diffusivité effective D_e (m²/s)", 1e-10, 1e-6, 1e-8, format="%.1e")
        k_g = st.number_input("Coefficient de film k_g (m/s)", 1e-4, 1e-2, 1e-3, format="%.1e")
        
        alpha = np.linspace(0.05, 0.95, 50)
        t_chem = (R/1000) / k_s * (1 - (1-alpha)**(1/3))
        t_ash = (R/1000)**2 / (6*D_e) * (1 - 3*(1-alpha)**(2/3) + 2*(1-alpha))
        t_film = (R/1000) / (3*k_g) * alpha
        
        if regime == "Contrôle chimique":
            t = t_chem
            title = "Contrôle chimique"
        elif regime == "Diffusion dans la couche de cendre":
            t = t_ash
            title = "Diffusion dans la couche de cendre"
        else:
            t = t_film
            title = "Contrôle par le film"
        
        fig_sc = go.Figure(go.Scatter(x=t*60, y=alpha*100, mode="lines", line=dict(width=3)))
        fig_sc.update_layout(title=f"Shrinking-core – {title}",
                             xaxis_title="Temps (min)", yaxis_title="Conversion (%)", height=420)
        st.plotly_chart(fig_sc, use_container_width=True)
        
        st.caption(f"Rayon de particule : {R} mm")
        
    else:
        # Comparaison des régimes
        st.subheader("Comparaison des régimes limitants")
        alpha = np.linspace(0.1, 0.9, 30)
        t_chem = 1 - (1-alpha)**(1/3)
        t_diff = 1 - 3*(1-alpha)**(2/3) + 2*(1-alpha)   # diffusion dans la couche de cendre
        t_film = alpha   # approximation linéaire pour le film
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(x=alpha*100, y=t_chem, mode="lines", name="Contrôle chimique", line=dict(width=2.5)))
        fig_comp.add_trace(go.Scatter(x=alpha*100, y=t_diff, mode="lines", name="Diffusion solide/couche", line=dict(width=2.5)))
        fig_comp.add_trace(go.Scatter(x=alpha*100, y=t_film, mode="lines", name="Couche limite (film)", line=dict(width=2.5)))
        fig_comp.update_layout(title="Temps relatif selon le régime limitant",
                               xaxis_title="Conversion (%)", yaxis_title="Temps relatif", height=450)
        st.plotly_chart(fig_comp, use_container_width=True)
        st.caption("Chaque régime présente une signature différente du temps de réaction en fonction de la conversion.")
    
    # ==================== DIFFUSION GAZEUSE ====================
    if mechanism == "Diffusion solide (Fick)":
        pass  # already handled
    elif mechanism == "Shrinking-core complet":
        pass
    else:
        st.subheader("Modèle de diffusion gazeuse")
        st.markdown("Diffusion d’un gaz réactif dans les pores ou la couche limite.")
        
        D_gas = st.number_input("Diffusivité gazeuse D_g (m²/s)", 1e-6, 1e-4, 1e-5, format="%.1e")
        L = st.slider("Épaisseur de couche / pore (mm)", 0.1, 5.0, 1.0)
        delta_C = st.slider("Écart de concentration (mol/m³)", 0.1, 10., 2.0)
        
        flux_g = D_gas * delta_C / (L/1000)
        st.metric("Flux gazeux", f"{flux_g:.2e} mol/m²·s")
        
        # Courbe flux vs épaisseur
        Ls = np.linspace(0.1, 5, 40)
        fluxes_g = D_gas * delta_C / (Ls/1000)
        fig_gas = go.Figure(go.Scatter(x=Ls, y=fluxes_g, mode="lines", line=dict(width=3)))
        fig_gas.add_vline(x=L, line_dash="dash", line_color="red")
        fig_gas.update_layout(title="Flux de diffusion gazeuse vs épaisseur",
                              xaxis_title="Épaisseur (mm)", yaxis_title="Flux (mol/m²·s)", height=380)
        st.plotly_chart(fig_gas, use_container_width=True)
        st.caption("Loi de Fick stationnaire : \( N = D_g \cdot \Delta C / L \)")
    
    # ==================== DÉFAUTS CRISTALLINS ====================
    st.subheader("Analyse des défauts cristallins")
    st.markdown("Influence des défauts sur la diffusion et la réactivité.")
    
    defect_type = st.selectbox("Type de défaut", 
        ["Lacunes (défauts ponctuels)", "Dislocations", "Joints de grains", "Comparaison"])
    
    T_def = st.slider("Température (°C)", 400, 1200, 800, key="T_def")
    density_def = st.slider("Densité de défauts (relative)", 0.1, 10., 1.0)
    
    # Coefficient de diffusion effectif augmenté par les défauts
    D_base = arrhenius(T_def, 150, 1e-4)
    
    if defect_type == "Lacunes (défauts ponctuels)":
        D_eff = D_base * (1 + 0.5 * density_def)
        st.metric("D effectif", f"{D_eff:.2e} m²/s")
        st.info("Les lacunes facilitent la diffusion substitutionnelle. Plus la concentration en lacunes est élevée, plus D augmente.")
        
    elif defect_type == "Dislocations":
        D_eff = D_base * (1 + 2.0 * density_def)
        st.metric("D effectif", f"{D_eff:.2e} m²/s")
        st.info("Les dislocations agissent comme des courts-circuits de diffusion (pipe diffusion). Effet marqué à basse température.")
        
    elif defect_type == "Joints de grains":
        D_eff = D_base * (1 + 5.0 * density_def)
        st.metric("D effectif", f"{D_eff:.2e} m²/s")
        st.info("Les joints de grains sont des chemins de diffusion rapide. Importants dans les matériaux polycristallins à basse température.")
        
    else:
        factors = [1 + 0.5*density_def, 1 + 2.0*density_def, 1 + 5.0*density_def]
        labels = ["Lacunes", "Dislocations", "Joints de grains"]
        fig_def = go.Figure(go.Bar(x=labels, y=factors, marker_color=["#3498db", "#e67e22", "#c0392b"]))
        fig_def.update_layout(title="Facteur d’augmentation de D selon le type de défaut",
                              yaxis_title="Facteur multiplicatif", height=380)
        st.plotly_chart(fig_def, use_container_width=True)
        st.caption("Les joints de grains et les dislocations accélèrent fortement la diffusion à basse température.")

# ==================== 6. OPTIMISATION Q/K & RÉCUPÉRATION ====================
elif module == "7. Optimisation Q/K & Récupération":
    st.header(f"Optimisation Q/K – {metal}")
    params = get_metal_params(metal)
    mineral = st.selectbox("Minerai", ["Hématite", "Magnétite", "Pyrolusite", "Chalcopyrite", "Sphalérite", "Bauxite (Gibbsite)"], key="min_qk")
    ore = get_ore_constants(mineral)
    st.info(f"Minerai : {mineral} → facteur de récupération ×{ore['rec_factor']:.2f}")
    
    qk = st.slider("Q/K actuel", 0.05, 1.8, 0.40, 0.05)
    
    base_rec = params["base_rec"] * ore["rec_factor"]
    rec = base_rec * (1.15 - 0.6*qk) if qk < 1 else base_rec * (0.7 - 0.3*(qk-1))
    rec = np.clip(rec, 35, 99)
    st.metric("Récupération estimée", f"{rec:.1f} %")
    
    if qk < 1:
        st.success(f"Q/K = {qk:.2f} < 1 → Zone favorable")
    else:
        st.error(f"Q/K = {qk:.2f} ≥ 1 → Zone défavorable")
    
    qk_vals = np.linspace(0.05, 1.8, 50)
    rec_vals = [np.clip(base_rec * (1.15 - 0.6*q if q < 1 else 0.7 - 0.3*(q-1)), 35, 99) for q in qk_vals]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=qk_vals, y=rec_vals, mode="lines", name="Récupération",
                             line=dict(color="#1a5276", width=3)))
    fig.add_vline(x=1.0, line_dash="dash", line_color="red", line_width=2,
                  annotation_text="Limite Q/K = 1", annotation_position="top")
    fig.add_vrect(x0=0, x1=1, fillcolor="green", opacity=0.08, line_width=0)
    fig.add_vrect(x0=1, x1=2, fillcolor="red", opacity=0.08, line_width=0)
    fig.update_layout(title="Courbe de récupération avec limite Q/K = 1",
                      xaxis_title="Ratio Q/K", yaxis_title="Récupération (%)", height=450)
    st.plotly_chart(fig, use_container_width=True)

# ==================== 7. BILANS ÉNERGÉTIQUES & FINANCIERS ====================
elif module == "11. Bilans Énergétiques & Financiers":
    st.header("Optimisation Énergétique & Analyse Financière")
    show_market_data()
    
    energy = st.slider("Énergie (MWh/t)", 1.5, 14.0, 3.6, 0.1)
    cost_mwh = st.number_input("Coût MWh (FCFA)", 72000, step=2000)
    selling = st.number_input("Prix vente (FCFA/t)", 510000, step=10000)
    other = st.number_input("Autres coûts (FCFA/t)", 155000, step=5000)
    inv_m = st.number_input("Investissement (M FCFA)", 3800., step=100.)
    prod = st.number_input("Production annuelle (t)", 42000)
    life = st.number_input("Durée (ans)", 12, 20, 15)
    disc = st.slider("Taux actualisation %", 8., 13., 10.) / 100
    
    e_cost = energy * cost_mwh
    total = e_cost + other
    margin = selling - total
    acf = margin * prod
    inv = inv_m * 1e6
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Coût énergie", f"{e_cost:,.0f}")
    c2.metric("Marge / t", f"{margin:,.0f}")
    if acf > 0:
        c3.metric("Retour investissement", f"{inv/acf:.1f} ans")
    
    # Bouton téléchargement
    results = pd.DataFrame({
        "Indicateur": ["Énergie (MWh/t)", "Coût énergie (FCFA/t)", "Marge (FCFA/t)", "VAN estimée (M FCFA)"],
        "Valeur": [energy, e_cost, margin, (acf * life - inv)/1e6]
    })
    st.download_button(
        label="Télécharger les résultats (CSV)",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="resultats_financiers.csv",
        mime="text/csv"
    )
    
    if st.button("Courbe VAN annuelle"):
        years = list(range(life+1))
        van_list = [-inv]
        cum = -inv
        for y in range(1, life+1):
            cf = acf + (inv*0.08 if y == life else 0)
            cum += cf / (1+disc)**y
            van_list.append(cum)
        
        fig = go.Figure(go.Scatter(x=years, y=np.array(van_list)/1e6, mode="lines+markers",
                                   line=dict(color="#27ae60", width=3)))
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(title="VAN cumulée par année", xaxis_title="Année", 
                          yaxis_title="VAN (M FCFA)", height=450)
        st.plotly_chart(fig, use_container_width=True)
        st.metric("VAN finale", f"{van_list[-1]/1e6:,.1f} M FCFA")

# ==================== 8. THERMODYNAMIQUE DES SCORIES ====================
elif module == "8. Thermodynamique des Scories":
    st.header("Thermodynamique des Scories")
    with st.expander("Explication scientifique du module", expanded=False):
        st.markdown("""
        **Objectif :** Caractériser le laitier (basicité, liquidus, viscosité, activités).
        
        **Paramètres :**
        - Basicité (CaO/SiO₂) : indique le caractère acide ou basique et influence la viscosité et la capacité d’absorption des impuretés.
        - Teneurs en Al₂O₃, MgO, FeO, MnO : modifient le réseau silicaté et donc la viscosité.
        
        **Modèles de viscosité :**
        - Urbain / Riboud / Iida : modèles empiriques ou semi-empiriques basés sur la composition.
        - Eyring / Arrhenius : modèles activés décrivant la dépendance en température.
        
        **Limitations :**
        - Les modèles empiriques sont valables dans des domaines de composition limités.
        - Ils ne remplacent pas une mesure expérimentale ou un calcul thermodynamique complet (FactSage, etc.).
        
        **Cas d’utilisation :** Estimation rapide de la fluidité, comparaison de compositions de laitier, aide à la conduite de four.
        """)
    st.markdown("Basicité, liquidus, activités des oxydes et viscosité.")

    c1, c2, c3 = st.columns(3)
    with c1:
        sio2 = st.slider("SiO₂ (%)", 20., 50., 35.)
        cao = st.slider("CaO (%)", 15., 55., 40.)
    with c2:
        al2o3 = st.slider("Al₂O₃ (%)", 2., 20., 8.)
        mgo = st.slider("MgO (%)", 0., 15., 6.)
    with c3:
        mno = st.slider("MnO (%)", 0., 15., 3.)
        feo = st.slider("FeO (%)", 0., 20., 2.)

    total = sio2 + cao + al2o3 + mgo + mno + feo
    if abs(total - 100) > 5:
        st.warning(f"Somme des oxydes = {total:.1f} %")

    B2 = cao / sio2 if sio2 > 0 else 0
    B4 = (cao + mgo) / (sio2 + al2o3) if (sio2 + al2o3) > 0 else 0
    optical = (cao + 0.5*mgo + mno) / (sio2 + 0.5*al2o3) if (sio2 + al2o3) > 0 else 0

    st.subheader("Indices de basicité")
    b1, b2, b3 = st.columns(3)
    b1.metric("B2 = CaO/SiO₂", f"{B2:.2f}")
    b2.metric("B4", f"{B4:.2f}")
    b3.metric("Basicité optique", f"{optical:.2f}")

    if B2 < 0.8:
        st.info("Laitier acide")
    elif B2 < 1.2:
        st.info("Laitier neutre")
    else:
        st.success("Laitier basique")

    T_liq = 1400 + 8*(sio2-35) - 6*(cao-40) + 4*al2o3 - 3*mgo + 2*feo
    T_liq = np.clip(T_liq, 1150, 1650)
    st.metric("Température de liquidus estimée", f"{T_liq:.0f} °C")

    # Activités
    st.subheader("Activités des oxydes")
    moles = {
        "SiO2": sio2/60.08, "CaO": cao/56.08, "Al2O3": al2o3/101.96,
        "MgO": mgo/40.3, "MnO": mno/70.94, "FeO": feo/71.84
    }
    total_moles = sum(moles.values())
    x = {k: v/total_moles for k, v in moles.items()} if total_moles > 0 else {}
    
    a_sio2 = x.get("SiO2", 0) * np.exp(-2.5 * B2)
    a_cao = x.get("CaO", 0) * np.exp(1.8 * (B2 - 1))
    a_feo = x.get("FeO", 0) * 0.8
    a_mno = x.get("MnO", 0) * 0.9
    
    act_df = pd.DataFrame({
        "Oxyde": ["SiO₂", "CaO", "FeO", "MnO"],
        "x": [round(x.get("SiO2",0),3), round(x.get("CaO",0),3), round(x.get("FeO",0),3), round(x.get("MnO",0),3)],
        "a": [round(a_sio2,3), round(a_cao,3), round(a_feo,3), round(a_mno,3)]
    })
    st.dataframe(act_df, hide_index=True)
    
    # Bouton téléchargement activités
    st.download_button(
        label="Télécharger activités des oxydes (CSV)",
        data=act_df.to_csv(index=False).encode("utf-8"),
        file_name="activites_oxydes.csv",
        mime="text/csv"
    )

    # Viscosité (modèle Urbain simplifié)
    st.subheader("Viscosité du laitier")
    T_visc = st.slider("Température pour viscosité (°C)", 1300, 1600, int(T_liq+50))
    B_urbain = cao / (sio2 + al2o3) if (sio2 + al2o3) > 0 else 1
    log_visc = -3.5 + 4500/(T_visc+273) + 1.2*(1 - B_urbain)
    viscosity = 10**log_visc
    st.metric("Viscosité simulée", f"{viscosity:.2f} Pa·s")
    
    # Courbes de viscosité
    st.subheader("Courbes de viscosité")
    T_range_visc = np.linspace(1300, 1600, 40)
    visc_curve = 10**(-3.5 + 4500/(T_range_visc+273) + 1.2*(1 - B_urbain))
    
    fig_visc = go.Figure()
    fig_visc.add_trace(go.Scatter(x=T_range_visc, y=visc_curve, mode="lines", 
                                  name="Viscosité", line=dict(width=3, color="#1a5276")))
    fig_visc.add_vline(x=T_visc, line_dash="dash", line_color="red", 
                       annotation_text="T actuelle")
    fig_visc.update_layout(title="Viscosité en fonction de la température",
                           xaxis_title="Température (°C)", yaxis_title="Viscosité (Pa·s)",
                           height=400)
    st.plotly_chart(fig_visc, use_container_width=True)
    
    # Courbe viscosité vs basicité
    B_range = np.linspace(0.5, 1.8, 30)
    visc_B = 10**(-3.5 + 4500/(T_visc+273) + 1.2*(1 - B_range))
    fig_B = go.Figure()
    fig_B.add_trace(go.Scatter(x=B_range, y=visc_B, mode="lines", line=dict(width=3, color="#27ae60")))
    fig_B.add_vline(x=B_urbain, line_dash="dash", line_color="red", annotation_text="Votre basicité")
    fig_B.update_layout(title="Viscosité en fonction de la basicité",
                        xaxis_title="Basicité (CaO/(SiO₂+Al₂O₃))", yaxis_title="Viscosité (Pa·s)",
                        height=380)
    st.plotly_chart(fig_B, use_container_width=True)
    
    # ==================== MODÈLES AVANCÉS ====================
    st.subheader("Modèles de viscosité avancés")
    st.markdown("Comparaison des modèles Urbain, Riboud et Iida.")
    
    model_choice = st.selectbox("Modèle à afficher", 
        ["Urbain simplifié", "Riboud", "Iida", "Comparaison des 3 modèles"])
    
    T_visc_adv = st.slider("Température pour modèles avancés (°C)", 1300, 1650, 1450, key="T_adv")
    
    # Calculs des modèles
    def viscosity_urbain(T_c, B):
        return 10**(-3.5 + 4500/(T_c+273) + 1.2*(1 - B))
    
    def viscosity_riboud(T_c, sio2, cao, al2o3, mgo):
        # Approximation Riboud
        X = sio2 + al2o3
        Y = cao + mgo
        A = np.exp(-17.5 + 0.35*X - 0.15*Y)
        B_r = 6000 + 40*X - 20*Y
        return A * np.exp(B_r / (T_c+273))
    
    def viscosity_iida(T_c, sio2, cao, al2o3):
        # Approximation Iida
        log_eta = -2.8 + 3800/(T_c+273) + 0.8*(sio2/40) - 0.4*(cao/40) + 0.3*(al2o3/10)
        return 10**log_eta
    
    B_u = cao / (sio2 + al2o3) if (sio2 + al2o3) > 0 else 1
    
    if model_choice == "Urbain simplifié":
        eta = viscosity_urbain(T_visc_adv, B_u)
        st.metric("Viscosité Urbain", f"{eta:.3f} Pa·s")
    elif model_choice == "Riboud":
        eta = viscosity_riboud(T_visc_adv, sio2, cao, al2o3, mgo)
        st.metric("Viscosité Riboud", f"{eta:.3f} Pa·s")
    elif model_choice == "Iida":
        eta = viscosity_iida(T_visc_adv, sio2, cao, al2o3)
        st.metric("Viscosité Iida", f"{eta:.3f} Pa·s")
    else:
        # Comparaison
        Ts = np.linspace(1300, 1650, 40)
        eta_u = viscosity_urbain(Ts, B_u)
        eta_r = viscosity_riboud(Ts, sio2, cao, al2o3, mgo)
        eta_i = viscosity_iida(Ts, sio2, cao, al2o3)
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(x=Ts, y=eta_u, mode="lines", name="Urbain", line=dict(width=2.5)))
        fig_comp.add_trace(go.Scatter(x=Ts, y=eta_r, mode="lines", name="Riboud", line=dict(width=2.5)))
        fig_comp.add_trace(go.Scatter(x=Ts, y=eta_i, mode="lines", name="Iida", line=dict(width=2.5)))
        fig_comp.update_layout(title="Comparaison des modèles de viscosité",
                               xaxis_title="Température (°C)", yaxis_title="Viscosité (Pa·s)",
                               height=450, yaxis_type="log")
        st.plotly_chart(fig_comp, use_container_width=True)
        
        st.caption("Les modèles avancés (Riboud, Iida, Urbain complet) tiennent compte des fractions molaires de tous les oxydes et de coefficients d’interaction spécifiques.")
    
    # ==================== ANALYSE DÉTAILLÉE DE LA VISCOSITÉ ====================
    st.subheader("Analyse détaillée de la viscosité")
    
    with st.expander("Interprétation de la viscosité", expanded=True):
        st.markdown("""
        **Plages de viscosité typiques pour les laitiers :**
        - **< 0,3 Pa·s** : très fluide → excellente coulée, bonne séparation métal/laitier
        - **0,3 – 0,8 Pa·s** : fluide → conditions normales de travail
        - **0,8 – 1,5 Pa·s** : limite → risque de problèmes de coulée
        - **> 1,5 Pa·s** : visqueux → mauvaise coulée, inclusions, pertes de métal
        
        **Facteurs influençant la viscosité :**
        - **Température** : effet très fort (loi d’Arrhenius)
        - **Basicité** : les laitiers basiques sont généralement moins visqueux
        - **Al₂O₃** : augmente la viscosité (réseau)
        - **MgO, CaO** : diminuent la viscosité (modificateurs de réseau)
        - **FeO, MnO** : réduisent fortement la viscosité
        """)
    
    # Sensibilité à la température
    st.write("**Sensibilité à la température**")
    T_sens = np.linspace(1350, 1600, 30)
    eta_sens = 10**(-3.5 + 4500/(T_sens+273) + 1.2*(1 - B_urbain))
    fig_sens = go.Figure(go.Scatter(x=T_sens, y=eta_sens, mode="lines+markers", line=dict(width=2.5)))
    fig_sens.add_hline(y=0.5, line_dash="dash", line_color="green", annotation_text="Seuil fluide")
    fig_sens.add_hline(y=1.0, line_dash="dash", line_color="orange", annotation_text="Limite")
    fig_sens.update_layout(title="Évolution de la viscosité avec la température",
                           xaxis_title="Température (°C)", yaxis_title="Viscosité (Pa·s)",
                           yaxis_type="log", height=400)
    st.plotly_chart(fig_sens, use_container_width=True)
    show_interpretation("Viscosité vs Température", """
    **Interprétation technique :**
    - La viscosité diminue fortement avec la température (dépendance exponentielle type Arrhenius/Eyring).
    - En dessous de 0,5 Pa·s : laitier fluide, bonne coulée et séparation métal/laitier.
    - Au-dessus de 1 Pa·s : risque de problèmes de coulée, inclusions et pertes de métal.
    
    Une élévation de 50–100 °C peut diviser la viscosité par 2 ou plus.
    """)
    
    # ==================== IMPACT DE LA BASICITÉ SUR LA FLUIDITÉ ====================
    st.subheader("Impact de la basicité sur la fluidité")
    st.markdown("Relation entre l’indice de basicité et la viscosité du laitier.")
    
    T_bas = st.slider("Température d’analyse (°C)", 1400, 1600, 1500, key="T_bas")
    B_range = np.linspace(0.6, 1.8, 40)
    eta_bas = 10**(-3.5 + 4500/(T_bas+273) + 1.2*(1 - B_range))
    
    fig_bas = go.Figure()
    fig_bas.add_trace(go.Scatter(x=B_range, y=eta_bas, mode="lines", line=dict(width=3, color="#1a5276")))
    fig_bas.add_vline(x=B2, line_dash="dash", line_color="red", annotation_text="Votre basicité")
    fig_bas.add_hline(y=0.5, line_dash="dot", line_color="green")
    fig_bas.update_layout(title=f"Viscosité en fonction de la basicité (T = {T_bas} °C)",
                          xaxis_title="Basicité CaO/SiO₂", yaxis_title="Viscosité (Pa·s)",
                          yaxis_type="log", height=420)
    st.plotly_chart(fig_bas, use_container_width=True)
    show_interpretation("Impact de la basicité", """
    **Interprétation :**
    - Une basicité plus élevée (plus de CaO) casse le réseau silicaté et diminue la viscosité.
    - L’effet est particulièrement marqué à basse température.
    - Une basicité trop faible conduit à un laitier visqueux difficile à couler.
    
    Zone typique de travail : basicité 1,0 – 1,4 pour un bon compromis fluidité / capacité d’absorption des impuretés.
    """)
    
    if B2 < 0.9:
        st.warning("Basicité faible → viscosité plus élevée → fluidité réduite")
    elif B2 < 1.3:
        st.info("Basicité intermédiaire → fluidité correcte")
    else:
        st.success("Basicité élevée → viscosité plus faible → meilleure fluidité")
    
    st.caption("En général, une augmentation de la basicité diminue la viscosité des laitiers silicatés (effet de modification du réseau).")
    
    # ==================== RHÉOLOGIE DE LA SCORIE ====================
    st.subheader("Rhéologie de la scorie")
    st.markdown("Comportement rhéologique et effets spécifiques des oxydes.")
    
    with st.expander("Définition des minerais principaux", expanded=False):
        st.markdown("""
        **Minerais et métaux associés :**
        - **Hématite (Fe₂O₃)** : principal minerai de fer. Réduction relativement facile.
        - **Magnétite (Fe₃O₄)** : minerai de fer à structure spinelle. Cinétique légèrement plus lente.
        - **Pyrolusite (MnO₂)** : principal minerai de manganèse. Bonne réactivité.
        - **Chalcopyrite (CuFeS₂)** : principal minerai de cuivre. Nécessite des conditions oxydantes.
        - **Sphalérite (ZnS)** : principal minerai de zinc.
        - **Bauxite (Gibbsite Al(OH)₃)** : principal minerai d’aluminium. Procédé Bayer.
        """)
    
    # Effet de l'alumine
    st.write("**Rôle de l’alumine (Al₂O₃)**")
    al2o3_range = np.linspace(2, 20, 30)
    # Al2O3 augmente la viscosité
    eta_al = 10**(-3.5 + 4500/(T_bas+273) + 1.2*(1 - B_urbain) + 0.04*(al2o3_range - 8))
    fig_al = go.Figure(go.Scatter(x=al2o3_range, y=eta_al, mode="lines", line=dict(width=3, color="#e74c3c")))
    fig_al.add_vline(x=al2o3, line_dash="dash", line_color="black", annotation_text="Al₂O₃ actuel")
    fig_al.update_layout(title="Effet de l’alumine sur la viscosité",
                         xaxis_title="Al₂O₃ (%)", yaxis_title="Viscosité (Pa·s)", height=380)
    st.plotly_chart(fig_al, use_container_width=True)
    st.warning("L’alumine augmente la viscosité (renforce le réseau silicaté).")
    
    # Effet de MgO
    st.write("**Effet du MgO**")
    mgo_range = np.linspace(0, 15, 30)
    # MgO diminue la viscosité
    eta_mgo = 10**(-3.5 + 4500/(T_bas+273) + 1.2*(1 - B_urbain) - 0.03*(mgo_range - 6))
    fig_mgo = go.Figure(go.Scatter(x=mgo_range, y=eta_mgo, mode="lines", line=dict(width=3, color="#27ae60")))
    fig_mgo.add_vline(x=mgo, line_dash="dash", line_color="black", annotation_text="MgO actuel")
    fig_mgo.update_layout(title="Effet du MgO sur la viscosité",
                          xaxis_title="MgO (%)", yaxis_title="Viscosité (Pa·s)", height=380)
    st.plotly_chart(fig_mgo, use_container_width=True)
    st.success("Le MgO diminue la viscosité (modificateur de réseau, améliore la fluidité).")
    
    st.info("""
    **Résumé rhéologique :**
    - Al₂O₃ → augmente la viscosité
    - MgO et CaO → diminuent la viscosité
    - FeO et MnO → réduisent fortement la viscosité
    - La température a l’effet le plus important
    """)
    
    # ==================== VISCOSITÉ vs TEMPÉRATURE + EFFET CaO ====================
    st.subheader("Viscosité en fonction de la température et effet du CaO")
    
    T_cao = np.linspace(1350, 1620, 40)
    cao_levels = [30, 40, 50]
    
    fig_cao = go.Figure()
    for cao_val in cao_levels:
        B_temp = cao_val / sio2 if sio2 > 0 else 1
        eta_t = 10**(-3.5 + 4500/(T_cao+273) + 1.2*(1 - B_temp))
        fig_cao.add_trace(go.Scatter(x=T_cao, y=eta_t, mode="lines", name=f"CaO = {cao_val} %",
                                     line=dict(width=2.5)))
    
    # Courbe actuelle
    eta_current = 10**(-3.5 + 4500/(T_cao+273) + 1.2*(1 - B_urbain))
    fig_cao.add_trace(go.Scatter(x=T_cao, y=eta_current, mode="lines", name="Votre composition",
                                 line=dict(width=3, dash="dash", color="black")))
    
    fig_cao.update_layout(title="Viscosité vs Température pour différentes teneurs en CaO",
                          xaxis_title="Température (°C)", yaxis_title="Viscosité (Pa·s)",
                          yaxis_type="log", height=450)
    st.plotly_chart(fig_cao, use_container_width=True)
    
    st.success("""
    **Effet du CaO :**
    - Une augmentation de CaO diminue la viscosité à température constante
    - Le CaO agit comme modificateur de réseau (casse les chaînes silicatées)
    - L’effet est plus marqué à basse température
    """)
    
    st.caption("La température reste le paramètre le plus influent sur la viscosité (dépendance exponentielle).")
    
    # ==================== MODÈLE D'EYRING ====================
    st.subheader("Modèle de viscosité d’Eyring")
    st.markdown(r"""
    Le modèle d’Eyring repose sur la théorie de l’état de transition :
    \[
    \eta = \frac{h N_A}{V_m} \exp\left(\frac{\Delta G^\ddagger}{RT}\right)
    \]
    où \(\Delta G^\ddagger\) est l’énergie libre d’activation du flux visqueux.
    """)
    
    dG_act = st.slider("Énergie libre d’activation ΔG‡ (kJ/mol)", 80., 250., 150.)
    Vm = st.number_input("Volume molaire Vm (cm³/mol)", 20., 80., 45.)
    
    T_ey = np.linspace(1400, 1650, 40)
    # Constante simplifiée
    h = 6.626e-34
    NA = 6.022e23
    R = 8.314
    eta_ey = (h * NA / (Vm * 1e-6)) * np.exp(dG_act * 1000 / (R * (T_ey + 273)))
    # Normalisation pour obtenir des valeurs réalistes en Pa·s
    eta_ey = eta_ey / eta_ey[20] * 0.5   # ancrage à ~0.5 Pa·s au milieu
    
    fig_ey = go.Figure(go.Scatter(x=T_ey, y=eta_ey, mode="lines", line=dict(width=3, color="#8e44ad")))
    fig_ey.update_layout(title="Viscosité selon le modèle d’Eyring",
                         xaxis_title="Température (°C)", yaxis_title="Viscosité (Pa·s)",
                         yaxis_type="log", height=400)
    st.plotly_chart(fig_ey, use_container_width=True)
    
    st.info(f"""
    **Interprétation Eyring :**
    - ΔG‡ = {dG_act:.0f} kJ/mol
    - Plus ΔG‡ est élevé, plus la viscosité est sensible à la température
    - Le modèle capture le caractère activé du flux visqueux
    """)
    
    # ==================== COMPARAISON ARRHENIUS vs EYRING ====================
    st.subheader("Comparaison Arrhenius vs Eyring")
    
    Ea_arr = st.slider("Énergie d’activation Arrhenius Ea (kJ/mol)", 80., 250., 140.)
    
    # Arrhenius : η = A * exp(Ea/RT)
    A_arr = 1e-4
    eta_arr = A_arr * np.exp(Ea_arr * 1000 / (8.314 * (T_ey + 273)))
    eta_arr = eta_arr / eta_arr[20] * 0.5   # ancrage
    
    fig_comp_visc = go.Figure()
    fig_comp_visc.add_trace(go.Scatter(x=T_ey, y=eta_ey, mode="lines", name="Eyring", line=dict(width=3)))
    fig_comp_visc.add_trace(go.Scatter(x=T_ey, y=eta_arr, mode="lines", name="Arrhenius", line=dict(width=3, dash="dash")))
    fig_comp_visc.update_layout(title="Comparaison des modèles de viscosité",
                                xaxis_title="Température (°C)", yaxis_title="Viscosité (Pa·s)",
                                yaxis_type="log", height=450)
    st.plotly_chart(fig_comp_visc, use_container_width=True)
    show_interpretation("Arrhenius vs Eyring", """
    **Comparaison des modèles :**
    - Les deux modèles donnent une décroissance exponentielle de la viscosité avec la température.
    - Eyring est théoriquement plus fondé (théorie de l’état de transition + volume molaire).
    - Arrhenius est plus simple et souvent suffisant pour des estimations industrielles.
    
    L’écart entre les courbes augmente lorsque les énergies d’activation diffèrent.
    """)
    
    st.markdown("""
    **Différences principales :**
    - **Arrhenius** : forme empirique simple \(\eta = A \exp(E_a/RT)\)
    - **Eyring** : fondé sur la théorie de l’état de transition, fait intervenir le volume molaire
    - Les deux modèles donnent des dépendances exponentielles similaires en température
    - Eyring est théoriquement plus justifié pour les liquides
    """)
    
    with st.expander("Explication du modèle de viscosité"):
        st.markdown(r"""
        **Modèle utilisé (simplifié type Urbain / Riboud)**  
        Le modèle empirique calcule le logarithme de la viscosité à partir de :
        - La température (terme d’Arrhenius)
        - La basicité (rapport CaO / (SiO₂ + Al₂O₃))
        
        Forme générale :
        \[
        \log_{10} \eta = A + \frac{B}{T} + C \times (1 - B_{\text{urbain}})
        \]
        
        **Interprétation** :
        - Viscosité < 0,3 Pa·s : très fluide (bonne coulée)
        - 0,3 – 1,0 Pa·s : acceptable
        - > 1 Pa·s : risque de problèmes de coulée et de séparation métal/laitier
        
        Les modèles industriels plus avancés (Urbain, Riboud, FactSage, etc.) prennent en compte 
        les fractions molaires de tous les oxydes et des coefficients d’interaction.
        """)
    
    if viscosity < 0.3:
        st.success("Viscosité faible – bonne fluidité")
    elif viscosity < 1.0:
        st.info("Viscosité correcte")
    else:
        st.warning("Viscosité élevée – risque de problèmes de coulée")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[B2], y=[T_liq], mode="markers", marker=dict(size=15, color="red"), name="Votre laitier"))
    fig.update_layout(title="Position du laitier", xaxis_title="Basicité CaO/SiO₂", yaxis_title="T liquidus (°C)", height=400)
    st.plotly_chart(fig, use_container_width=True)

# ==================== 9. MODÉLISATION THERMODYNAMIQUE AVANCÉE ====================
elif module == "9. Modélisation Thermodynamique Avancée":
    st.header("Modélisation Thermodynamique Avancée")
    st.markdown(r"Diagrammes d’Ellingham et calcul de \(P_{\mathrm{O}_2}\).")

    T_range = st.slider("Plage de température (°C)", 600, 1600, (800, 1400))
    oxide = st.selectbox("Oxyde", ["FeO", "MnO", "SiO₂", "Cr₂O₃", "ZnO"])

    ellingham = {
        "FeO": (-265, 0.065),
        "MnO": (-385, 0.075),
        "SiO₂": (-910, 0.18),
        "Cr₂O₃": (-1120, 0.25),
        "ZnO": (-350, 0.10)
    }
    A, B = ellingham[oxide]
    Ts = np.linspace(T_range[0]+273, T_range[1]+273, 50)
    dG = A + B * Ts

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Ts-273, y=dG, mode="lines", name=f"2{oxide} → métal + O₂", line=dict(width=3)))
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(title=f"Diagramme d’Ellingham – {oxide}",
                      xaxis_title="Température (°C)", yaxis_title="ΔG° (kJ/mol O₂)", height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Activité et pression partielle d’oxygène")
    a_oxide = st.slider(f"Activité a_{oxide}", 0.01, 1.0, 0.15, 0.01)
    T_eq = st.slider("Température d’équilibre (°C)", 1000, 1600, 1250)
    
    dG_T = A + B * (T_eq + 273)
    K = np.exp(-dG_T * 1000 / (8.314 * (T_eq + 273)))
    P_O2 = K * (a_oxide ** 2)
    
    st.metric("Constante K", f"{K:.3e}")
    st.metric("P_O₂ d’équilibre", f"{P_O2:.3e} bar")
    
    st.subheader("Interprétation physique")
    if a_oxide < 0.3:
        st.success(f"""
        **Activité faible** (a = {a_oxide:.2f})  
        → P_O₂ d’équilibre **basse** ({P_O2:.2e} bar)  
        → L’oxyde est **peu stable** → **Réduction facilitée**
        """)
    elif a_oxide > 0.7:
        st.error(f"""
        **Activité élevée** (a = {a_oxide:.2f})  
        → P_O₂ d’équilibre **plus haute** ({P_O2:.2e} bar)  
        → L’oxyde est **plus stable** → **Réduction plus difficile**
        """)
    else:
        st.info(f"**Activité moyenne** (a = {a_oxide:.2f}) → P_O₂ = {P_O2:.2e} bar")
    
    st.markdown(r"""
    **Règle** :  
    - Activité faible de l’oxyde → \(P_{\mathrm{O}_2}\) faible → réduction plus facile  
    - Activité forte de l’oxyde → \(P_{\mathrm{O}_2}\) élevée → réduction plus difficile
    """)
    
    # ==================== SIMULATION PRESSION PARTIELLE ====================
    st.subheader("Simulation de la pression partielle d’oxygène")
    st.markdown("Évolution de \(P_{\mathrm{O}_2}\) en fonction de la température et de l’activité.")
    
    a_range = st.slider("Plage d’activité", 0.01, 1.0, (0.05, 0.5), key="a_range_po2")
    T_po2_min, T_po2_max = st.slider("Plage de température (°C)", 1000, 1600, (1100, 1500), key="T_po2")
    
    Ts_po2 = np.linspace(T_po2_min, T_po2_max, 40)
    dG_po2 = A + B * (Ts_po2 + 273)
    K_po2 = np.exp(-dG_po2 * 1000 / (8.314 * (Ts_po2 + 273)))
    
    fig_po2 = go.Figure()
    for a_val in [a_range[0], (a_range[0]+a_range[1])/2, a_range[1]]:
        P = K_po2 * (a_val ** 2)
        fig_po2.add_trace(go.Scatter(x=Ts_po2, y=P, mode="lines", name=f"a = {a_val:.2f}",
                                     line=dict(width=2.5)))
    fig_po2.update_layout(title="P_O₂ d’équilibre en fonction de la température",
                          xaxis_title="Température (°C)", yaxis_title="P_O₂ (bar)",
                          yaxis_type="log", height=450)
    st.plotly_chart(fig_po2, use_container_width=True)
    
    st.caption("Plus l’activité de l’oxyde est faible, plus la pression partielle d’oxygène d’équilibre est basse → réduction facilitée.")

# ==================== 10. CARACTÉRISTIQUES DES MINERAIS ====================
elif module == "1. Caractéristiques des Minerais":
    st.header("Caractéristiques des Minerais")
    c1, c2 = st.columns(2)
    with c1:
        mineral = st.selectbox("Minéral principal", 
            ["Hématite", "Magnétite", "Pyrolusite", "Chalcopyrite", "Sphalérite", "Bauxite (Gibbsite)"])
        grain_size = st.slider("Taille de grain (µm)", 10, 500, 80)
        liberation = st.slider("Degré de libération (%)", 40, 98, 75)
    with c2:
        hardness = st.slider("Dureté (Mohs)", 2.0, 7.0, 5.5)
        density = st.slider("Densité (g/cm³)", 2.5, 5.5, 4.2)
        moisture = st.slider("Humidité (%)", 0.5, 15.0, 4.0)

    st.subheader("Impact sur le procédé")
    if liberation < 70:
        st.warning("Libération faible → broyage plus fin nécessaire")
    else:
        st.success("Bonne libération")

    if grain_size < 50:
        st.info("Grains fins → meilleure cinétique, risque de boues")
    elif grain_size > 200:
        st.warning("Grains grossiers → cinétique plus lente")

    Wi = 12 + (hardness-4)*3
    energy_grind = Wi * (100/grain_size)**0.5
    st.metric("Énergie de broyage indicative", f"{energy_grind:.1f} kWh/t")
    
    # Courbe énergie vs taille de grain
    sizes = np.linspace(10, 300, 40)
    Wi_val = 12 + (hardness-4)*3
    energies = Wi_val * (100/sizes)**0.5
    fig_grind = go.Figure()
    fig_grind.add_trace(go.Scatter(x=sizes, y=energies, mode="lines", line=dict(width=3, color="#e67e22")))
    fig_grind.add_vline(x=grain_size, line_dash="dash", line_color="red", annotation_text="Taille actuelle")
    fig_grind.update_layout(title="Énergie de broyage en fonction de la taille de grain",
                            xaxis_title="Taille de grain (µm)", yaxis_title="Énergie (kWh/t)",
                            height=400)
    st.plotly_chart(fig_grind, use_container_width=True)
    
    st.subheader("Recommandations détaillées")
    st.markdown(f"""
    - Minéral principal : **{mineral}**
    - Taille de grain actuelle : {grain_size} µm
    - Taille optimale recommandée : {grain_size*0.7:.0f} – {grain_size:.0f} µm
    - Degré de libération : {liberation} %
    - Dureté (Mohs) : {hardness}
    - Densité : {density} g/cm³
    - Humidité : {moisture} %
    - Énergie de broyage estimée : {energy_grind:.1f} kWh/t
    """)

# ==================== 11. RÉACTEURS CATALYTIQUES ====================
elif module == "10. Réacteurs Catalytiques":
    st.header("Modélisation des Réacteurs Catalytiques")
    st.markdown("Simulation de réacteurs à lit fixe (PFR) et parfaitement agités (CSTR) avec catalyseur.")
    
    reactor_type = st.radio("Type de réacteur", ["Lit fixe (PFR)", "Parfaitement agité (CSTR)", "Comparaison PFR vs CSTR"])
    
    col1, col2 = st.columns(2)
    with col1:
        T_reac = st.slider("Température (°C)", 200, 600, 350)
        Ea_cat = st.number_input("Ea catalytique (kJ/mol)", 40., 150., 75.)
        k0_cat = st.number_input("k₀ catalytique", 1e3, 1e8, 1e5, format="%.0e")
    with col2:
        tau = st.slider("Temps de séjour τ (min)", 1., 120., 30.)
        C0 = st.number_input("Concentration entrée (mol/m³)", 10., 1000., 100.)
        order_cat = st.selectbox("Ordre de réaction", [1, 2])
    
    k_cat = arrhenius(T_reac, Ea_cat, k0_cat)
    st.metric("Constante catalytique k", f"{k_cat:.2e} min⁻¹")
    
    if reactor_type == "Lit fixe (PFR)":
        if order_cat == 1:
            X = 1 - np.exp(-k_cat * tau)
        else:
            X = (k_cat * tau * C0) / (1 + k_cat * tau * C0)
        st.metric("Conversion PFR", f"{X*100:.1f} %")
        
        z = np.linspace(0, 1, 50)
        if order_cat == 1:
            X_z = 1 - np.exp(-k_cat * tau * z)
        else:
            X_z = (k_cat * tau * z * C0) / (1 + k_cat * tau * z * C0)
        fig_pfr = go.Figure(go.Scatter(x=z, y=X_z*100, mode="lines", line=dict(width=3)))
        fig_pfr.update_layout(title="Profil de conversion le long du lit fixe",
                              xaxis_title="Position relative", yaxis_title="Conversion (%)", height=400)
        st.plotly_chart(fig_pfr, use_container_width=True)
        
    elif reactor_type == "Parfaitement agité (CSTR)":
        if order_cat == 1:
            X = (k_cat * tau) / (1 + k_cat * tau)
        else:
            X = 1 - 1 / (1 + k_cat * tau * C0 * 0.5)
        st.metric("Conversion CSTR", f"{X*100:.1f} %")
        st.info("Dans un CSTR, la conversion est plus faible qu’en PFR pour la même constante de vitesse.")
        
    else:
        taus = np.linspace(1, 120, 40)
        if order_cat == 1:
            X_pfr = 1 - np.exp(-k_cat * taus)
            X_cstr = (k_cat * taus) / (1 + k_cat * taus)
        else:
            X_pfr = (k_cat * taus * C0) / (1 + k_cat * taus * C0)
            X_cstr = 1 - 1 / (1 + k_cat * taus * C0 * 0.5)
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(x=taus, y=X_pfr*100, mode="lines", name="PFR", line=dict(width=3)))
        fig_comp.add_trace(go.Scatter(x=taus, y=X_cstr*100, mode="lines", name="CSTR", line=dict(width=3)))
        fig_comp.update_layout(title="Comparaison PFR vs CSTR",
                               xaxis_title="Temps de séjour (min)", yaxis_title="Conversion (%)", height=450)
        st.plotly_chart(fig_comp, use_container_width=True)
    
    st.subheader("Facteur d’efficacité du catalyseur")
    phi = st.slider("Module de Thiele φ", 0.1, 10., 1.5)
    eta = (3/phi) * (phi * np.cosh(phi) - np.sinh(phi)) / np.sinh(phi) if phi > 0 else 1
    st.metric("Facteur d’efficacité η", f"{eta:.3f}")
    if eta > 0.9:
        st.success("Limitation cinétique faible (η élevé)")
    elif eta > 0.5:
        st.info("Limitation diffusionnelle modérée")
    else:
        st.warning("Forte limitation par diffusion interne dans le catalyseur")
    
    with st.expander("Catalyseurs industriels en métallurgie / chimie"):
        st.markdown("""
        **Exemples de catalyseurs utilisés dans des procédés liés à la métallurgie :**
        
        - **Production d’hydrogène** (reformage) : catalyseurs à base de Ni  
        - **Synthèse d’ammoniac** : catalyseur Fe promu (procédé Haber-Bosch)  
        - **Oxydation de SO₂ → SO₃** (acide sulfurique) : V₂O₅  
        - **Hydrodésulfuration** : catalyseurs Co-Mo ou Ni-Mo sur alumine  
        - **Réduction sélective** : catalyseurs à base de Cu, Zn, ou métaux nobles selon le procédé
        
        En pyrométallurgie classique, les « catalyseurs » sont souvent les phases liquides (laitier, métal) ou les surfaces solides réactives plutôt que des catalyseurs solides classiques.
        """)
    
    with st.expander("Exemple détaillé : Procédé Haber-Bosch", expanded=False):
        st.markdown(r"""
        **Synthèse de l’ammoniac (Haber-Bosch)**
        
        **Réaction :**
        \[
        \mathrm{N_2 + 3H_2 \rightleftharpoons 2NH_3} \quad \Delta H = -92\,\mathrm{kJ/mol}
        \]
        
        **Conditions industrielles typiques :**
        - Température : 400 – 500 °C
        - Pression : 150 – 300 bar
        - Catalyseur : fer promu (Fe + Al₂O₃, K₂O, CaO)
        
        **Pourquoi ces conditions ?**
        - La réaction est exothermique → favorisée à basse température thermodynamiquement
        - Mais la cinétique est trop lente à basse T → compromis à ~450 °C
        - Haute pression → déplacement de l’équilibre vers NH₃ (principe de Le Chatelier)
        
        **Catalyseur :**
        - Le fer réduit la barrière d’activation de la dissociation de N₂ (étape limitante)
        - Les promoteurs (K₂O) augmentent l’activité électronique
        - Al₂O₃ stabilise la structure (support textural)
        
        **Réacteur :**
        - Généralement un réacteur à lit fixe multi-lits avec refroidissement intermédiaire
        - Conversion par passe : 15–25 %
        - Recyclage des gaz non convertis
        
        **Lien avec la métallurgie :**
        - Production d’hydrogène souvent couplée à des procédés métallurgiques ou de gazéification
        - Catalyseurs à base de fer proches de ceux utilisés dans certaines réductions
        """)
        
        # Mini simulation
        T_hb = st.slider("Température Haber-Bosch (°C)", 350, 550, 450, key="T_hb")
        P_hb = st.slider("Pression (bar)", 100, 300, 200)
        # Approximation simple de conversion
        K_hb = np.exp(10000/(T_hb+273) - 12) * (P_hb/200)**2
        X_hb = min(0.35, 0.15 * K_hb / (1 + K_hb))
        st.metric("Conversion approximative par passe", f"{X_hb*100:.1f} %")
        st.caption("Modèle simplifié à titre illustratif.")
        
        st.write("**Paramètres explorables :**")
        st.write(f"- Température : {T_hb} °C")
        st.write(f"- Pression : {P_hb} bar")
        if T_hb < 420:
            st.info("Température basse → cinétique lente")
        elif T_hb > 500:
            st.warning("Température élevée → équilibre défavorable")
        else:
            st.success("Plage de température industrielle typique")
    
    with st.expander("Exemple détaillé : Procédé Ostwald", expanded=False):
        st.markdown(r"""
        **Procédé Ostwald – Production d’acide nitrique**
        
        **Étapes principales :**
        
        1. **Oxydation catalytique de l’ammoniac**
        \[
        4\mathrm{NH_3} + 5\mathrm{O_2} \rightarrow 4\mathrm{NO} + 6\mathrm{H_2O} \quad \Delta H < 0
        \]
        - Catalyseur : toile de platine-rhodium (Pt-Rh)
        - Température : 800 – 900 °C
        - Pression : 1 – 10 bar
        
        2. **Oxydation de NO en NO₂**
        \[
        2\mathrm{NO} + \mathrm{O_2} \rightarrow 2\mathrm{NO_2}
        \]
        
        3. **Absorption de NO₂ dans l’eau**
        \[
        3\mathrm{NO_2} + \mathrm{H_2O} \rightarrow 2\mathrm{HNO_3} + \mathrm{NO}
        \]
        
        **Points clés :**
        - Catalyseur très sélectif (Pt-Rh) pour éviter la formation de N₂
        - Temps de contact très court (~0,001 s) pour limiter les réactions secondaires
        - Récupération du catalyseur importante (coût élevé du platine)
        
        **Lien avec Haber-Bosch :**
        - L’ammoniac produit par Haber-Bosch est la matière première du procédé Ostwald
        - Les deux procédés sont souvent couplés dans les complexes d’engrais
        """)
        
        T_ost = st.slider("Température Ostwald (°C)", 750, 950, 850, key="T_ost")
        # Sélectivité approximative
        selectivite = 95 - 0.02 * (T_ost - 850)**2
        selectivite = np.clip(selectivite, 85, 98)
        st.metric("Sélectivité approximative en NO", f"{selectivite:.1f} %")
        st.caption("La sélectivité est maximale autour de 850 °C.")

st.markdown("---")
st.caption("**Dr Ulrich Landry Compaoré** – Génie Métallurgique – EPO Ouagadougou • Application complète unifiée • Novembre 2026")
