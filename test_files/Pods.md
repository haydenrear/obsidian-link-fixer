# What are Pods
- smallest deployment unit
- can contain multiple containers (sidecar).
- apps in pods share same ip, port space, hostname, and communicate through interprocess comms

# Pod Scheduling
- once scheduled to a node, pods can't be moved - must be explicitly destroyed and rescheduled.
- kubernetes tries to schedule on separate machines if more than one replica, but may schedule on one machine

# Running Pods
`kubectl run kuard --generator=run-pod/v1 --image=gcr.io/kuar-demo/kuard-amd64:blue`

## from a manifest
```
apiVersion: v1
kind: Pod
metadata:
  name: kuard
spec:
  containers:
    - image: gcr.io/kuar-demo/kuard-amd64:blue
      name: kuard
      ports:
        - containerPort: 8080
          name: http
          protocol: TCP
```

then 

`kubectl apply -f kuard-pod.yaml`

# Delete pod

`kubectl delete pods/kuard`

## from file

`kubectl delete -f kuard-pod.yaml`


# Get Logs from Pod

`kubectl logs kuard`


# Resources

![](link-fixer/test_files/pngs/Pasted image 20220626093041.png)
can also specify gpu resources


# Volumes

## Types of volumes

NFS, iSCSI, cloud storage, git, cache

## Mounting a server (cloud)

![](link-fixer/test_files/pngs/Pasted image 20220626093434.png)
