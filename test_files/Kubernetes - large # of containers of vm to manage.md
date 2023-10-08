---

_Created at 2020-08-16T16:37:39-04:00._
_Last updated at 2020-08-16T18:33:42-04:00._




---

# Kubernetes - large # of containers of vm to manage


_**Kubernetes - large # of containers of vm to manage**_

_run containers of vm - "container orchestration"_

*   _load balancing_
*   _node pools_
*   _automatic scaling & updating_
*   _autohealing_ 
*   _stackdriver monitoring_

_kubernetes architecture_

**pods -** encapsulate, run container(s) - usually just one container
**deployments -** multiple pods w/ some options
**services -** access pod through service - ensure IP (static) associated with pod (dynamic: created and destroyed according to health)

_kubernetes storage objects_

**persistent volumes -** unit of storage outside of pod keep track of state
**persistent volume claims -** data structure allow pod to access volume, work with data in volume. (pointer to storage for pod to access)

_deplyoing kubernetes cluster using cloud shell_

```
gcloud container clusters create [nameOfCluster] [nameOfZone i.e. --zone=us-west1-b] [go to next line with '\'] [machineType i.e. --machine=type-n1-standard-1] [diskSize in GB i.e. --disk-size=100]
```

_see list of active clusters_

```
gcloud container clusters list
```

_deploying applications (workloads) into kubernetes cluster_

applications run in containers - can run app stored in cloud repository, github, bitbucket, or existing, such as nginx
workloads -> deploy

_kubectl - "kube control" - adjusting things within kubernetes cluster_
oppose this with doing operations on a cluster, for which we use google cloud abstraction api for kubernetes

![](CS/_resources/Kubernetes_-_large_#_of_containers_of_vm_to_manage.resources/unknown_filename.png)
_stackdrive kubernetes engine monitoring_
kubernetes engine -> clusters -> clusters -> check stack driver kubernetes engine monitoring within Details tab
legacy stackdriver kubernetes engine monitor disabled is correct configuration

search bar monitor -> stack driver monitoring -> resources -> kubernetes engine -> drop down to see nodes -> each node usually means one instance (vm) -> each node has multiple pods
from stackdriver above switch do workloads tab -> see which applications or "workloads" are running -> nodes and pods associated
from stackdrive above switch to services -> high level apps that are running

