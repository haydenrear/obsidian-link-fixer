## Kubernetes consists of
1. control plane
2. master node
	1. hosts control plane
3. worker nodes

![](/Users/hayde/Library/Mobile Documents/iCloud~md~obsidian/Documents/Hayden/hello/IMG_1345.png)

![](link-fixer/test_files/pngs/Pasted image 20211217100735.png)
### Control Plane

-   The _Kubernetes API Server_, which you and the other Control Plane components communicate with
-   The _Scheduler_, which schedules your apps (assigns a worker node to each deployable component of your application)
-   The _Controller Manager_, which performs cluster-level functions, such as replicating components, keeping track of worker nodes, handling node failures, and so on
-   _etcd_, a reliable distributed data store that persistently stores the cluster configuration.


![](link-fixer/test_files/pngs/Pasted image 20211217100959.png)
### Kubernetes Controllers

"""
a high level, a controller in Kubernetes terms is software that watches resources and takes action to synchronize or enforce a specific state (either the desired state or reflecting the current state as a status). Kubernetes has many controllers, which generally “own” a specific object type or specific operation.
"""

#### kube-controller-manager

includes multiple controllers that manage the Kubernetes network stack
![](link-fixer/test_files/pngs/Pasted image 20220105103915.png)
### Kubelet

single binary runs on every node in cluster
manages pods that are scheduled to the node, and provides updates on them.

1. Kubernetes scheduler watches for pod and determines if node exists to schedule to, based on constraints such as CPU/memory request constraing, etc.
2. When finds one, it schedules the pod to the node.
3. kubelet watching to see if pod scheduled but not created creates it once it observes, and makes call to CNI plugin to add pod to network


