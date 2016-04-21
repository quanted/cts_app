# Names of nodes to start
#   most people will only start one node:
CELERYD_NODES="test_worker chemaxon_worker epi_worker sparc_worker measured_worker manager_worker"
#   but you can also start multiple and configure settings
#   for each in CELERYD_OPTS (see `celery multi --help` for examples):
#CELERYD_NODES="worker1 worker2 worker3"
#   alternatively, you can specify the number of nodes to start:
CELERYD_NODES=6

# Absolute or relative path to the 'celery' command:
# CELERY_BIN="/usr/local/bin/celery"
CELERY_BIN="/var/www/ubertool/virtualenv/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="cts_celery"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
CELERYD_CHDIR="/var/www/ubertool/ubertool_cts"

# Extra command-line arguments to the worker
CELERYD_OPTS="-Q:1 test -c:1 1 -n:1 test_worker \
	-Q:2 chemaxon -c:2 8 -n:2 chemaxon_worker \
	-Q:3 epi -c:3 8 -n:3 epi_worker \
	-Q:4 sparc -c:4 1 -n:4 sparc_worker \
	-Q:5 measured -c:5 1 -n:5 measured_worker \
	-Q:6 manager -n:6 manager_worker"

# %N will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%N.log"
CELERYD_PID_FILE="/var/run/celery/%N.pid"

# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists, e.g. nobody).
CELERYD_USER="celery"
CELERYD_GROUP="celery"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1