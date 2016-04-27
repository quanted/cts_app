start celery -A celery_cts worker -Q manager --loglevel=info -n manager_worker
start celery -A celery_cts worker -Q test --loglevel=info --concurrency=1 -n test_worker
start celery -A celery_cts worker -Q chemaxon --loglevel=info --concurrency=8 -n chemaxon_worker

start celery -A celery_cts worker -Q epi --loglevel=info --concurrency=8 -n epi_worker
start celery -A celery_cts worker -Q sparc --loglevel=info --concurrency=1 -n sparc_worker
start celery -A celery_cts worker -Q measured --loglevel=info --concurrency=1 -n measured_worker

start flower -A tasks --port=5000