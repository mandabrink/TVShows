# 1. POST from js(fetch)
# 2. CORS
# 3. persist data on server

# python3 server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json


class MyRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print("the PATH is:", self.path)
        if self.path == "/shows":
            data_look = open("textfile.txt", "r")
            data_read = (data_look.readlines())
            data_look.close()
            # respond accordingly
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            # send a body
            self.wfile.write(bytes(json.dumps(data_read), "utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            pass
            # 404

    def do_POST(self):
        if self.path == "/shows":    
            data_send = open("textfile.txt", "a")
               
            length = self.headers["Content-Length"]
            # read the body (data)
            body = self.rfile.read(int(length)).decode("utf-8")
            print("BODY", body)
            # TODO: parse the body string into a dictionary using parse-qs()
            parse_body = parse_qs(body)
            print("PASED BODY:", parse_body)
            # TODO: save the restaurant into our list of restaurants
            name = parse_body["name"]
            data_send.write(name+"\n")
            data_send.close()
            # respond to the client
            self.send_response(201)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()        
        
        else:
            pass


def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)

    print("Listening.....")
    server.serve_forever()
    
run()