
# 1. POST from js(fetch)
# 2. CORS
# 3. persist data on server

# python3 server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from shows_db import showsDB
import json


class MyRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    

    def do_GET(self):
        print("the PATH is:", self.path)
        if self.path == "/shows":
            self.handleShowsRetriveCollection()
        elif self.path.startswith("/shows/"):
            self.handleShowsRetriveMember
        else:
            self.handleNotfound()

    def do_POST(self):
        if self.path == "/shows":    
            length = self.headers["Content-Length"]
            body = self.rfile.read(int(length)).decode("utf-8")
            print("BODY", body)

            parse_body = parse_qs(body)
            print("PASED BODY:", parse_body)


            name = parse_body["name"][0]
            genre = parse_body["genre"][0]
            status = parse_body["status"][0]
            rating = parse_body["rating"][0]

            db = showsDB()
            db.insertShow(name, genre, status, rating)

            self.send_response(201)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()    

        elif self.path.startswith("/shows/"):
            parts = self.path.split("/")
            shows_id = parts[2]

            db = showsDB()
            show = db.getOneShow(shows_id)

            if show != None:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(show), "utf-8"))
            else:
                self.handleNotfound()
        
        else:
            self.handleNotfound()

    def do_DELETE(self):
        parts = self.path.split('/')[1:]
        collection = parts[0]
        if len(parts) >1:
            id = parts[1]
        else:
            id = None
        db = showsDB()
        if collection == "posts":
            if id == None or db.getOneShow == None:
                self.handleNotfound()
            else:
                self.handleShowsDelete(id)
        else:
            self.handleNotfound()
        return   

    def handleNotfound(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("not found", "utf-8"))

    def handleShowsRetriveCollection(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        db = showsDB()
        shows = db.getShows()
        self.wfile.write(bytes(json.dumps(shows), "utf-8"))

    def handleShowsRetriveMember(self):
        parts = self.path.split("/")
        shows_id = parts[2]

        db = showsDB()
        shows = db.getOneShow(shows_id)

        if shows != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(shows), "utf-8"))
        else:
            self.handleNotfound()
    

    def handleShowsDelete(self, id):
        parts = self.path.split("/")
        shows_id = parts[2]

        db = showsDB()
        shows = db.getOneShow(shows_id)

        if shows != None:
            db.deleteShows(shows_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(shows), "utf-8"))
        else:
            self.handleNotfound()

def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)

    print("Listening.....")
    server.serve_forever()
    
run()