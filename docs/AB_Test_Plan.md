# Plan A/B Test — Relance Email d'Abandon de Panier
### DDDM Projet | ENSIAS GL2 — 2025/2026

---

## 1. Contexte & Objectif

L'analyse prédictive a révélé un taux d'abandon de panier de **71.9%** sur la plateforme e-commerce étudiée (Online Retail II + E-Commerce Behavior Data). L'objectif de cette expérimentation est de mesurer l'effet causal d'une **relance email automatique dans les 2 heures suivant l'abandon** sur le taux de conversion cart → purchase.

---

## 2. Formulation des Hypothèses

| | Énoncé |
|---|---|
| **H₀ (nulle)** | L'envoi d'un email de relance dans les 2h n'a pas d'effet significatif sur le taux de conversion cart → purchase |
| **H₁ (alternative)** | Le taux de conversion du groupe traitement (email) est **strictement supérieur** au groupe contrôle |
| **Type de test** | Test unilatéral supérieur (one-tailed z-test de proportions) |

---

## 3. Protocole Expérimental

### 3.1 Groupes

| Groupe | Description | Allocation |
|---|---|---|
| **A — Contrôle** | Aucun email envoyé (comportement actuel) | 50% |
| **B — Traitement** | Email de relance personnalisé 2h après abandon, avec photo du produit abandonné + livraison offerte | 50% |

### 3.2 Critères d'éligibilité
- Session ayant généré un événement `cart` sans `purchase` dans les 2 heures suivantes
- Client avec adresse email valide et opt-in marketing
- Exclusion : clients ayant déjà reçu un email de relance dans les 7 derniers jours

### 3.3 Randomisation
Attribution aléatoire au niveau de la **session** (pas du client) via hachage de l'ID session modulo 2. Reproductible avec seed fixé.

---

## 4. Métriques

### KPI Principal
- **Taux de conversion cart → purchase dans les 24h suivant l'abandon**

### KPIs Secondaires (suivi post-décision)
| Métrique | Description | Seuil d'alerte |
|---|---|---|
| Taux d'ouverture email | Nb ouvertures / nb envois | < 15% |
| Taux de clic | Clics lien panier / ouvertures | < 8% |
| AOV (panier moyen) | CA moyen des commandes récupérées | — |
| Taux de désabonnement | Unsubscribes / envois | > 0.5% |
| Taux de conversion à 72h | Mesure de l'effet retardé | — |

---

## 5. Calcul Statistique

| Paramètre | Valeur | Justification |
|---|---|---|
| Taux de conversion baseline (p₀) | 28.1% | Mesuré sur données historiques |
| Effet minimal détectable (MDE) | +5% relatif → p₁ = 29.5% | Seuil de rentabilité estimé |
| Risque type I (α) | 0.05 | Standard industriel |
| Puissance (1−β) | 80% | Standard industriel |
| **Taille d'échantillon / groupe** | **~3 800 sessions** | Calculée via formule z-test à deux proportions |
| **Total sessions nécessaires** | **~7 600** | Sur les deux groupes |
| **Durée estimée** | **14 jours** | ~540 sessions avec panier/jour en moyenne |

**Formule utilisée :**
```
n = (z_α + z_β)² × [p₀(1−p₀) + p₁(1−p₁)] / (p₁ − p₀)²
avec z_α = 1.96, z_β = 0.842
```

---

## 6. Durée & Planning

| Étape | Date | Durée |
|---|---|---|
| Setup technique (tracking, segmentation) | J0 | 3 jours |
| Collecte des données (expérience live) | J3 → J17 | **14 jours** |
| Analyse des résultats | J18 | 1 jour |
| Décision de déploiement | J19 | — |

> **Règle d'arrêt anticipé :** Si p-value < 0.01 à mi-parcours (J10) avec n ≥ 1500/groupe, l'expérience peut être stoppée et le traitement déployé. Si taux de désabonnement > 1%, arrêt immédiat.

---

## 7. Résultats Simulés

Sur une simulation Monte Carlo (seed=42, n=3800/groupe) :

| Groupe | Taux de conversion | n convertis |
|---|---|---|
| A — Contrôle | 28.1% | ~1 068 |
| B — Traitement | 30.1% | ~1 144 |
| **Lift observé** | **+7.1%** | — |
| **p-value** | **< 0.05** | ✅ H₀ rejetée |

---

## 8. Impact Financier Attendu

| Indicateur | Valeur |
|---|---|
| Conversions supplémentaires / mois | ~480 |
| Panier moyen (AOV) | £42.70 |
| **CA additionnel / mois** | **~£20 500** |
| **CA additionnel / an** | **~£246 000** |
| Coût email (0.02€/envoi × 8000/mois) | ~160€/mois |
| **ROI estimé** | **~1 200%** |

---

## 9. Décision

Si H₀ est rejetée (p < 0.05) et que le taux de désabonnement reste sous 0.5%, la recommandation est de **déployer l'email de relance à 100% de la base éligible** et de mesurer l'impact réel sur 30 jours via les métriques de suivi définies ci-dessus.

---

*Document rédigé dans le cadre du module Data-Driven Decision Making — ENSIAS GL2 — 2025/2026*
