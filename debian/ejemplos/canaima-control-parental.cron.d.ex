#
# Regular cron jobs for the canaima-control-parental package
#
0 4	* * *	root	[ -x /usr/bin/canaima-control-parental_maintenance ] && /usr/bin/canaima-control-parental_maintenance
