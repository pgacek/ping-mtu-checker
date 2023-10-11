import subprocess
import re
import http.server
import os
import threading
import time
import argparse
import logging
from urllib.parse import urlparse
from prometheus_client import Gauge, generate_latest

# Set up logging
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Set defaults using argparse
parser = argparse.ArgumentParser(description="Ping hosts with different MTU sizes and expose as Prometheus metrics.")
parser.add_argument('--hosts', type=str,
                    help='Comma-separated list of hosts to ping.',
                    default=os.environ.get('PING_HOSTS', "google.com,yahoo.com,bing.com"))
parser.add_argument('--mtu_sizes', type=str,
                    help='Comma-separated list of MTU sizes.',
                    default=os.environ.get('PING_MTU_SIZES', "1300,1400,1500"))
args = parser.parse_args()

hosts = args.hosts.split(',')
mtu_sizes = [int(size) for size in args.mtu_sizes.split(',')]

# Prometheus metric setup
PING_STATUS = Gauge('ping_latency_milliseconds',
                    'Ping time in miliseconds for hosts with different MTU sizes.',
                    ['host', 'ip_mtu', 'data'])


def ping_host_with_mtu(host, mtu_size):
    try:
        process = subprocess.Popen(
            ["ping", "-c", "1", "-M", "do", "-s", str(mtu_size - 28), host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(returncode=process.returncode, cmd=process.args, output=stdout,
                                                stderr=stderr)

        max_time_match = re.search(r"rtt min/avg/max/mdev = [\d.]+/[\d.]+/([\d.]+)/[\d.]+ ms", stdout)
        if max_time_match:
            return float(max_time_match.group(1))
        else:
            logging.info(
                f"Failed to extract max ping time for {host} with MTU size {mtu_size}. Unexpected ping output: {stdout}")
            return -1


    except subprocess.CalledProcessError as e:
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            combined_error = f"stdout: {e.output}, stderr: {e.stderr}"
            logging.error(f"Failed to ping {host} with MTU size {mtu_size}. Error: {combined_error}")
        else:
            logging.info(f"Failed to ping {host} with MTU size {mtu_size}.")
        return -1


def update_metrics():
    while True:
        for host in hosts:
            for mtu_size in mtu_sizes:
                try:
                    result = ping_host_with_mtu(host, mtu_size)
                    PING_STATUS.labels(
                        host=host,
                        ip_mtu=str(mtu_size),
                        data=str(mtu_size - 28)).set(result)
                except Exception as e:
                    logging.error(f"Error updating metrics for {host} with MTU size {mtu_size}: {e}")

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

    PORT = int(os.environ.get('SERVER_PORT', 5000))
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, MetricsHandler)
    logging.info(f"Serving metrics at port {PORT}")
    httpd.serve_forever()
