# Kubernetes Properties

![](link-fixer/test_files/pngs/Pasted image 20211217153646.png)
## config maps and secrets

1. create the config map or secret
2. inject them into other places

## Config Maps

### creating the config map

#### imperative

`kubectl create config-map [name of config map]  --from-file=[filename]`
`kubectl create config-map [name of config map]  --from-literal=hello=goodbye`

#### declarative

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
data:
  database_url: jdbc:postgresql://localhost/test
  user: fred
```

### mounting config map as volume

```
apiVersion: v1
kind: Pod
metadata:
  name: configured-pod
spec:
  containers:
  - image: nginx:1.19.0
    name: app
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: backend-config
```

### injecting values

#### declarative

```
apiVersion: v1
kind: Pod
metadata:
  name: configured-pod
spec:
  containers:
  - image: nginx:1.19.0
    name: app
    env:
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: backend-config
          key: database_url
    - name: USERNAME
      valueFrom:
        configMapKeyRef:
          name: backend-config
          key: user
```

check to see if envs were added

`kubectl exec [pod name] -- env`


## Secrets

### Creating Secrets

#### imperative

`kubectl create secret [generic,docker-registry,tls] [name of secret] --from-literal=hello=goodbye`
`kubectl create secret [generic,docker-registry,tls] [name of secret] --from-env-file=hello.env`

#### declarative

possible, but must base64 encode the secret value

```
apiVersion: v1
kind: Secret
metadata:
  name: db-creds
type: Opaque
data:
  pwd: czNjcmUh
```

to refer to it inside pod.yaml, change configMapKeyRef to secretRef

### mounting secret as volume

```
apiVersion: v1
kind: Pod
metadata:
  name: configured-pod
spec:
  containers:
  - image: nginx:1.19.0
    name: app
    volumeMounts:
    - name: secret-volume
      mountPath: /var/app
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: ssh-key
```


