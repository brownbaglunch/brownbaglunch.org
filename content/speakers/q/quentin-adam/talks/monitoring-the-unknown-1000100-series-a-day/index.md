---
layout: talk
url: /speakers/quentin-adam/talks/monitoring-the-unknown-1000100-series-a-day/
tags:
- warp10
- kafka
- hadoop
- observability
- monitoring
- devops
versions:
- label: FR
  flag: fr
  title: Monitoring the unknown, 1000*100 series a day
  abstract: How to monitor unknown third party code? One of the hardest challenges
    we face running Clever Cloud, apart from the impressive scale we face with hundreds
    of new applications per week, is the monitoring of unknown tech stacks. The first
    goal of rebuilding the monitoring platform was to accommodate the immutable infrastructure
    pattern that generates lots of ephemeral hosts every minute. The traditional approach
    is to focus on VMs or hosts, not applications. We needed to shift this into an
    approach of auto-discovery of metrics to monitor, allowing third party code to
    publish new items. This talk explains our journey in building Clever Cloud Metrics
    stack, heavily based on Warp10 (Kafka/Hadoop/Storm based) to deliver developer
    efficiency and trustability to our clients applications.
---
