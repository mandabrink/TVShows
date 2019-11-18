
# 1. POST from js(fetch)
# 2. CORS
# 3. persist data on server

# python3 server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import Cookies
from urllib.parse import parse_qs
from shows_db import showsDB
from session_store import SessionStore
import json

SESSION_STORE = SessionStore()

class MyRequestHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    # goal: load cookie into self.cookie
    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = Cookies.SimpleCookie(self.headers(["Cookie"]))

        else:
            self.cookie = Cookies.SimpleCookie()

    #def send_SimpleCookie(self):
    # put send_cookie before every send.header in this file
    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())
        pass

    # goal: load session into self.session 
    def load_session(self):
        self.load_cookie()
        # if session ID is in the cookie
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            # if session ID exists in the session store
            # save the session for use later (data member)
            self.session = SESSION_STORE.getSession(sessionId)


            #otherwise, if session ID is NOT in the session store
            if self.session == None:
                #create a new session
                sessionId = SESSION_STORE.createSession() 
                self.session = SESSION_STORE.getSession(sessionId)
                # set the new session ID into the cookie
                self.cookie["sessionId"] = sessionId
            

        # otherwise, if session ID is ont in the cookie
        else:
            #create a new session
            sessionId = SESSION_STORE.createSession()
            self.session = SESSION_STORE.getSession(sessionId) 
            # set the new session ID into the cookie
            self.cookie["sessionId"] = sessionId

    def do_OPTIONS(self):
        self.load_cookie()
        self.send_response(200)
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
        self.load_cookie()
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
            self.end_headers()    

        elif self.path.startswith("/shows/"):
            parts = self.path.split("/")
            shows_id = parts[2]

            db = showsDB()
            show = db.getOneShow(shows_id)

            if show != None:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(show), "utf-8"))
            else:
                self.handleNotfound()
        
        else:
            self.handleNotfound()

    def do_PUT(self):
        self.load_cookie()
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
            shows_id = parse_body["id"][0]

            db = showsDB()
            db.editShows(shows_id, name, genre, status, rating)

            self.send_response(201)
            self.end_headers()    
        
        else:
            self.handleNotfound()

    def do_DELETE(self):
        self.load_cookie()
        parts = self.path.split('/')[1:]
        collection = parts[0]
        print(parts)
        if len(parts) > 1:
            id = parts[1]
        else:
            id = None
        db = showsDB()
        if collection == "shows":
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
        self.load_cookie()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        db = showsDB()
        shows = db.getShows()
        self.wfile.write(bytes(json.dumps(shows), "utf-8"))

    def handleShowsRetriveMember(self):
        self.load_cookie()
        parts = self.path.split("/")
        shows_id = parts[2]

        db = showsDB()
        shows = db.getOneShow(shows_id)

        if shows != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(shows), "utf-8"))
        else:
            self.handleNotfound()
    

    def handleShowsDelete(self, id):
        self.load_cookie()
        if "userId" not in self.session:
            self.send_response(401)
            return 

        
        parts = self.path.split("/")
        shows_id = parts[2]

        db = showsDB()
        shows = db.getOneShow(shows_id)

        if shows != None:
            db.deleteShows(shows_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
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