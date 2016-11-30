rem Runs celery workers for p-chem calculators for development mode
rem Jun. 2016; np

start celery -A celery_cts worker -Q manager --loglevel=info -n manager_worker
start celery -A celery_cts worker -Q chemaxon --loglevel=info --concurrency=1 -n chemaxon_worker
rem start celery -A celery_cts worker -Q epi --loglevel=info --concurrency=1 -n epi_worker
start celery -A celery_cts worker -Q sparc --loglevel=info --concurrency=1 -n sparc_worker
rem start celery -A celery_cts worker -Q measured --loglevel=info --concurrency=1 -n measured_worker
rem start celery -A celery_cts worker -Q test --loglevel=info --concurrency=1 -n test_worker

rem Below is the little servlet to monitor celery workers. It's not required.
rem start flower -A tasks --port=5000