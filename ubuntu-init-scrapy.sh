#!/bin/sh

[ -f /etc/default/scrapyd ] && . /etc/default/scrapyd

if [ -z "$SCRAPY_FEED_URI" ] ;  then
  echo "SCRAPY_FEED_URI is not set, please set it in /etc/default/scrapyd" >&2
  exit 1
fi

if [ -z "$SCRAPY_AWS_ACCESS_KEY_ID" ] ;  then
  echo "SCRAPY_AWS_ACCESS_KEY_ID is not set, please set it in /etc/default/scrapyd" >&2
  exit 1
fi

if [ -z "$SCRAPY_AWS_SECRET_ACCESS_KEY" ] ;  then
  echo "SCRAPY_AWS_SECRET_ACCESS_KEY is not set, please set it in /etc/default/scrapyd" >&2
  exit 1
fi

echo $SCRAPY_FEED_URI
echo $SCRAPY_AWS_ACCESS_KEY_ID
echo $SCRAPY_AWS_SECRET_ACCESS_KEY

start() {
    log_daemon_msg "Starting scrapyd server: "
    (export SCRAPY_FEED_URI=$SCRAPY_FEED_URI; export SCRAPY_AWS_ACCESS_KEY_ID=$SCRAPY_AWS_ACCESS_KEY_ID; 
        export SCRAPY_AWS_SECRET_ACCESS_KEY=$SCRAPY_AWS_SECRET_ACCESS_KEY; bash -c '/usr/local/bin/scrapyd' &)
    log_daemon_msg "Scrapyd server startup"
}

stop() {
    log_daemon_msg "Stopping scrapyd server: "
    kill $(pgrep scrapyd)
}

# Source init functions
. /lib/lsb/init-functions

case "$1" in
    start)
        start
	;;
    stop)
	stop
	;;
    restart|reload|condrestart)
        stop
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac
exit 0
