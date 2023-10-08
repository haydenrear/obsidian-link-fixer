# Why

Exposing services to outside of cluster.

# What

Pick a port for the service, and then all traffic to the cluster that comes through that port comes to that service.

# How

```
kubectl edit service [service name]
```

And then edit the spec.type to NodePort

or when you create a service using `kubectl expose` specify `--type=NodePort`

