# Kubernetes Process When Run 

![](link-fixer/test_files/pngs/Pasted image 20211217110141.png)
1. REST request to ReplicationController
2. ReplicationController create pod, which then scheduled to worker node by Scheduler
3. Kubelet on node saw scheduled pod and instruct go get Docker image


