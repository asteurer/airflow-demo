#!/bin/zsh

# Install the CRDs
kubectl apply -f https://github.com/spinkube/spin-operator/releases/download/v0.2.0/spin-operator.crds.yaml

# Install the Runtime Class
# The commented line below installs the default runtime class; however, when there are node pools, this needs to be altered
# kubectl apply -f https://github.com/spinkube/spin-operator/releases/download/v0.2.0/spin-operator.runtime-class.yaml
# Altered runtime class
kubectl apply -f spin-operator.runtime-class.yaml

# Install cert-manager CRDs
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.3/cert-manager.crds.yaml

# Add and update Jetstack repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install the cert-manager Helm chart
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.14.3

# Add Helm repository if not already done
helm repo add kwasm http://kwasm.sh/kwasm-operator/
helm repo update

# Install KWasm operator
helm install \
  kwasm-operator kwasm/kwasm-operator \
  --namespace kwasm \
  --create-namespace \
  --set kwasmOperator.installerImage=ghcr.io/spinkube/containerd-shim-spin/node-installer:v0.14.1

# Provision Nodes
kubectl annotate node --all kwasm.sh/kwasm-node=true

# Inspect logs from the Kwasm Operator
kubectl logs -n kwasm -l app.kubernetes.io/name=kwasm-operator

helm install spin-operator \
  --namespace spin-operator \
  --create-namespace \
  --version 0.2.0 \
  --wait \
  oci://ghcr.io/spinkube/charts/spin-operator

# Create the namespace in which your spin apps will be running
kubectl create namespace spin-apps

# The shim-executor needs to be installed in the same namespace as the spin apps
kubectl apply -f https://github.com/spinkube/spin-operator/releases/download/v0.2.0/spin-operator.shim-executor.yaml -n spin-apps

