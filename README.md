# DDDM Projet — E-Commerce : Prédiction du Risque d'Abandon de Panier

## 🗂️ Architecture du projet

```
DDDM_Projet/
├── DDDM_Projet_Complet_FINAL.ipynb   # Notebook principal (phases 1–6)
├── requirements.txt                   # Dépendances Python
├── README.md                          # Ce fichier
│
├── dashboard/
│   └── app.py                         # Dashboard Plotly Dash (5 vues)
│
├── data/
│   ├── raw/                           # Datasets bruts (à télécharger — voir ci-dessous)
│   │   ├── online_retail_II.csv
│   │   └── ecommerce_behavior.csv
│   └── processed/                     # Générés par le notebook
│       ├── rfm.csv
│       └── rfm_clustered.csv
│
├── reports/                           # Figures PNG générées par le notebook
│   ├── fig_distributions.png
│   ├── fig_temporal.png
│   ├── fig_rfm.png
│   ├── fig_correlation_funnel.png
│   ├── fig_elbow.png
│   ├── fig_roc_comparison.png
│   ├── fig_shap.png
│   └── fig_ab_impact.png
│
└── docs/
    └── AB_Test_Plan.md                # Plan A/B Test (2 pages)
```

---

##  Installation

### 1. Prérequis
- Python 3.10+
- pip

### 2. Cloner le dépôt
```bash
git clone https://github.com/----/DDDM_Projet.git
cd DDDM_Projet
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Télécharger les datasets

**Dataset 1 — Online Retail II (UCI ML Repository)**
```
https://archive.ics.uci.edu/dataset/502/online+retail+ii
```
→ Placer `online_retail_II.csv` dans `data/raw/`

**Dataset 2 — E-Commerce Behavior Data**
```
https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store
```
→ Placer `ecommerce_behavior.csv` dans `data/raw/`

---

##  Lancement

### Notebook (analyse complète phases 1–6)
```bash
jupyter notebook DDDM_Projet_Complet_FINAL.ipynb
```
> Les chemins dans le notebook pointent vers `data/raw/`. Adapter si nécessaire.

### Dashboard interactif
```bash
python dashboard/app.py
```
Puis ouvrir : [http://localhost:8050](http://localhost:8050)

> Le dashboard fonctionne **sans les datasets réels** — il génère des données synthétiques représentatives si les fichiers CSV ne sont pas présents.

---

##  Phases du projet

| Phase | Description | Statut |
|---|---|---|
| 1 | Définition du problème & KPIs | ✅ |
| 2 | Collecte & Audit des données | ✅ |
| 3 | EDA & Analyse statistique | ✅ |
| 4 | Modélisation prédictive & SHAP | ✅ |
| 5 | Dashboard décisionnel (5 vues)| ✅ |
| 6 | Décision, A/B Testing & Impact | ✅ |

---

##  Livrables

| Livrable | Fichier |
|---|---|
| Notebook Jupyter complet | `DDDM_Projet_Complet_FINAL.ipynb` |
| Dashboard interactif | `dashboard/app.py` |
| Plan A/B Test (2 pages) | `docs/AB_Test_Plan.md` |
| Requirements | `requirements.txt` |
| README | `README.md` |

---

##  Résultats clés

- **Taux d'abandon de panier détecté** : 71.9%
- **Meilleur modèle** : Gradient Boosting — AUC-ROC ≈ 0.82
- **Features les plus prédictives** : prix du produit, nombre de pages vues
- **ROI estimé (relance email)** : 1 200% sur 12 mois
- **CA additionnel estimé/an** : ~£246 000

---

##  Stack technique

`Python 3.10` · `Pandas` · `Scikit-learn` · `SHAP` · `Plotly Dash` · `Scipy` · `Seaborn`

---

