# Install
```
$ curl -fsSL -o get_helm.sh \
https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```

![](link-fixer/test_files/pngs/Pasted image 20220625192244.png)
# Run
https://artifacthub.io/

## Repo
in the future, will support docker container registries to hold helm?

## Add Repo
```
$ helm repo add bitnami https://charts.bitnami.com/bitnami
"bitnami" has been added to your repositories
```

## Check Repos
```
$ helm repo list
NAME    URL
bitnami https://charts.bitnami.com/bitnami
```

### Search Repo
```
$ helm search repo drupal
NAME            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/drupal  7.0.0           9.0.0           One of the most versatile open...
```

## Install

command is 
`helm install [name of installation] [installation name in repo]`

```
$ helm install mysite bitnami/drupal
Error: cannot re-use a name that is still in use
```

need to add a name for the installation bc you can have multiple installations of same 

### Install to kubernetes namespace

```
$ kubectl create ns first
$ kubectl create ns second
$ helm install --namespace first mysite bitnami/drupal
$ helm install --namespace second mysite bitnami/drupal
```

## Upgrade
```
$ helm repo update [![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492083641/files/assets/1.png)](https://learning.oreilly.com/library/view/learning-helm/9781492083641/ch02.html#callout_using_helm_CO1-1)
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈ Happy Helming!⎈

$ helm upgrade mysite bitnami/drupal [![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492083641/files/assets/2.png)](https://learning.oreilly.com/library/view/learning-helm/9781492083641/ch02.html#callout_using_helm_CO1-2)
```


```
$ helm upgrade mysite bitnami/drupal --version 6.2.22
```


```
$ helm install mysite bitnami/drupal --values values.yaml 
$ helm upgrade mysite bitnami/drupal
```


### Uninstall

`helm uninstall mysite`

# Dry-Run

![](link-fixer/test_files/pngs/Pasted image 20220626084257.png)
`$ helm install mysite bitnami/drupal --values values.yaml --set drupalEmail=foo@example.com --dry-run`

# Template

people used dry run as a way to print out the data to paste into kubernetes, but it requires credentials, produces different output if used on install / upgrade, etc.

![](link-fixer/test_files/pngs/Pasted image 20220626085447.png)
![](link-fixer/test_files/pngs/Pasted image 20220626085544.png)
```
helm template mysite bitnami/drupal --values values.yaml --set \
drupalEmail=foo@example.com
```

