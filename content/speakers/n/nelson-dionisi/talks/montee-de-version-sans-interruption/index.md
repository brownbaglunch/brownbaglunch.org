---
layout: talk
url: /speakers/nelson-dionisi/talks/montee-de-version-sans-interruption/
tags:
- deployment
- database
- continuous-delivery
- java
versions:
- label: FR
  flag: fr
  title: Montée de version sans interruption
  abstract: De plus en plus d'éditeurs logiciels fournissent leurs solutions en SaaS,
    et tendent à déployer leurs applications en Continuous Delivery. Pour cela, les
    contraintes business impliquent souvent de pouvoir déployer un nouvelle version
    applicative sans interruption de service. Les techniques classiques de Rolling
    Update permettent de réaliser une montée de version sans interruption de service
    assez facilement. La complexité intervient lorsque l'on gère une base de données
    relationnelle, et que l'on souhaite faire évoluer son schéma, le tout, toujours
    sans interruption de service. Depuis 3 ans, au sein de Mirakl, nous avons mis
    en place un système de montée de version sans interruption de service avec une
    base relationnelle. Ce talk est un retour d'expérience présentant les mécanismes
    que nous avons mis en place pour réaliser ces montées de version sans interruption.
    Il se concentre sur la partie applicative, et les problématiques engendrées par
    un tel process. Le but est d'être le plus concret possible, avec des exemples
    de 'la vraie vie', notamment quelques astuces pour réaliser ses migrations sans
    douleur avec des frameworks comme Hibernate ou jOOQ. Les exemples sont donnés
    en Java avec une base de données PostgreSQL, mais les principes s'appliquent à
    n'importe quel language et à la plupart des bases de données relationnelles.
---
