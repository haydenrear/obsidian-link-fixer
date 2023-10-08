
check the env

`minikube docker-env`

set docker envs:

```
DOCKPW=Goldmine423*
kubectl create secret docker-registry docker-repo \
  --docker-server=docker.io \
  --docker-username=haydenrear \
  --docker-password=DOCKPW \
  --docker-email=hayden.rear@gmail.com
```

notice secret type created is docker-registry...

then references this in the creation:

```
apiVersion: v1
kind: Pod
metadata:
  name: hello-pod1
spec:
  containers:
  - name: hello
    image: haydenrear/test:hello
  imagePullSecrets:
  - name: docker-repo

```

notice haydenrear is username, test is repo name, and hello is tag name