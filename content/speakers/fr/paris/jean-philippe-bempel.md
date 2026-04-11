---
name: "Jean-Philippe Bempel"
since: "2014-05-12"
city: "fr/paris"
cities:
  - "fr/paris"
tags:
  - "mechanical-sympathy"
  - "cpu"
  - "jvm"
  - "low-latency"
  - "performance"
  - "gc"
  - "memoire"
  - "jit"
  - "lock-free"
  - "metriques"
  - "diagnostic"
  - "clr"
  - "shenandoah"
  - "azul-c4"
  - "z-gc"
picture: "https://pbs.twimg.com/profile_images/1019190216995811328/YARM51Fl_400x400.jpg"
contacts:
  x: "jpbempel"
  mail: "jp.bempel@criteo.com"
websites:
  - name: "Web"
    url: "http://jpbempel.blogspot.com"
  - name: "LinkedIn"
    url: "http://fr.linkedin.com/in/jeanphilippebempel"
sessions:
  - tags:
      - "mechanical-sympathy"
      - "cpu"
      - "jvm"
      - "low-latency"
      - "performance"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Low Latency & Mechanical Sympathy : écueils et solutions"
        abstract: "Une application de connexion aux marchés financiers requiert une performance accrue. Le traitement des ordres se mesure en centaines de microsecondes, parfois moins. A partir du moment où l'on descend sous la barre de la milliseconde, on entre dans un domaine où la connaissance du matériel (CPU) et des sous-systèmes mémoire devient prépondérante : Il est nécessaire d'être en harmonie avec le matériel (Mechanical Sympathy). Quels sont les plus gros problèmes pour optimiser un traitement inférieur à la milliseconde ? Cette présentation donnera les clés pour répondre à cette question et un retour d'expérience sur l'application de ces optimisations."
  - tags:
      - "jvm"
      - "gc"
      - "memoire"
      - "performance"
    versions:
      - label: "FR"
        flag: "fr"
        title: "OutOfMemoryError : Quel est le coût des objets en Java"
        abstract: "A Ullink, nos Heaps sont habituellement plutôt large (jusqu'à 256 Go) et nous gérons un large volume de données. Mais nous avons observé que la majorité de l'espace occupé dans la Heap ne l'est pas par les données business mais par les structures ! Dans cette présentation il sera montré quel est le coût des objets, quels sont les suspects idéals dans nos structures de données habituelles (Lists, Maps, Strings) et ce que nous pouvons faire pour réduire l'empreinte mémoire."
  - tags:
      - "cpu"
      - "jit"
      - "jvm"
      - "lock-free"
      - "performance"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Programmation Lock-Free : les techniques des pros"
        abstract: "La scalabilité des applications est une préoccupation importante. Beaucoup de pertes en scalabilité proviennent de code contenant des locks qui produisent une importante contention en cas de forte charge. Dans cette présentation nous allons aborder différentes techniques (striping, copy-on-write, ring buffer, spinning, ...) qui vont nous permettre de réduire cette contention ou d'obtenir un code sans lock. Nous expliquerons aussi les concepts de Compare-And-Swap et de barrières mémoires."
  - tags:
      - "jvm"
      - "performance"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Coding & Performance : un parcours initiatique"
        abstract: "Lorsque l'on entre dans le domaine de la performance, un non-initié peut se retrouver perdu parmi les règles empiriques (rule of thumbs), les grand O, les benchmarks et autres optimisations prématurées. Cette présentation propose d'aider le développeur à acquérir les connaissances et l'expérience nécessaire pour affronter les défis permanents que posent l'élaboration et la maintenance d'une application performante."
  - tags:
      - "jvm"
      - "gc"
      - "metriques"
      - "diagnostic"
      - "performance"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Le guide de dépannage de la JVM"
        abstract: "Votre application Java/Scala/autres en production ne répond plus ! Que faire pour diagnostiquer le problème ? Un thread bloqué ? le CPU à 100% ? le GC part en vrille ? Une OutOfMemoryError ? Par où commencer ? Cette présentation vous donnera les outils et la méthodologie pour être capable de gérer cette situation. Vous verrez les informations et métriques fournis par la JVM ainsi que la bonne façon de les interpréter."
  - tags:
      - "jvm"
      - "clr"
      - "jit"
      - "gc"
      - "performance"
    versions:
      - label: "FR"
        flag: "fr"
        title: "CLR-JVM différences d'implémentation"
        abstract: "Chez Criteo, nous utilisons à la fois la .NET CLR et la JVM. A première vue il semble que ces 2 runtimes sont similaires: du byte code, un JIT, un GC, ... Mais en fait il y a des différences dans l'implementation et dans la vision des applications ciblées et leurs besoins. Nous verrons les avantages et inconvénients des différences de ces 2 runtimes."
  - tags:
      - "jvm"
      - "gc"
      - "shenandoah"
      - "azul-c4"
      - "z-gc"
      - "performance"
    versions:
      - label: "FR"
        flag: "fr"
        title: "Comprendre les GC à faible latence de la JVM"
        abstract: "Depuis quelques années, le monde du GC sur la JVM évolue. Une nouvelle catégorie de GC émerge: Les GC à faible latence (low latency). Shenandoah est mis à disposition par Red Hat, Oracle a mis en open Source ZGC dans l'OpenJDK depuis le JDK 11 et Azul C4 est toujours là. Comme les GC 'classiques' sont plutôt bien compris maintenant, cette présentation s'attardera sur les arcanes des plus récents. Nous allons expliquer le concurrent marking (tri-color marking), la Load Value Barrier de C4, les Brooks pointers de Shenandoah et le multi-mapping de ZGC. Enfin, comment choisir son GC à faible latence ?"
---

Développeur passionné par les performances, les runtimes (JVM, CLR) et adepte de Mechanical Sympathy, Jean-Philippe Bempel a plus de 8 ans d'expérience dans les systèmes de trading low latency. Maintenant il apporte son expertise sur la JVM chez Criteo afin d'optimiser les resources sur des clusters d'applications de plusieurs milliers de noeuds.
