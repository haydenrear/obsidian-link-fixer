Create a role, and a role binding

![](link-fixer/test_files/pngs/Pasted image 20220626111107.png)
# Create Role

```
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: default
  name: pod-and-services
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["create", "delete", "get", "list", "patch", "update", "watch"]
```

# Create Role Binding

```
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: default
  name: pods-and-services
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: alice
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: mydevs
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-and-services
```

# Cluster Role & Cluster Role Binding
Create roles for entire cluster

## Built-in

`kubectl get clusterroles`

## Transience
![](link-fixer/test_files/pngs/Pasted image 20220626111034.png)


# Verbs

![](link-fixer/test_files/pngs/Pasted image 20220626110929.png)

# Testing Auth

```
kubectl auth can-i create pods
kubectl auth can-i get pods --subresource=logs
```

# Aggregation Rules


![](link-fixer/test_files/pngs/Pasted image 20220626111256.png)

# Groups

Use groups instead of assigning roles to individuals

![](link-fixer/test_files/pngs/Pasted image 20220626111441.png)

we may be creating internal infernals for light people.

