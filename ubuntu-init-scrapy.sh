#!/bin/sh

# Install instructions (do as 'sudo'):
# cp ubuntu-init-scrapy.sh /etc/init.d/scrapyd
# chmod +x /etc/init.d/scrapyd

start() {
    log_daemon_msg "Starting scrapyd server: "
    /usr/local/bin/scrapyd &
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
