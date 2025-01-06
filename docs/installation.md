# Installation Guide

# This setup needs a Kubernetes cluster and helm cli setup to connect to the Kubernetes cluster

# Add bitnami helm repo
```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

# Install/Upgrade Kafka 
```sh
helm upgrade --install kafka -f helm/kafka-values.yaml bitnami/kafka --namespace=kafka --create-namespace
```

# Install/Upgrade Apache Flink
```sh
helm upgrade --install flink -f helm/flink-min-values.yaml bitnami/flink --namespace=flink --create-namespace
```
