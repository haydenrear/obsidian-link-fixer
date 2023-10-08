# Syntax

![](link-fixer/test_files/pngs/Pasted image 20220626093823.png)
# Applying Labels

```
kubectl run alpaca-prod \
  --image=gcr.io/kuar-demo/kuard-amd64:blue \
  --replicas=2 \
  --labels="ver=1,app=alpaca,env=prod"
```

## show labels

`kubectl get deployments --show-labels`

can modify labels after deployment also

# Selectors

## Usages

- network policies
- replica sets

a way to select based on labels

`kubectl get pods --selector="ver=2"`

## Boolean expressions

`kubectl get pods --selector="app in (alpaca,bandicoot)"`

![](link-fixer/test_files/pngs/Pasted image 20220626094104.png)
# Annotations

Provide info to libraries about what an object is, where it came from, policy of object, etc.

```
When in doubt, add information to an object as an annotation and promote it to a label if you find yourself wanting to use it in a selector.
```

*Annotations are saved as a string, and not validated at any point by kubernetes*

![](link-fixer/test_files/pngs/Pasted image 20220626094509.png)

