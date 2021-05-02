from kubernetes import client, config
import os
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

parser = argparse.ArgumentParser(description='Small tool to check Kubernetes node is draining.')
parser.add_argument('--port',  help='port of the server')
args = parser.parse_args()




class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.status = self.check_node_status()
        self.wfile.write(bytes(self.status,"utf-8"))

    def do_GET(self):
        self._set_response()
        
    def log_message(self, format, *args):
        return
    
    def check_node_status(self):

        node_name = os.getenv('NODE_NAME')

        config.load_incluster_config()

        v1 = client.CoreV1Api()

        node_info = v1.read_node(name=node_name)

        node_status = node_info.spec.unschedulable
        
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        location = ("localhost", 443)
        
        ingress_check = a_socket.connect_ex(location)        
        if ingress_check != 0:
            return "IngressDown"
        if node_status == None:
            return "healthy"
        if node_status == True:
            return "DrainActive"

            
def run(server_class=HTTPServer, handler_class=S, port=int(args.port)):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    run()