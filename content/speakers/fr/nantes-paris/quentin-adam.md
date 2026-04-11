---
name: "Quentin ADAM"
since: "2019-02-03"
city: "fr/nantes-paris"
cities:
  - "fr/paris"
  - "fr/nantes"
tags:
  - "cloud-computing"
  - "paas"
  - "devops"
  - "postgres"
  - "sql"
  - "database"
  - "nosql"
  - "functional-programing"
  - "code"
  - "cloud"
  - "container"
  - "docker"
  - "linux"
  - "virtualization"
  - "systemd"
  - "scala"
  - "warp10"
  - "kafka"
  - "hadoop"
  - "observability"
  - "monitoring"
picture: "https://i.imgur.com/YdzlEj0.jpg"
contacts:
  x: "waxzce"
  mail: "quentin.adam@clever-cloud.com"
websites:
  - name: "Web"
    url: "http://www.waxzce.org"
  - name: "LinkedIn"
    url: "http://fr.linkedin.com/in/waxzce"
  - name: "GitHub"
    url: "https://github.com/waxzce"
sessions:
  - tags:
      - "cloud-computing"
      - "paas"
      - "devops"
    versions:
      - label: "FR"
        flag: "fr"
        title: "C'est quoi Clever Cloud et comment ça marche ?"
        abstract: "Une rapide demo de Clever Cloud et de pourquoi on l'a construit et comment. L'idée est de découvrir le fonctionnement de l'outil afin d'envisager si ça peut être utile et rendre les devs plus efficaces et heureux. En fonction du temps, une explication de comment ça marche est possible."
  - tags:
      - "postgres"
      - "sql"
      - "database"
      - "nosql"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Why postgres SQL deserve noSQL fan respect"
        abstract: "Postgres SQL is a plain old SQL DB. Very powerful and very consistent, in some case, project needs an ACID database, but schemaless… With JSON support, postgres is a very interesting tool to provide ACID and some very interesting function (time management, localisation function and data types…) and the schemaless noSQL point of view with json and indexed json. This talk show some great usage and some insigth to build some great application with postgres."
  - tags:
      - "functional-programing"
      - "code"
      - "devops"
      - "cloud"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Immutability: from code to infrastructure, the way of scalability"
        abstract: "The all functional programming world, Docker, Clever Cloud, micro service architecture, logs append only DB… All of this rely on the immutability at some point: infrastructure immutability, data immutability, append only. This is the way we now build some of the best scalable applications and infrastructure. The talk is made to understand why Immutability rules the scalability and why it’s important."
  - tags:
      - "devops"
      - "container"
      - "docker"
      - "linux"
      - "virtualization"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Containers, VMs, Processes… Isolation, performances, I/O… How all of these technologies work and compare to each other? Deep dive and learn about your Operating System."
        abstract: "Everybody is now using virtualization, containers are all the rage today, and microkernels start to gain traction… But how is all this working? How did these solutions come to be? What are the differences between containers and virtual machines? Where and why should you use docker, runc, rocket, kvm, xen, virtualbox, includeOS, rancherOS? This talk is a full session providing understanding on how these technologies work, how they compare to each other, and lot’s of demo to understand differences and fundamental concept on isolation. So, let’s look under the hood, and understand how your system works (hint: it’s not magic). And yes, it will be understandable even if you are not an OPS or an expert. That’s precisely the point."
  - tags:
      - "devops"
      - "linux"
      - "systemd"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Comment ça marche systemd déjà ? "
        abstract: "Après la grande guerre initd et systemd, il est clair que maintenant systemd s’est imposé. Pourquoi ? Quels sont les intérêts ? Est ce difficile de faire un fichier de configuration systemd ? Comment ça marche ? Comment écrire un fichier de conf ? Comment gérer des CRONs avec ?"
  - tags:
      - "scala"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Scala Implicits: pour faire des APIs simples, des DSL ou de la magie noire, ça marche comment ?"
        abstract: "C’est quoi un implicit ? Pourquoi ça existe dans le langage ? Le lien au DSL (au fait c’est quoi un DSL) ? Construire une API en les utilisant… Ce talk est un 101 des implicits dans le scala."
  - tags:
      - "warp10"
      - "kafka"
      - "hadoop"
      - "observability"
      - "monitoring"
      - "devops"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Monitoring the unknown, 1000*100 series a day"
        abstract: "How to monitor unknown third party code? One of the hardest challenges we face running Clever Cloud, apart from the impressive scale we face with hundreds of new applications per week, is the monitoring of unknown tech stacks. The first goal of rebuilding the monitoring platform was to accommodate the immutable infrastructure pattern that generates lots of ephemeral hosts every minute. The traditional approach is to focus on VMs or hosts, not applications. We needed to shift this into an approach of auto-discovery of metrics to monitor, allowing third party code to publish new items. This talk explains our journey in building Clever Cloud Metrics stack, heavily based on Warp10 (Kafka/Hadoop/Storm based) to deliver developer efficiency and trustability to our clients applications."
  - tags: []
    versions:
      - label: "FR"
        flag: "fr"
        title: "Any other talk?"
        abstract: "Yes, sure, read here https://evman.clever-cloud.com/public/user/9"
---

CEO chez Clever Cloud
