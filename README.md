# Webhook-poc
## Overview
- Create TLS Certificates for Client & Server
- Create webhook-server which invokes a /mutate API when webhook enabled pod is created
- Deploy webhook
- Deploy MutatingWebhookConfiguration
- Mount GPU cluster node local disk path /mnt/disk1/data(which is pointing to minio service bucket) to persistent volume & pesistent volume claim to access it
- Create a test pod to with volume mounts to verify if /mnt/disk1/data can be accessed within the newly created pod container at run time

## Webhook Configuration
- Refer to this github link [mutating-webhook](https://github.com/adityajoshi12/kubernetes-development/tree/main/mutating-webhook) to create client and server certificates.

#### CA Certificates
The following commands generate ca.key and ca.crt used while calling webhook /mutate API

```bash
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 365 -key ca.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=Acme Root CA" -out ca.crt
```

#### Issue TLS certificates
Generate server side TLS certifcates for `webhook service` with name `mutationwebhook`

```bash
export SERVICE=mutationwebhook
openssl req -newkey rsa:2048 -nodes -keyout tls.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=$SERVICE.default.svc.cluster.local" -out tls.csr
openssl x509 -req -extfile <(printf "subjectAltName=DNS:$SERVICE.default.svc.cluster.local,DNS:$SERVICE.default.svc.cluster,DNS:$SERVICE.default.svc,DNS:$SERVICE.default.svc,DNS:$SERVICE.default,DNS:$SERVICE") -days 365 -in tls.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out tls.crt
```

#### Create TLS kubernetes Secret
Upload server side certificates (tls.crt & tls.key) to webhook pod volume `tls`

```bash
kubectl create secret tls tls --cert=tls.crt --key=tls.key
```

#### Docker images 
Use the following docker build and push commands to generate a docker image with webhook service /mutate API 

```bash
docker build -t <ACR_NAME>.azurecr.io/mutationwebhook:latest -f Dockerfile .
docker push <ACR_NAME>.azurecr.io/mutationwebhook:latest

kubectl apply -f deployment.yaml
```

#### MutatingWebhookConfiguration
Replace `CA-CERT` placeholder for base64 encoded tls certificate and apply webhook
```bash
CA_CERT=$(cat tls.crt | base64 | tr -d '\n')
sed "s@CA-CERT@$CA_CERT@g" mutating.yaml > webhook.yaml

kubectl apply -f webhook.yaml
```
#### PV & PVC
```bash
kubectl apply -f minio-pv.yaml
kubectl apply -f minio-pvc.yaml
```

### Verify Mounted Path with Test Pod
Create a test pod to access local mount path /mnt/disk1/data through pvc

```bash
kubectl apply -f test-pod.yaml
kubectl describe pod test-pod
```

