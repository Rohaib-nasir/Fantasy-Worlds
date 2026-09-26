from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


APP_DIR = Path(__file__).resolve().parent
API_BASE = "http://127.0.0.1:8000"
ALLOWED_API_PREFIXES = ("/worlds", "/world/")


class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/worlds" or path.startswith("/world/"):
            self._proxy_request()
            return
        super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path == "/predict":
            self._proxy_request()
            return
        self.send_error(404)

    def _proxy_request(self):
        path = urlsplit(self.path).path
        if not any(path == prefix or path.startswith(prefix) for prefix in ALLOWED_API_PREFIXES) and path != "/predict":
            self.send_error(404)
            return

        body = self.rfile.read(int(self.headers.get("Content-Length", "0"))) if self.command == "POST" else None
        request = Request(
            f"{API_BASE}{unquote(self.path)}",
            data=body,
            headers={"Content-Type": self.headers.get("Content-Type", "application/json")},
            method=self.command,
        )
        try:
            with urlopen(request, timeout=60) as response:
                status = response.status
                payload = response.read()
                content_type = response.headers.get("Content-Type", "application/json")
        except HTTPError as error:
            status = error.code
            payload = error.read()
            content_type = error.headers.get("Content-Type", "application/json")
        except URLError as error:
            payload = ("{\"detail\":\"Model API is unavailable: " + str(error.reason).replace('"', "'") + "\"}").encode("utf-8")
            status = 502
            content_type = "application/json"

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 5500), AppHandler)
    print("Fantasy Worlds UI: http://127.0.0.1:5500")
    print("Forwarding API requests to: " + API_BASE)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping frontend server.")
        server.server_close()
