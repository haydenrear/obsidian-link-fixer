# Get IP for Pod

```
ALPACA_POD=$(kubectl get pods -l app=alpaca-prod \
    -o jsonpath='{.items[0].metadata.name}')
kubectl port-forward $ALPACA_POD 48858:8080
```



## Running Container Easy Way

### create pod
`kubectl run hello --image=haydenrear/test:hello --port=8080 run/v1`

add -o yaml to create a dc
add --env="key=value" to add environmentals
add --labels="key=value,key1=value1" to add csv of labels

add init command:

`kubectl run mypod --image=busybox -o yaml --dry-run=client --restart=Never \
  > pod.yaml -- /bin/sh -c "while true; do date; sleep 10; done"`


the generator part makes it so it runs as replication controller instead of deployment
you may need to update to local docker repo

or declarative: 

```
apiVersion: v1
kind: Pod
metadata:
  name: hazelcast
  labels:
    app: hazelcast
    env: prod
spec:
  containers:
  - env:
    - name: DNS_DOMAIN
      value: cluster
    image: hazelcast/hazelcast
    name: hazelcast
    ports:
    - containerPort: 5701
  restartPolicy: Never
```

### create anything else

`kubectl create ...`

### Viewing

`kubectl get pods`
`kubectl get services`
`kubectl get nodes`
`kubectl get [object]`
`kubectl cluster-info`
`kubectl logs [pod name]`

### Accessing Pods

This is done through creating a service

`kubectl expose pod hello --type=LoadBalancer --name hello-http`

rc stands for replication controller
the type must be LoadBalancer, because if not, then it would not be accessible from outside the cluster, like the pod it providing access to

`kubectl create secret generic regcred --from-file=.dockerconfigjson=/Users/hayde/.docker/config.json --type=kubernetes.io/dockerconfigjson`

or
	
`kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v1/ --docker-username=haydenrear --docker-password=Goldmine423* --docker-email=hayden.rear@gmail.com`

5bfa68bb-230e-48c4-b646-074151a8c714

### executing inside pod:

`kubectl exec -it [pod name] /bin/sh`


## Editing 

`kubectl edit pod [name of pod]`

### also can replace

`kubectl replace -f [yaml dc]`
`kubectl apply -f [yaml dc]`

## Port Forwarding

If we want to access a service in Kubernetes, we need to open the port according to the following:

`kubectl port-forward service/vault 8200:8200 -n vault`

where vault is the name of the service ... i.e.

![](link-fixer/test_files/pngs/Pasted image 20220116101538.png)
# Run Command in Container

## interactive shell
`kubectl exec -it [pod name] --bash`

## attach

`kubectl attach -it [pod name]`


# Copy Files To Container

`kubectl cp <pod-name>:</path/to/remote/file> </path/to/local/file>`


# Get Events from Kubernetes Cluster

`kubectl get events`


