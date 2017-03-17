# Beringei

Beringei is a high performance time series storage engine. Time series are commonly used as a representation of statistics, gauges, and counters for monitoring performance and health of a system.
 
It's an OpenSource project from facebook, you can read more about it here : https://github.com/facebookincubator/beringei

# Beringei-HTTP-Interface

After following Facebook-Beringei instructions for sure you have asked yourself, how on earth I'm going to use this ? Executing binaries is the last thing that I really need to do.

And this is why I've built this simple http interface.

# How It Works

- Start beringei.

```
$ ./beringei/service/beringei_main \
    -beringei_configuration_path /tmp/beringei.json \
    -create_directories \
    -sleep_between_bucket_finalization_secs 60 \
    -allowed_timestamp_behind 300 \
    -bucket_size 600 \
    -buckets $((86400/600)) \
    -logtostderr \
    -v=2
```

- Set the compiled beringei bins path in the config.ini
```
[beringei]
bin_path=/tmp/beringei/build/beringei/tools/
config_file=/tmp/beringei.json
```

- Start the HTTP Interface
```
$ uwsgi --http-socket 0.0.0.0:7777 ./uwsgi.ini
```

# Use It
- PUT Keys
```
$ curl "172.17.0.13:7777/put" -F "KEY=testkey" -F "VALUE=54321"
{"status": "ok"}
$ curl "172.17.0.13:7777/put" -F "KEY=testkey" -F "VALUE=54444"
{"status": "ok"}
```
- GET Keys

SORTED=1/0,ASC=1/0 (Default = 0)
```
$ curl "172.17.0.13:7777/get?KEY=testkey&SORTED=1&ASC=1" 
{"1488659898": "54321", "1488660223": "54444"}
```