import http.server
import random
import time

from itertools import cycle

class RandomNotification:
    last_update_time = 0
    status_cycle = cycle([1, 0, 1])  # Keep this as an iterator
    current_status = next(status_cycle)  # Initialize the current status
    priority = random.choice(["HIGH", "MEDIUM", "LOW"])

    @classmethod
    def update_if_needed(cls):
        current_time = time.time()
        if current_time - cls.last_update_time >= 60:  # Check if 60 seconds have passed
            cls.current_status = next(cls.status_cycle) 
            cls.priority = random.choice(["HIGH", "MEDIUM", "LOW"])
            cls.last_update_time = current_time


    def __str__(self):
        return f";{self.current_status};{self.priority};"


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/nce-rest/arduino-status/aod-open-notifications":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            RandomNotification.update_if_needed()
            response = RandomNotification()
            print(response)
            self.wfile.write(str(response).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            response = "404 Not Found"
            self.wfile.write(response.encode())


def run_server():
    host = "schreckhorn"
    port = 8080
    server_address = (host, port)

    try:
        server = http.server.HTTPServer(server_address, MyHandler)
        print(f"Server started at http://{host}:{port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")


if __name__ == "__main__":
    run_server()
