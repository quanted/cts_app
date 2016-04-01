start celery --app=tasks:app worker -Q test --loglevel=info --concurrency=1 -n test_worker
start celery --app=tasks:app worker -Q chemaxon --loglevel=info --concurrency=8 -n chemaxon_worker
start celery --app=tasks:app worker -Q epi --loglevel=info --concurrency=8 -n epi_worker
start celery --app=tasks:app worker -Q sparc --loglevel=info --concurrency=1 -n sparc_worker
start celery --app=tasks:app worker -Q measured --loglevel=info --concurrency=1 -n measured_worker

rem python manage.py celery --app=tasks:app worker -Q chemaxon --loglevel=info --concurrency=8 -n chemaxon_worker
rem python manage.py celery multi start 2 -Q:1 test -Q:2 chemaxon -c:1 1 -c:2 8 -n:1 test_worker -n:2 chemaxon_worker

exit 0