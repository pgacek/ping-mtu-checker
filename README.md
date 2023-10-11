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

#### Disclaimer
Running this code directly on MacOS may show you the error like this:
`ERROR - Failed to ping bing.com with MTU size 1400. Error: stdout: , stderr: ping: invalid message: 'd'`

That's because MacOS's ping is different from the on Linux, especially the `-M` parameter

MacOS
```commandline
ping
usage: ping [-AaDdfnoQqRrv] [-c count] [-G sweepmaxsize]
            [-g sweepminsize] [-h sweepincrsize] [-i wait]
            [-l preload] [-M mask | time] [-m ttl] [-p pattern]
            [-S src_addr] [-s packetsize] [-t timeout][-W waittime]
            [-z tos] host
       ping [-AaDdfLnoQqRrv] [-c count] [-I iface] [-i wait]
            [-l preload] [-M mask | time] [-m ttl] [-p pattern] [-S src_addr]
            [-s packetsize] [-T ttl] [-t timeout] [-W waittime]
            [-z tos] mcast-group
Apple specific options (to be specified before mcast-group or host like all options)
            -b boundif           # bind the socket to the interface
            -k traffic_class     # set traffic class socket option
            -K net_service_type  # set traffic class socket options
            --apple-connect       # call connect(2) in the socket
            --apple-time          # display current time
```

Linux
```commandline
ping --help
ping: invalid option -- '-'

Usage
  ping [options] <destination>

Options:
  <destination>      dns name or ip address
  -a                 use audible ping
  -A                 use adaptive ping
  -B                 sticky source address
  -c <count>         stop after <count> replies
  -D                 print timestamps
  -d                 use SO_DEBUG socket option
  -f                 flood ping
  -h                 print help and exit
  -I <interface>     either interface name or address
  -i <interval>      seconds between sending each packet
  -L                 suppress loopback of multicast packets
  -l <preload>       send <preload> number of packages while waiting replies
  -m <mark>          tag the packets going out
  -M <pmtud opt>     define mtu discovery, can be one of <do|dont|want>
  -n                 no dns name resolution
  -O                 report outstanding replies
  -p <pattern>       contents of padding byte
  -q                 quiet output
  -Q <tclass>        use quality of service <tclass> bits
  -s <size>          use <size> as number of data bytes to be sent
  -S <size>          use <size> as SO_SNDBUF socket option value
  -t <ttl>           define time to live
  -U                 print user-to-user latency
  -v                 verbose output
  -V                 print version and exit
  -w <deadline>      reply wait <deadline> in seconds
  -W <timeout>       time to wait for response

IPv4 options:
  -4                 use IPv4
  -b                 allow pinging broadcast
  -R                 record route
  -T <timestamp>     define timestamp, can be one of <tsonly|tsandaddr|tsprespec>

IPv6 options:
  -6                 use IPv6
  -F <flowlabel>     define flow label, default is random
  -N <nodeinfo opt>  use icmp6 node info query, try <help> as argument

For more details see ping(8).
```
