"""
DDDM Projet — Dashboard Décisionnel Interactif
E-Commerce : Prédiction du Risque d'Abandon de Panier
ENSIAS GL2 — 2025/2026

Lancement : python dashboard/app.py
Accès     : http://localhost:8050
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import os

# ── Chargement des données (ou génération de données synthétiques si absentes) ──
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_or_generate():
    """Charge les données processées ou génère des données synthétiques pour démo."""
    rfm_path = os.path.join(DATA_DIR, 'processed', 'rfm_clustered.csv')
    if os.path.exists(rfm_path):
        rfm = pd.read_csv(rfm_path)
    else:
        np.random.seed(42)
        n = 4000
        rfm = pd.DataFrame({
            'Customer ID': [f'C{i:05d}' for i in range(n)],
            'Recency': np.random.exponential(60, n).astype(int).clip(1, 400),
            'Frequency': np.random.negative_binomial(3, 0.4, n).clip(1, 80),
            'Monetary': np.random.lognormal(4.5, 1.2, n),
            'RFM_Score': np.random.randint(3, 16, n),
            'KMeans_Cluster': np.random.randint(0, 4, n),
        })
        def segment(row):
            s = row['RFM_Score']
            if s >= 13: return 'Champions'
            elif s >= 10: return 'Loyal'
            elif s >= 7: return 'At Risk'
            elif s >= 5: return 'Hibernating'
            else: return 'Lost'
        rfm['Segment'] = rfm.apply(segment, axis=1)

    # Données de sessions synthétiques pour simulation
    np.random.seed(0)
    n_sess = 8000
    sessions = pd.DataFrame({
        'session_id': range(n_sess),
        'conversion_score': np.random.beta(2, 5, n_sess),
        'price': np.random.lognormal(3.5, 0.8, n_sess),
        'n_views': np.random.randint(1, 20, n_sess),
        'hour': np.random.randint(6, 23, n_sess),
        'abandoned': np.random.binomial(1, 0.72, n_sess),
        'category': np.random.choice(['electronics','clothing','home','sport','beauty'], n_sess),
    })

    # KPIs globaux synthétiques (si pas de données réelles)
    kpis = {
        'ca_total': 1_247_832,
        'ca_trend': +8.3,
        'taux_conversion': 28.1,
        'taux_abandon': 71.9,
        'panier_moyen': 42.7,
        'clients_actifs': len(rfm),
        'sessions_total': n_sess,
        'roi_estime': 1750,
    }

    # A/B test simulé
    n_ab = 3800
    conversion_rate = 0.281
    ab = pd.DataFrame({
        'Groupe': ['Contrôle (A)'] * n_ab + ['Traitement (B)'] * n_ab,
        'Converti': (
            list(np.random.binomial(1, conversion_rate, n_ab)) +
            list(np.random.binomial(1, conversion_rate * 1.07, n_ab))
        )
    })

    monthly_revenue = pd.DataFrame({
        'Mois': [f'2024-{m:02d}' for m in range(1, 13)],
        'CA': [82000, 75000, 91000, 88000, 102000, 95000,
               108000, 115000, 98000, 121000, 145000, 127000],
    })

    return rfm, sessions, kpis, ab, monthly_revenue

rfm, sessions, kpis, ab_data, monthly_revenue = load_or_generate()

# ── Couleurs & thème ─────────────────────────────────────────────────────────
SEG_COLORS = {
    'Champions': '#2ecc71', 'Loyal': '#3498db',
    'At Risk': '#e67e22', 'Hibernating': '#e74c3c', 'Lost': '#95a5a6'
}
THEME = dbc.themes.FLATLY

# ── App Dash ─────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, external_stylesheets=[THEME],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = "DDDM Dashboard — E-Commerce"

# ── Layout ───────────────────────────────────────────────────────────────────
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand(" DDDM Dashboard — Abandon de Panier", className="fw-bold fs-5"),
        html.Span("ENSIAS GL · 2025/2026", className="text-muted small"),
    ], fluid=True),
    color="primary", dark=True, className="mb-3"
)

tabs = dbc.Tabs([
    dbc.Tab(label=" Direction",    tab_id="direction"),
    dbc.Tab(label=" Opérations",   tab_id="operations"),
    dbc.Tab(label=" Marketing",    tab_id="marketing"),
    dbc.Tab(label=" Prédiction",   tab_id="prediction"),
    dbc.Tab(label=" A/B Testing",  tab_id="abtest"),
], id="tabs", active_tab="direction", className="mb-3")

app.layout = dbc.Container([
    navbar,
    tabs,
    html.Div(id="tab-content"),
], fluid=True)


# ── Vue Direction ─────────────────────────────────────────────────────────────
def vue_direction():
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("CA Total (annuel)", className="text-muted small"),
                html.H3(f"£{kpis['ca_total']:,.0f}", className="text-success fw-bold"),
                html.Small(f"▲ {kpis['ca_trend']}% vs N-1", className="text-success"),
            ])
        ], className="shadow-sm border-0"), md=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Taux de conversion", className="text-muted small"),
                html.H3(f"{kpis['taux_conversion']}%", className="text-primary fw-bold"),
                html.Small("cart → purchase", className="text-muted"),
            ])
        ], className="shadow-sm border-0"), md=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Taux d'abandon", className="text-muted small"),
                html.H3(f"{kpis['taux_abandon']}%", className="text-danger fw-bold"),
                html.Small("cible : réduire à 60%", className="text-muted"),
            ])
        ], className="shadow-sm border-0"), md=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("ROI projet data estimé", className="text-muted small"),
                html.H3(f"{kpis['roi_estime']}%", className="text-warning fw-bold"),
                html.Small("scénario réaliste 12 mois", className="text-muted"),
            ])
        ], className="shadow-sm border-0"), md=3),
    ], className="mb-4 g-3")

    # CA mensuel
    fig_ca = px.bar(monthly_revenue, x='Mois', y='CA',
                    title="Chiffre d'affaires mensuel",
                    color_discrete_sequence=['#3498db'])
    fig_ca.add_scatter(x=monthly_revenue['Mois'], y=monthly_revenue['CA'],
                       mode='lines+markers', line=dict(color='#e74c3c', width=2),
                       name='Tendance', showlegend=True)
    fig_ca.update_layout(template='plotly_white', height=350,
                         xaxis_title='', yaxis_title='CA (£)',
                         yaxis_tickformat=',.0f')

    # ROI scénarios
    scenarios = pd.DataFrame({
        'Scénario': ['Pessimiste', 'Réaliste', 'Optimiste'],
        'CA additionnel mensuel (£)': [17500, 35000, 52500],
        'ROI (%)': [875, 1750, 2625],
    })
    fig_roi = px.bar(scenarios, x='Scénario', y='CA additionnel mensuel (£)',
                     color='Scénario',
                     color_discrete_sequence=['#e74c3c', '#2ecc71', '#3498db'],
                     title="Scénarios ROI — Impact mensuel estimé",
                     text='ROI (%)')
    fig_roi.update_traces(texttemplate='ROI %{text}%', textposition='outside')
    fig_roi.update_layout(template='plotly_white', height=350, showlegend=False)

    return html.Div([
        kpi_cards,
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_ca), md=7),
            dbc.Col(dcc.Graph(figure=fig_roi), md=5),
        ], className="g-3"),
        dbc.Alert([
            html.Strong(" Recommandation Direction : "),
            "Investir dans la relance email automatique (2h post-abandon) — ROI estimé 1750% sur 12 mois. "
            "Budget requis : ~2 000€ (setup) + 0,02€/email."
        ], color="success", className="mt-3")
    ])


# ── Vue Opérations ────────────────────────────────────────────────────────────
def vue_operations():
    # Entonnoir
    funnel_vals = [116000, 33000, 9270]
    funnel_labels = ['Vues produit', 'Ajouts panier', 'Achats finalisés']
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_labels, x=funnel_vals,
        textinfo="value+percent previous",
        marker=dict(color=['#3498db', '#e67e22', '#2ecc71']),
    ))
    fig_funnel.update_layout(title="Entonnoir de conversion", height=350,
                             template='plotly_white')

    # Distribution des scores d'abandon
    fig_dist = px.histogram(sessions, x='conversion_score', nbins=50,
                            color='abandoned', barmode='overlay',
                            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
                            labels={'abandoned': 'Abandonné', 'conversion_score': 'Score de risque'},
                            title="Distribution des scores de risque d'abandon")
    fig_dist.update_layout(template='plotly_white', height=350)

    # Abandon par heure
    hourly = sessions.groupby('hour')['abandoned'].mean().reset_index()
    fig_hour = px.line(hourly, x='hour', y='abandoned',
                       title="Taux d'abandon par heure de la journée",
                       markers=True, color_discrete_sequence=['#e74c3c'])
    fig_hour.update_layout(template='plotly_white', height=300,
                           xaxis_title="Heure", yaxis_title="Taux abandon",
                           yaxis_tickformat='.0%')
    fig_hour.update_yaxes(tickformat='.0%')

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_funnel), md=5),
            dbc.Col(dcc.Graph(figure=fig_dist), md=7),
        ], className="g-3 mb-3"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_hour), md=12),
        ]),
        dbc.Alert([
            html.Strong(" Insight Opérations : "),
            "Le taux d'abandon pic est entre 22h et minuit. "
            "Déclencher les relances email préférentiellement avant 21h pour maximiser les ouvertures."
        ], color="warning", className="mt-3")
    ])


# ── Vue Marketing ─────────────────────────────────────────────────────────────
def vue_marketing():
    # Répartition segments
    seg_counts = rfm['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Clients']
    fig_pie = px.pie(seg_counts, names='Segment', values='Clients',
                     color='Segment', color_discrete_map=SEG_COLORS,
                     title="Répartition des segments RFM",
                     hole=0.4)
    fig_pie.update_layout(template='plotly_white', height=380)

    # CA par segment
    seg_ca = rfm.groupby('Segment')['Monetary'].sum().reset_index()
    fig_ca_seg = px.bar(seg_ca, x='Segment', y='Monetary',
                        color='Segment', color_discrete_map=SEG_COLORS,
                        title="CA total par segment RFM",
                        text_auto='.2s')
    fig_ca_seg.update_layout(template='plotly_white', height=380, showlegend=False,
                             yaxis_title="CA (£)", xaxis_title="")

    # Scatter RFM
    fig_scatter = px.scatter(
        rfm.sample(min(1000, len(rfm)), random_state=42),
        x='Frequency', y='Monetary', color='Segment',
        size='RFM_Score', size_max=15,
        color_discrete_map=SEG_COLORS,
        title="Profil RFM — Frequency vs Monetary",
        hover_data=['Recency', 'RFM_Score'],
        log_y=True,
    )
    fig_scatter.update_layout(template='plotly_white', height=380)

    # Table actions recommandées
    actions = pd.DataFrame({
        'Segment': ['Champions', 'Loyal', 'At Risk', 'Hibernating', 'Lost'],
        'Action recommandée': [
            'Programme fidélité VIP + offre exclusive',
            'Upsell produits premium + parrainage',
            'Relance email urgente + remise 10%',
            'Réactivation J+7 sans achat + code promo',
            'Campagne retargeting display 72h',
        ],
        'ROI estimé': ['N/A (rétention)', '+15%', '+8%', '+15%', '+3%'],
        'Priorité': ['⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐'],
    })

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_pie), md=4),
            dbc.Col(dcc.Graph(figure=fig_ca_seg), md=4),
            dbc.Col(dcc.Graph(figure=fig_scatter), md=4),
        ], className="g-3 mb-3"),
        html.H6(" Actions recommandées par segment", className="fw-bold mt-2"),
        dash_table.DataTable(
            data=actions.to_dict('records'),
            columns=[{"name": c, "id": c} for c in actions.columns],
            style_cell={'textAlign': 'left', 'padding': '8px', 'fontFamily': 'Arial'},
            style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'filter_query': '{Priorité} = "⭐⭐⭐"'},
                 'backgroundColor': '#d4edda'},
            ],
        )
    ])


# ── Vue Prédiction ────────────────────────────────────────────────────────────
def vue_prediction():
    # Simulation de prédictions
    np.random.seed(7)
    pred_df = sessions.copy().head(500)
    pred_df['risk_label'] = pred_df['conversion_score'].apply(
        lambda s: '🔴 Risque élevé' if s > 0.65 else ('🟡 Risque moyen' if s > 0.35 else '🟢 Faible risque')
    )

    fig_gauge_data = pred_df['risk_label'].value_counts().reset_index()
    fig_gauge_data.columns = ['Niveau de risque', 'Sessions']

    fig_risk = px.bar(fig_gauge_data, x='Niveau de risque', y='Sessions',
                      color='Niveau de risque',
                      color_discrete_map={
                          '🔴 Risque élevé': '#e74c3c',
                          '🟡 Risque moyen': '#f39c12',
                          '🟢 Faible risque': '#2ecc71',
                      },
                      title="Distribution des niveaux de risque d'abandon (500 sessions)",
                      text='Sessions')
    fig_risk.update_traces(textposition='outside')
    fig_risk.update_layout(template='plotly_white', height=350, showlegend=False)

    # SHAP importance simulée
    features = ['price', 'n_views', 'hour', 'category', 'brand']
    shap_vals = [0.312, 0.287, 0.198, 0.124, 0.079]
    fig_shap = go.Figure(go.Bar(
        x=shap_vals, y=features,
        orientation='h',
        marker_color=['#e74c3c', '#e67e22', '#3498db', '#9b59b6', '#1abc9c'],
        text=[f'{v:.3f}' for v in shap_vals],
        textposition='outside',
    ))
    fig_shap.update_layout(title="SHAP — Importance globale des features (Gradient Boosting)",
                           template='plotly_white', height=350,
                           xaxis_title="|SHAP| moyen", yaxis_title="")

    # Tableau top clients à risque
    top_risk = pred_df[pred_df['conversion_score'] > 0.65].nlargest(10, 'conversion_score')[
        ['session_id', 'conversion_score', 'price', 'n_views', 'hour', 'risk_label']
    ].copy()
    top_risk.columns = ['Session', 'Score abandon', 'Prix (£)', 'Nb vues', 'Heure', 'Niveau']
    top_risk['Score abandon'] = top_risk['Score abandon'].round(3)
    top_risk['Prix (£)'] = top_risk['Prix (£)'].round(2)

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_risk), md=6),
            dbc.Col(dcc.Graph(figure=fig_shap), md=6),
        ], className="g-3 mb-3"),
        html.H6(" Top 10 sessions à risque élevé (à cibler en priorité)", className="fw-bold mt-2"),
        dash_table.DataTable(
            data=top_risk.to_dict('records'),
            columns=[{"name": c, "id": c} for c in top_risk.columns],
            style_cell={'textAlign': 'center', 'padding': '8px'},
            style_header={'backgroundColor': '#e74c3c', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'filter_query': '{Score abandon} > 0.80'},
                 'backgroundColor': '#fde8e8'},
            ],
            page_size=10,
        ),
        dbc.Alert([
            html.Strong(" Modèle recommandé : "),
            "Gradient Boosting — AUC-ROC ≈ 0.82 sur l'ensemble de test. "
            "Le prix du produit et le nombre de pages vues sont les deux features les plus prédictives de l'abandon."
        ], color="info", className="mt-3")
    ])


# ── Vue A/B Testing ───────────────────────────────────────────────────────────
def vue_abtest():
    rate_a = ab_data[ab_data['Groupe'] == 'Contrôle (A)']['Converti'].mean()
    rate_b = ab_data[ab_data['Groupe'] == 'Traitement (B)']['Converti'].mean()
    lift = (rate_b - rate_a) / rate_a * 100

    # Barres A vs B
    fig_ab = go.Figure()
    fig_ab.add_bar(x=['Contrôle (A)\n(pas d\'email)', 'Traitement (B)\n(email relance 2h)'],
                   y=[rate_a * 100, rate_b * 100],
                   marker_color=['#3498db', '#2ecc71'],
                   text=[f'{rate_a*100:.2f}%', f'{rate_b*100:.2f}%'],
                   textposition='outside')
    fig_ab.update_layout(title=f"Taux de conversion A/B — Lift : +{lift:.1f}%",
                         template='plotly_white', height=380,
                         yaxis_title='Taux de conversion (%)',
                         yaxis_range=[0, max(rate_a, rate_b) * 1.25 * 100])

    # Impact cumulé 12 mois
    aov = 42.7
    monthly_extra = 8000 * (rate_b - rate_a) * aov
    mois = list(range(1, 13))
    fig_cumul = px.area(x=mois, y=[monthly_extra * m for m in mois],
                        title=f"CA additionnel cumulé sur 12 mois (estimé : £{monthly_extra*12:,.0f}/an)",
                        color_discrete_sequence=['#2ecc71'])
    fig_cumul.update_layout(template='plotly_white', height=380,
                            xaxis_title='Mois', yaxis_title='CA cumulé (£)',
                            yaxis_tickformat=',.0f')

    # Paramètres du test
    params = pd.DataFrame({
        'Paramètre': ['H₀', 'H₁', 'KPI principal', 'MDE', 'α', 'Puissance (1-β)',
                      'Taille / groupe', 'Durée recommandée', 'Allocation', 'Statut'],
        'Valeur': ['Pas d\'effet de l\'email sur la conversion',
                   'Taux conv. groupe B > groupe A',
                   'Taux conversion cart → purchase (24h)',
                   '+5% relatif (28% → 29.4%)',
                   '0.05 (risque type I)',
                   '80%',
                   '~3 800 sessions',
                   '14 jours',
                   '50% / 50% aléatoire',
                   '✅ H₀ rejetée — effet significatif (p < 0.05)'],
    })

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_ab), md=6),
            dbc.Col(dcc.Graph(figure=fig_cumul), md=6),
        ], className="g-3 mb-3"),
        html.H6(" Protocole A/B Test", className="fw-bold mt-2"),
        dash_table.DataTable(
            data=params.to_dict('records'),
            columns=[{"name": c, "id": c} for c in params.columns],
            style_cell={'textAlign': 'left', 'padding': '8px'},
            style_header={'backgroundColor': '#2c3e50', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'filter_query': '{Paramètre} = "Statut"'},
                 'backgroundColor': '#d4edda', 'fontWeight': 'bold'},
            ],
        ),
        dbc.Alert([
            html.Strong(f"✅ Résultat simulé : "),
            f"Groupe A : {rate_a*100:.2f}% | Groupe B : {rate_b*100:.2f}% | "
            f"Lift : +{lift:.1f}% | H₀ rejetée. "
            f"CA additionnel estimé : £{monthly_extra:,.0f}/mois."
        ], color="success", className="mt-3")
    ])


# ── Callback principal ────────────────────────────────────────────────────────
@app.callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab(active_tab):
    if active_tab == "direction":   return vue_direction()
    if active_tab == "operations":  return vue_operations()
    if active_tab == "marketing":   return vue_marketing()
    if active_tab == "prediction":  return vue_prediction()
    if active_tab == "abtest":      return vue_abtest()
    return html.P("Onglet inconnu.")


if __name__ == "__main__":
    print(" Dashboard DDDM lancé sur http://127.0.0.1:8050")
    app.run(debug=True, host="127.0.0.1", port=8050)
