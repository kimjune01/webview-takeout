from mcp.server.fastmcp import FastMCP
import threading
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# Initialize FastMCP server
mcp = FastMCP("webview-takeout")


@mcp.tool()
async def ping_webview_takeout() -> str:
    """Ping the webview-takeout server"""
    return "Pong webview-takeout!"


@mcp.tool()
async def create_and_serve_webview(webview_content: str) -> str:
    """Create and serve a webview with the given content in raw HTML"""
    if is_raw_html(webview_content):
        html = webview_content
    else:
        return "Webview content must be raw HTML"
    serve_html_in_webview(html)
    return "Webview created and served!"


def serve_html_in_webview(html: str, port: int = 65535):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        def log_message(self, format, *args):
            return  # Suppress logging

    server = HTTPServer(("localhost", port), Handler)

    def run_server():
        server.serve_forever()

    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    webbrowser.open(f"http://localhost:{port}/")
    time.sleep(1.5)  # Give the browser time to load
    server.shutdown()
    thread.join()


def is_raw_html(content: str) -> bool:
    stripped = content.lstrip()
    return stripped.startswith("<!DOCTYPE html") or stripped.startswith("<html")


if __name__ == "__main__":
    mcp.run()
