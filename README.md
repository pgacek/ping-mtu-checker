## ping mtu exporter

Prometheus exporter to check the hosts ping time value with desired MTU size.

### Usage

```text
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

```text
docker run --rm -p 8080:8080 -e SERVER_PORT=8080 -e PING_HOSTS="your_favourite.host.com" -e PING_MTU_SIZES="1400,1450,1528,1529,1628,1629" pgacek/ping-mtu-exporter:v1.2.0
```

#### Example output

```text
# HELP ping_latency_milliseconds Ping time in miliseconds for hosts with different MTU sizes.
# TYPE ping_latency_milliseconds gauge
ping_latency_milliseconds{data="1272",host="google.com",ip_mtu="1300"} 11.781
ping_latency_milliseconds{data="1372",host="google.com",ip_mtu="1400"} 12.004
ping_latency_milliseconds{data="1472",host="google.com",ip_mtu="1500"} -1.0
ping_latency_milliseconds{data="1272",host="yahoo.com",ip_mtu="1300"} 174.989
ping_latency_milliseconds{data="1372",host="yahoo.com",ip_mtu="1400"} 174.762
ping_latency_milliseconds{data="1472",host="yahoo.com",ip_mtu="1500"} 175.259
ping_latency_milliseconds{data="1272",host="bing.com",ip_mtu="1300"} 13.356
ping_latency_milliseconds{data="1372",host="bing.com",ip_mtu="1400"} 12.282
ping_latency_milliseconds{data="1472",host="bing.com",ip_mtu="1500"} -1.0
```
