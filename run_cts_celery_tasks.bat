start celery --app=tasks:app worker -Q manager --loglevel=info -n manager_worker
start celery --app=tasks:app worker -Q test --loglevel=info --concurrency=1 -n test_worker
start celery --app=tasks:app worker -Q chemaxon --loglevel=info --concurrency=8 -n chemaxon_worker

start flower -A tasks --port=5000

rem start celery --app=tasks:app worker -Q epi --loglevel=info --concurrency=8 -n epi_worker
rem start celery --app=tasks:app worker -Q sparc --loglevel=info --concurrency=1 -n sparc_worker
rem start celery --app=tasks:app worker -Q measured --loglevel=info --concurrency=1 -n measured_worker