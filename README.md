# PyHealth
## Python container that monitors a draining node.

If you decided to work with any external Load balancer (like haproxy :D ) and Kubernetes, 
you surly understand that there is nothing that tells the load balancer that a node is draining (for maintainance and such).
PyHealth will monitor your nodes and will return to the load balancer check if the node is healthy or not!
### it also checks for Ingress 443 port.

just run kubectl apply -f https://raw.githubusercontent.com/RagingPuppies/PyHealth/main/DaemonSet.yml

