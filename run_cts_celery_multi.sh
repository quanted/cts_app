#!/bin/sh

celery multi start 5 \
	-Q:1 test -c:1 1 -n:1 test_worker \
	-Q:2 chemaxon -c:2 8 -n:2 chemaxon_worker \
	-Q:3 epi -c:3 8 -n:3 epi_worker \
	-Q:4 sparc -c:4 1 -n:4 sparc_worker \
	-Q:5 measured -c:5 1 -n:5 measured_worker