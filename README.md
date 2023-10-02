## ping mtu exporter

Prometheus exporter to check the hosts ping time value with desired MTU size.

### Usage

```json
usage: main.py [-h] [--hosts HOSTS] [--mtu_sizes MTU_SIZES] [--subtract_headers]

Ping hosts with different MTU sizes and expose as Prometheus metrics.

options:
  -h, --help            show this help message and exit
  --hosts HOSTS         Comma-separated list of hosts to ping.
  --mtu_sizes MTU_SIZES
                        Comma-separated list of MTU sizes.
  --subtract_headers    Subtract 28 bytes from MTU size while pinging
```

### Run with docker

It's possible to change the default http server(5000) by setting environment variable `SERVER_PORT`

```json
docker run --rm -p 8080:8080 -e SERVER_PORT=8080 -e PING_HOSTS="your_favourite.host.com" -e PING_MTU_SIZES="1400,1450,1528,1529,1628,1629" pgacek/ping-mtu-exporter:v1.2.0
```

#### Example output

```json
# HELP ping_latency_milliseconds Ping time in miliseconds for hosts with different MTU sizes.
# TYPE ping_latency_milliseconds gauge
ping_latency_milliseconds{host="google.com",mtu_size="1300",payload="1272"} -1.0
ping_latency_milliseconds{host="google.com",mtu_size="1400",payload="1372"} -1.0
ping_latency_milliseconds{host="google.com",mtu_size="1500",payload="1472"} -1.0
ping_latency_milliseconds{host="google.com",mtu_size="1600",payload="1572"} -1.0
ping_latency_milliseconds{host="yahoo.com",mtu_size="1300",payload="1272"} -1.0
ping_latency_milliseconds{host="yahoo.com",mtu_size="1400",payload="1372"} -1.0
ping_latency_milliseconds{host="yahoo.com",mtu_size="1500",payload="1472"} -1.0
ping_latency_milliseconds{host="yahoo.com",mtu_size="1600",payload="1572"} -1.0
ping_latency_milliseconds{host="bing.com",mtu_size="1300",payload="1272"} 29.6
ping_latency_milliseconds{host="bing.com",mtu_size="1400",payload="1372"} 25.9
```
