#!/bin/sh
celery multi stop \
	chemaxon_worker \
	test_worker \
	epi_worker \
	sparc_worker \
	measured_worker