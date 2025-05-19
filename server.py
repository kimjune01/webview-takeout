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
    """Create and serve a webview with the given content (JSX or raw HTML)"""
    if is_raw_html(webview_content):
        html = webview_content
    else:
        html = react_jsx_to_html(webview_content)
    serve_html_in_webview(html)
    return "Webview created and served!"


def react_jsx_to_html(jsx_code: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>React Webview</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  </head>
  <body>
    <div id="root"></div>
    <script type="text/babel">
{jsx_code}
      ReactDOM.createRoot(document.getElementById('root')).render(<MemoryGame />);
    </script>
  </body>
</html>
"""


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
