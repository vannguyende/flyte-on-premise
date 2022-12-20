# create tempalte config file in path ".flyte/config.yaml"
IP=$(kubectl -n ingress-nginx get svc| grep NodePort|  awk '{print $4}')
PORT=$(kubectl describe service -n ingress-nginx| grep -i nodeport| grep -i https| awk '{print $3}'| grep -o '[0-9]\+')
ADDRESS=$IP:$PORT
yes | flytectl config init --host=$ADDRESS

# replace content of config file
cat << EOF > ~/.flyte/config.yaml
admin:
  endpoint: dns:///$ADDRESS
  authType: Pkce
  insecure: false
  insecureSkipVerify: true
logger:
  show-source: true
  level: 0
EOF