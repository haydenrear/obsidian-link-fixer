# Security Context

"A security context defines privilege and access control settings for a Pod or a container."

i.e.

"""
-   The user ID that should be used to run the Pod and/or container.
    
-   The group ID that should be used for filesystem access.
    
-   Granting a running process inside the container some privileges of the root user but not all of them.
"""

<b>is not a kubernetes primitive</b>

only something to be applied at pod level..

```
apiVersion: v1
kind: Pod
metadata:
  name: non-root
spec:
  containers:
  - image: nginx:1.18.0
    name: secured-container
    securityContext:
      runAsNonRoot: true
```

can also, under security context, set fs-group (file-system group), wherein if the pod creates file, then group number (i.e. 3500) will be assigned to it.