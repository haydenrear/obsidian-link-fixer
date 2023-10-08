# Why

External Traffic - either LoadBalancer or NodePort.

ClusterIP < NodeIP < LoadBalancer

Points to a service > pod > container > image x n (includes sidecar sometimes)

# What
Creates a load balancer per service

# How

Update spec from ClusterIP to LoadBalancer