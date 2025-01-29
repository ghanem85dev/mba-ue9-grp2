# Guide de Scraping des Données – Équipes Data Scientists de l’ADEME

## Problèmes Rencontrés

### Difficultés Techniques :
- Blocages fréquents (CAPTCHAs, restrictions API, détection de scraping par les sites médias).
- Limites d'outils standards comme Octoparse sur les contenus complexes ou non structurés.
- Impossibilité d’accéder directement à certaines API de sites médias.

### Obstacles Légaux et Éthiques :
- Conformité aux conditions d’utilisation et au RGPD pour éviter tout risque juridique.
- Sensibilité accrue des données collectées, notamment pour des sujets comme le complotisme.

---

## Organisation et Méthodes

### Division par Sources :
- Organisation des tâches en fonction des types de plateformes : YouTube, Reddit, médias en ligne.
- Focus sur les sources critiques et spécifiques (contenus vidéo, discussions).

### Optimisation des Données :
- Utilisation de **KPI de filtrage** pour prioriser les données pertinentes.
- Nettoyage en amont pour éviter les doublons ou les résultats peu fiables.

### Approches Outils :
- **Octoparse** : Développement de templates personnalisés (pagination avancée, boucles imbriquées) pour les plateformes comme YouTube et Reddit, où il est efficace.
- **Python** : Développement de scripts avancés pour les sites médias nécessitant des solutions plus flexibles et robustes.

---

## Bonnes Pratiques

1. **Respecter les règles des plateformes** (conditions d’utilisation, RGPD).

2. **Déployer des techniques avancées en Python** :
   - Rotation des proxies et des User-Agents pour éviter les blocages.
   - Utilisation d’API spécialisées comme **News API** ou **ScraperAPI** pour des extractions fiables.
   - Automatisation via des interfaces utilisateurs (IHM) pour simplifier l’expérience.

3. **Former les équipes à** :
   - Reconnaître les limites légales et techniques.
   - Adapter les outils à chaque type de source.

---

## Limites d’Octoparse

- **Efficace** pour les plateformes comme YouTube grâce à des templates optimisés.
- **Limité** pour les sites médias :
  - Détection facile des processus automatisés.
  - Incapacité à gérer les interactions dynamiques ou les API.

**Solution Alternative** : Utilisation de scripts Python sur mesure, plus flexibles, permettant d’intégrer des stratégies avancées.

---

## Recommandations

1. **Automatisation Interne** : Développer une solution Python robuste pour le scraping complexe.
2. **Surveillance Continue** : Mettre en place un processus d’analyse automatisée pour détecter les discours critiques.
3. **Équipes Formées** : Sensibiliser les data scientists aux contraintes légales et aux techniques modernes de scraping.
