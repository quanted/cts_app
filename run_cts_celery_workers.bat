start celery -A celery_cts worker -Q manager --loglevel=info -n manager_worker
rem start celery -A celery_cts worker -Q test --loglevel=info --concurrency=1 -n test_worker
start celery -A celery_cts worker -Q chemaxon --loglevel=info --concurrency=1 -n chemaxon_worker

start celery -A celery_cts worker -Q epi --loglevel=info --concurrency=1 -n epi_worker
start celery -A celery_cts worker -Q sparc --loglevel=info --concurrency=1 -n sparc_worker
start celery -A celery_cts worker -Q measured --loglevel=info --concurrency=1 -n measured_worker

rem start flower -A tasks --port=5000