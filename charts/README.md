## 1. Deployment
### 1.1. Flyte sandbox (locally)

#### 1.1.1. Install flytectl by shell script and set environment path**

    curl -sL https://ctl.flyte.org/install | bash
    export PATH=$HOME/bin:$PATH

#### 1.1.2. create cluster
* step 1. start flyte sandbox cluster 
 
      start sandbox by flytectl

* step 2: set env path for kube config and flytectl config 
    *Note: you can copy this variable in logs console after sandbox start.* 

       export KUBECONFIG=$KUBECONFIG:/<path_to>/.kube/config:/<path>/.flyte/k3s/k3s.yaml
       export FLYTECTL_CONFIG=/<path_to>/.flyte/config-sandbox.yaml

* Step 3: Open this url (http://localhost:30081/console) on your browser.**
### 1.2. Flyte Native (AWS)

#### 1.2.1. Deploy cluster 

Step 1: Follow [deployment flyte docs](https://docs.flyte.org/en/latest/deployment/aws/manual.html#deployment-aws-manual) to install some dependences

Step 2: Setting env variable

    export CHART_PATH=<path-to-charts-directory>

Step 3: Install spark-operator:

    helm install -n spark-operator -f $CHART_PATH/spark-operator-chart/values.yaml spark-operator $CHART_PATH/spark-operator-chart --create-namespace

Step 4: Install ingress nginx

4.1. Label node

    kubectl label node <name_node> runingress=nginx

4.2. Lnstall chart

    helm install -n ingress-nginx --create-namespace ingress-nginx  -f values.yaml . 

Step 5: Installing Flyte.

    helm install -n flyte -f $CHART_PATH/flyte-core/values-eks-all.yaml --create-namespace flyte $CHART_PATH/flyte-core/


