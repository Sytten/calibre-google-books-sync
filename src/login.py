import webbrowser
from threading import Thread

from PyQt5.Qt import QObject, pyqtSignal

from polyglot.queue import Queue
from polyglot.http_server import HTTPServer, SimpleHTTPRequestHandler
from polyglot.urllib import urlencode, urlparse, parse_qs

from calibre_plugins.google_books_sync.src.utils.security import generate_token
from calibre_plugins.google_books_sync.src.utils.http import post, parse_json


class GoogleLoginRequestHandler(SimpleHTTPRequestHandler):
    QUEUE = Queue()
    CLOSE_HTML = get_resources("assets/html/close.html")

    def do_GET(self):
        # Fetch the code
        href = urlparse(self.path)
        data = parse_qs(href.query)

        code = data.get("code")
        if code:
            self.QUEUE.put("code:{}".format(code[0]))
        else:
            error = data.get("error", "Unknown error")
            self.QUEUE.put("error:{}".format(error))

        # Send response to the user
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.CLOSE_HTML)


class GoogleLoginServer:
    def __init__(self, port):
        # TODO: Have a list of ports if this one is already taken
        self.server = HTTPServer(("", port), GoogleLoginRequestHandler)
        self.thread = None

    def start(self):
        self.thread = Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.server.shutdown()

    def get_code(self):
        return GoogleLoginRequestHandler.QUEUE.get()


class GoogleLogin(QObject):
    success = pyqtSignal(str)
    failure = pyqtSignal(str)

    def __init__(self):
        # TODO: Allow customization by the user if they want to use their own application
        # and not rely on mine.
        self.server_port = 5464
        self.client_id = (
            "260273173690-658moqlj2ica52521jhqm10bush8fro9.apps.googleusercontent.com"
        )
        self.client_secret = "Lf12hiJ8PJ9a5xDajI8NDMYK"
        self.scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/books",
        ]
        self.thread = None

    def start(self):
        self.thread = Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        # Start the background server to receive the code
        server = GoogleLoginServer(self.server_port)
        server.start()

        try:
            # Natigate user to the login page
            code_challenge = generate_token()
            url = self._get_login_url(code_challenge)
            webbrowser.open(url)

            # Retrieve and handle the code
            code = server.get_code()
            self._handle_code(code, code_challenge)
        finally:
            server.stop()

    def _handle_code(self, code, code_verifier):
        status, value = code.split(":")

        if status != "code":
            # TODO: Send failure signal and log properly
            print("ERROR")
            return

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": value,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "redirect_uri": "http://127.0.0.1:{}".format(self.server_port),
        }
        res = post("oauth2.googleapis.com", "/tokens", payload)
        data = parse_json(res)
        print(data)

    def _get_login_url(self, code_challenge):
        query_string = urlencode(
            {
                "client_id": self.client_id,
                "redirect_uri": "http://127.0.0.1:{}".format(self.server_port),
                "response_type": "code",
                "scope": " ".join(self.scopes),
                "code_challenge": code_challenge,
                "code_challenge_method": "plain",
            }
        )

        return "https://accounts.google.com/o/oauth2/v2/auth?" + query_string
