---
name: "Nelson Dionisi"
since: "2019-09-02"
city: "fr/bordeaux"
cities:
  - "fr/bordeaux"
  - "fr/paris"
tags:
  - "deployment"
  - "database"
  - "continous-delivery"
  - "java"
  - "postgresql"
  - "performance"
cover: "https://avatars1.githubusercontent.com/u/12200878?s=460&v=4"
contacts:
  mail: "ndionisi@mirakl.com"
websites:
  - name: "GitHub"
    url: "https://github.com/ndionisi"
  - name: "LinkedIn"
    url: "https://www.linkedin.com/in/nelson-dionisi-84a00472"
sessions:
  - tags:
      - "deployment"
      - "database"
      - "continous-delivery"
      - "java"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Montée de version sans interruption"
        abstract: "De plus en plus d'éditeurs logiciels fournissent leurs solutions en SaaS, et tendent à déployer leurs applications en Continuous Delivery. Pour cela, les contraintes business impliquent souvent de pouvoir déployer un nouvelle version applicative sans interruption de service. Les techniques classiques de Rolling Update permettent de réaliser une montée de version sans interruption de service assez facilement. La complexité intervient lorsque l'on gère une base de données relationnelle, et que l'on souhaite faire évoluer son schéma, le tout, toujours sans interruption de service. Depuis 3 ans, au sein de Mirakl, nous avons mis en place un système de montée de version sans interruption de service avec une base relationnelle. Ce talk est un retour d'expérience présentant les mécanismes que nous avons mis en place pour réaliser ces montées de version sans interruption. Il se concentre sur la partie applicative, et les problématiques engendrées par un tel process. Le but est d'être le plus concret possible, avec des exemples de 'la vraie vie', notamment quelques astuces pour réaliser ses migrations sans douleur avec des frameworks comme Hibernate ou jOOQ. Les exemples sont donnés en Java avec une base de données PostgreSQL, mais les principes s'appliquent à n'importe quel language et à la plupart des bases de données relationnelles."
  - tags:
      - "database"
      - "postgresql"
      - "performance"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Ce que les développeurs doivent savoir sur les index"
        abstract: "Les développeurs sont très souvent amenés à écrire des requêtes SQL pour communiquer avec des bases de données relationnelles. Pour les cas simples, connaître la syntaxe et le principe du SQL est amplement suffisant. Par contre, quand la volumétrie augmente et que les performances sont importantes, la question des index se pose rapidement. Bien souvent, on demande aux DBA de nous aider à indexer correctement nos tables car l'on considère que créer les index et comprendre leur fonctionnement est un travail de DBA. C'est faux ! Les développeurs connaissent le métiers des applications sur lesquelles ils travaillent, et ce sont eux les mieux placés pour comprendre quelles données doivent être indexées et comment. Ce talk présente les principes de base des index, leur fonctionnement, et comment les utiliser de manière efficace en fonction des cas d'utilisation. Il n'a pas pour but de rentrer dans un niveau de détail extrêmement pointu sur les mécanismes internes des SGBD, puisqu'il existe des DBA pour ça ! Par contre, il donne un tour d'horizon sur les notions importantes à avoir en tête en tant que développeur pour écrire des requêtes performantes et scalables. En plus de la théorie, le but est de montrer des exemples concrets d'utilisation. Pour ces exemples, nous utiliserons PostgreSQL, mais la grande majorité des concepts s'applique à la plupart des SGBD relationnels."
---

Lead Developer @Mirakl
