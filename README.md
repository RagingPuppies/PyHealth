# PyHealth
## Python container that monitors a draining node.

If you decided to work with any external Load balancer (like haproxy :D ) and Kubernetes, 
you surly understand that there is nothing that tells the load balancer that a node is draining (for maintainance and such).
PyHealth will monitor your nodes and will return to the load balancer check if the node is healthy or not!
### it also checks for Ingress 443 port.



## Step 1 - Create Service Account and Permissions
- Apply the following YAML
`kubectl apply -f https://raw.githubusercontent.com/RagingPuppies/PyHealth/main/Roles.yml`


In the above YAML file, first, we create a ServiceAccount which provides an identity for processes that run in a Pod, our process is a python code that query the kubernetes API to check the node status.
then we create ClusterRole which is a set of permission we allow, afterwards,
we Bind the account with the permissions with ClusterRoleBinding.

## Step 2 - Create the Daemon-Set app
- Apply the following YAML
`kubectl apply -f https://raw.githubusercontent.com/RagingPuppies/PyHealth/main/DaemonSet.yml`


following YAML containing the app container, healthcheck probs and more, what special here is the "serviceAccountName: py-node-health" which direct the pod to use our newly created account and "hostNetwork: true" which sets the Pod to communicate directly with the node network, therefore the Pod IP will be the Node IP, so access to the service will be direct from the nodes IP and the app listening port which is 10555.


Once deployed, check the following url: http://Node_IP:10555
it should return "healthy", if for any reason there is no output, check the pod logs.
will return one of the statuses: healthy, IngressDown, Draining.


## Step 3 - Set HAPROXY health check
Now that we have the health checks service up and running, let's configure the load balancer.
At the backend of our service we would like to change the way we check the service,
we need to create a new health check, change the port of the check and set intervals:
edit /etc/haproxy/haproxy.cfg in the HAPROXY servers:

```
backend ingress
    balance roundrobin
    option log-health-checks
    option httpchk GET / HTTP/1.1\r\n
    http-check expect string healthy
    server worker1 1.2.3.4:443  ssl verify none alpn h2,http/1.1 check port 10555 fall 3 rise 2 inter 10s
    server worker2 2.3.4.5:443  ssl verify none alpn h2,http/1.1 check port 10555 fall 3 rise 2 inter 10s
```
- **option httpchk** creates http health check and construct the call
- **http-check** sets what to expact from the result, we expact the string 'healthy'
- **check port 10555 fall 3 rise 2 inter 10s** at the end of the server sets the port and intervals

afterwards, reload the proxy
`service haproxy reload`
