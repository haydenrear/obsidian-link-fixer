In this article, you will learn how to run Vault on Kubernetes and integrate it with your Spring Boot application. We will use the Spring Cloud Vault project in order to generate database credentials dynamically and inject them into the application. Also, we are going to use a mechanism that allows authenticating against Vault using a Kubernetes service account token. If this topic seems to be interesting for you it is worth reading one of my previous articles about how to run Vault on a quite similar platform as Kubernetes – Nomad. You may find it [here](https://piotrminkowski.com/2018/12/21/secure-spring-cloud-microservices-with-vault-and-nomad/).

## Why Spring Cloud Vault on Kubernetes?

First of all, let me explain why I decided to use Spring Cloud instead of Hashicorp’s Vault Agent. It is important to know that Vault Agent is always injected as a sidecar container into the application pod. So even if we have a single secret in Vault and we inject it once on startup there is always one additional container running. I’m not saying it’s wrong, since it is a standard approach on Kubernetes. However, I’m not very happy with it. I also had some problems in troubleshooting with Vault Agent. To be honest, it wasn’t easy to find my mistake in configuration based just on its logs. Anyway, Spring Cloud is an interesting alternative to the solution provided by Hashicorp. It allows you to easily integrate Spring Boot configuration properties with the Vault Database engine. In fact, you just need to include a single dependency to use it.

## Source Code

If you would like to try it by yourself, you may always take a look at my source code. In order to do that you need to clone my GitHub [repository](https://github.com/piomin/sample-spring-cloud-security.git). To see the sample application go to the `kubernetes/sample-db-vault` directory. Then you should just follow my instructions 🙂

## Prerequisites

Before we start, there are some required tools. Of course, we need to have a Kubernetes cluster locally or remotely. Personally, I use Docker Desktop, but you may use any other option you prefer. In order to run Vault on Kubernetes, we need to install [Helm](https://helm.sh/).

If you would like to build the application from the source code you need to have Skaffold, Java 17, and Maven. Alternatively, you may use a ready image from my Docker Hub account `piomin/sample-app`.

## Install Vault on Kubernetes with Helm

The recommended way to run Vault on Kubernetes is via the [Helm chart](https://www.vaultproject.io/docs/platform/k8s/helm.html). Helm installs and configures all the necessary components to run Vault in several different modes. Firstly, let’s add the HashiCorp Helm repository.

```
$ helm repo add hashicorp https://helm.releases.hashicorp.com
```

Before proceeding it is worth updating all the repositories to ensure helm uses the latest versions of the components.

```
$ helm repo update
```

Since I will run Vault in the dedicated namespace, we first need to create it.

```
$ kubectl create ns vault
```

Finally, we can install the latest version of the Vault server and run it in development mode.

```
$ helm install vault hashicorp/vault \
    --set "server.dev.enabled=true" \
    -n vault
```

We can verify the installation by displaying a list of running pods in the `vault` namespace. As you see the Vault Agent is installed by the Helm Chart, so you can try using it as well. If you wish to just go to this [tutorial](https://learn.hashicorp.com/tutorials/vault/kubernetes-sidecar?in=vault/kubernetes#set-a-secret-in-vault) prepared by HashiCorp.

```
$ kubectl get pod -n vault
NAME                                    READY   STATUS     RESTARTS   AGE
vault-0                                 1/1     Running    0          1h
vault-agent-injector-678dc584ff-wc2r7   1/1     Running    0          1h
```

## Access Vault on Kubernetes

Before we run our application on Kubernetes, we need to configure several things on Vault. I’ll show you how to do it using the `vault` CLI. The simplest way to use CLI on Kubernetes is just by getting a shell of a running Vault container:

```
$ kubectl exec -it vault-0 -n vault -- /bin/sh
```

Alternatively, we can use Vault Web Console available at the `8200` port. To access it locally we should first enable port forwarding:

```
$ kubectl port-forward service/vault 8200:8200 -n vault
```

Now, you access it locally in your web browser at `http://localhost:8200`. In order to log in there use the _Token_ method (a default token value is `root`). Then you may do the same as with the `vault` CLI but with the nice UI.

![vault-kubernetes-ui-login](https://i0.wp.com/piotrminkowski.com/wp-content/uploads/2021/12/Screenshot-2021-12-30-at-10.47.44.png?resize=300%2C154&ssl=1)

## Configure Kubernetes authentication

Vault provides a [Kubernetes authentication](https://www.vaultproject.io/docs/auth/kubernetes.html) method that enables clients to authenticate with a Kubernetes service account token. This token is available to every single pod. Assuming you have already started an interactive shell session on the `vault-0` pod just execute the following command:

```
$ vault auth enable kubernetes
```

In the next step, we are going to configure the Kubernetes authentication method. We need to set the location of the Kubernetes API, the service account token, its certificate, and the name of the Kubernetes service account issuer (required for Kubernetes 1.21+).

```
$ vault write auth/kubernetes/config \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
    token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
    issuer="https://kubernetes.default.svc.cluster.local"
```

Ok, now very important. You need to understand what happened here. We need to create a Vault policy that allows us to generate database credentials dynamically. We will enable the Vault database engine in the next section. For now, we are just creating a policy that will be assigned to the authentication role. The name of our Vault policy is `internal-app`:

```
$ vault policy write internal-app - <<EOF
path "database/creds/default" {
  capabilities = ["read"]
}
EOF
```

The next important thing is related to the Kubernetes RBAC. Although the Vault server is running in the `vault` namespace our sample application will be running in the `default` namespace. Therefore, the service account used by the application is also in the default namespace. Let’s create `ServiceAccount` for the application:

```
$ kubectl create sa internal-app
```

Now, we have everything to do the last step in this section. We need to create a Vault role for the Kubernetes authentication method. In this role, we set the name and location of the Kubernetes `ServiceAccount` and the Vault policy created in the previous step.

```
$ vault write auth/kubernetes/role/internal-app \
    bound_service_account_names=internal-app \
    bound_service_account_namespaces=default \
    policies=internal-app \
    ttl=24h
```

After that, we may proceed with the next steps. Let’s enable the Vault database engine.

## Enable Vault Database Engine

Just to clarify, we are still inside the `vault-0` pod. Let’s enable the Vault `database` engine.

```
$ vault secrets enable database
```

Of course, we need to run a database on Kubernetes. We will PostgreSQL since it is supported by Vault. The full deployment manifest is available on my GitHub repository in `/kubernetes/k8s/postgresql-deployment.yaml`. Here’s just the `Deployment` object:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:latest
          imagePullPolicy: "IfNotPresent"
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: POSTGRES_PASSWORD
                  name: postgres-secret
          volumeMounts:
            - mountPath: /var/lib/postgresql/data
              name: postgredb
      volumes:
        - name: postgredb
          persistentVolumeClaim:
            claimName: postgres-claim
```

Let’s apply the whole manifest to deploy Postgres in the `default` namespace:

```
$ kubectl apply -f postgresql-deployment.yaml
```

Following Vault documentation, we first need to configure a plugin for the PostgreSQL database and then provide connection settings and credentials:

```
$ vault write database/config/postgres \
    plugin_name=postgresql-database-plugin \
    allowed_roles="default" \
    connection_url="postgresql://{{username}}:{{password}}@postgres.default:5432?sslmode=disable" \
    username="postgres" \
    password="admin123"
```

I have disabled SSL for connection with Postgres by setting the property `sslmode=disable`. There is only one role allowed to use the Vault PostgresSQL plugin: `default`. The name of the role should be the same as the name passed in the field `allowed_roles` in the previous step. We also have to set a target database name and SQL statement that creates users with privileges. We set the max TTL of the lease to 10 minutes just to present revocation and renewal features of Spring Cloud Vault. It means that 10 minutes after your application has started it can no longer authenticate with the database.

```
$ vault write database/roles/default db_name=postgres \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";GRANT USAGE,  SELECT ON ALL SEQUENCES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1m" \
    max_ttl="10m"
```

And that’s all on the Vault server side. Now, we can test our configuration using a vault CLI as shown below. You can log in to the database using returned credentials. By default, they are valid for one minute (the `default_ttl` parameter in the previous command).

```
$ vault read database/creds/default
```

We can also verify a connection to the instance of PostgreSQL in Vault UI:

![](https://i0.wp.com/piotrminkowski.com/wp-content/uploads/2021/12/Screenshot-2021-12-30-at-14.44.49.png?resize=768%2C524&ssl=1)

Now, we can generate new credentials just by renewing the Vault lease (`vault lease renew LEASE_ID`). Hopefully, Spring Cloud Vault does it automatically for our app. Let’s see how it works.

## Use Spring Cloud Vault on Kubernetes

For the purpose of this demo, I created a simple Spring Boot application. It exposes REST API and connects to the PostgreSQL database. It uses Spring Data JPA to interact with the database. However, the most important thing here are the following two dependencies:

```
<dependency>
  <groupId>org.springframework.cloud</groupId>
  <artifactId>spring-cloud-starter-bootstrap</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.cloud</groupId>
  <artifactId>spring-cloud-vault-config-databases</artifactId>
</dependency>
```

The first of them enables `bootstrap.yml` processing on the application startup. The second of them include Spring Cloud Vault Database engine support.

The only thing we need to do is to provide the right configuration settings Here’s the minimal set of the required dependencies to make it work without any errors. The following configuration is provided in the `bootstrap.yml` file:

```
spring:
  application:
    name: sample-db-vault
  datasource:
    url: jdbc:postgresql://postgres:5432/postgres 
  jpa:
    hibernate:
      ddl-auto: update
  cloud:
    vault:
      config.lifecycle: 
        enabled: true
        min-renewal: 10s
        expiry-threshold: 30s
      kv.enabled: false 
      uri: http://vault.vault:8200 
      authentication: KUBERNETES 
      postgresql: 
        enabled: true
        role: default
        backend: database
      kubernetes: 
        role: internal-app
```

Let’s analyze the configuration visible above in the details:

**(1)** We need to set the database connection URI, but WITHOUT any credentials. Assuming our application uses standard properties for authentication against the database (`spring.datasource.username` and `spring.datasource.password`) we don’t need to anything else

**(2)** As you probably remember, the max TTL for the database lease is 10 minutes. We enable lease renewal every 30 seconds. Just for the demo purpose. You will see that Spring Cloud Vault will create new credentials in PostgreSQL every 30 seconds, and the application still works without any errors

**(3)** Vault KV is not needed here, since I’m using only the database engine

**(4)** The application is going to be deployed in the default namespace, while Vault is running in the vault namespace. So, the address of Vault should include the namespace name

**(5) (7)** Our application uses the Kubernetes authentication method to access Vault. We just need to set the role name, which is `internal-app`. All other settings should be left with the default values

**(6)** We also need to enable `postgres` database backend support. The name of the backend in Vault is `database` and the name of Vault role used for that engine is `default`.

## Run Spring Boot application on Kubernetes

The Deployment manifest is rather simple. But what is important here – we need to use the `ServiceAccount` `internal-app` used by the Vault Kubernetes authentication method.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app-deployment
spec:
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: sample-app
        image: piomin/sample-app
        ports:
        - containerPort: 8080
      serviceAccountName: internal-app
```

Our application requires Java 17. Since I’m using Jib Maven Plugin for building images I also have to override the default base image. Let’s use `openjdk:17.0.1-slim-buster`.

```
<plugin>
  <groupId>com.google.cloud.tools</groupId>
  <artifactId>jib-maven-plugin</artifactId>
  <version>3.1.4</version>
  <configuration>
    <from>
      <image>openjdk:17.0.1-slim-buster</image>
    </from>
  </configuration>
</plugin>
```

The repository is configured to easily deploy the application with Skaffold. Just go to the `/kubernetes/sample-db-vault` directory and run the following command in order to build and deploy our sample application on Kubernetes:

```
$ skaffold dev --port-forward
```

After that, you can call one of the REST endpoints to test if the application works properly:

```
$ curl http://localhost:8080/persons
```

Everything works fine? In the background, Spring Cloud Vault creates new credentials every 30 seconds. You can easily verify it inside the PostgreSQL container. Just connect to the `postgres` pod and run the `psql` process:

```
$ kubectl exec svc/postgres -i -t -- psql -U postgres
```

Now you can list users with the `\du` command. Repeat the command several times to see if the credentials have been regenerated. Of course, the application is able to renew the lease until the max TTL (10 minutes) is not exceeded.

![](https://i0.wp.com/piotrminkowski.com/wp-content/uploads/2021/12/Screenshot-2021-12-30-at-14.18.12.png?resize=768%2C123&ssl=1)