import subprocess
import re
import http.server
import os
import threading
import time
import argparse
from urllib.parse import urlparse
from prometheus_client import Gauge, generate_latest

# Set defaults using argparse
parser = argparse.ArgumentParser(description="Ping hosts with different MTU sizes and expose as Prometheus metrics.")
parser.add_argument('--hosts', type=str,
                    help='Comma-separated list of hosts to ping.',
                    default=os.environ.get('PING_HOSTS', "google.com,yahoo.com,bing.com"))
parser.add_argument('--mtu_sizes', type=str,
                    help='Comma-separated list of MTU sizes.',
                    default=os.environ.get('PING_MTU_SIZES', "1390,1420,1520"))
args = parser.parse_args()

hosts = args.hosts.split(',')
mtu_sizes = [int(size) for size in args.mtu_sizes.split(',')]

# Prometheus metric setup
PING_STATUS = Gauge('ping_latency_milliseconds',
                    'Ping status for hosts with different MTU sizes.',
                    ['host', 'mtu_size'])

def ping_host_with_mtu(host, mtu_size):
    try:
        result = subprocess.check_output(
            # IP header: 20 bytes
            # ICMP header: 8 bytes
            # Total: 28 bytes
            ["ping", "-c", "1", "-M", "do", "-s", str(mtu_size-28), host],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        # Extract the time value from the output
        time_match = re.search(r"time=(\d+\.\d+) ms", result)
        if time_match:
            return float(time_match.group(1))
        else:
            return 0
    except subprocess.CalledProcessError:
        return -1


def update_metrics():
    while True:
        for host in hosts:
            for mtu_size in mtu_sizes:
                result = ping_host_with_mtu(host, mtu_size)
                PING_STATUS.labels(host=host, mtu_size=str(mtu_size)).set(result)

        time.sleep(10)

class MetricsHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/metrics":
            metrics_page = generate_latest()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(metrics_page)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    # Start the background thread for pinging
    threading.Thread(target=update_metrics, daemon=True).start()

    PORT = int(os.environ.get('SERVER_PORT', 8080))
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, MetricsHandler)
    print(f"Serving metrics at port {PORT}")
    httpd.serve_forever()
