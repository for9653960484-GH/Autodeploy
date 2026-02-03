import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def summ(a, b):
    return a + b


def mult(a, b):
    return a * b


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/summ", "/mult"):
            query = parse_qs(parsed.query)
            try:
                a = float(query.get("a", [None])[0])
                b = float(query.get("b", [None])[0])
            except (TypeError, ValueError):
                self.send_response(400)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    b"Provide numeric query params a and b. Example: /summ?a=2&b=3\n"
                )
                return

            result = summ(a, b) if parsed.path == "/summ" else mult(a, b)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"{result}\n".encode("utf-8"))
            return

        message = "OK: container test app is running\n" f"Path: {self.path}\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def log_message(self, fmt, *args):
        # Keep logs simple in container output.
        print(f"{self.client_address[0]} - {fmt % args}")


def main():
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
