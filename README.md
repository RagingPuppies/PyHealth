# PyHealth
## Python container that monitors a draining node.

If you decided to work with any external Load balancer (like haproxy :D ) and Kubernetes, 
you surly understand that there is nothing that tells the load balancer that a node is draining (for maintainance and such).
PyHealth will monitor your nodes and will return to the load balancer check if the node is healthy or not!
### it also checks for Ingress 443 port.



## Step 1 - Create Service Account and Permissions
- Apply the following YAML (kubectl apply -f /path/to/yaml.yml)


In the above YAML file, first, we create a ServiceAccount which provides an identity for processes that run in a Pod, our process is a python code that query the kubernetes API to check the node status.
then we create ClusterRole which is a set of permission we allow, afterwards,
we Bind the account with the permissions with ClusterRoleBinding.

## Step 2 - Create the Daemon-Set app
- Apply the following YAML (kubectl apply -f /path/to/yaml.yml)



just run `kubectl apply -f https://raw.githubusercontent.com/RagingPuppies/PyHealth/main/DaemonSet.yml`

Once installed each of the worker nodes IPs will listen to port 10555 and will return one of the statuses: healthy, IngressDown, Draining.

