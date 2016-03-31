python manage.py celery --app=tasks:app worker -Q test --loglevel=info --concurrency=1 -n test_worker
REM python manage.py celery --app=tasks:app worker -Q chemaxon --loglevel=info --concurrency=8 -n chemaxon_worker &

rem python manage.py celery multi start 2 -Q:1 test -Q:2 chemaxon -c:1 1 -c:2 8 -n:1 test_worker -n:2 chemaxon_worker
