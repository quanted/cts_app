import os
import sys
import logging

if __name__ == "__main__":

	hasFile = False

	try:
		import local_path
		hasFile = True
	except ImportError:
		pass

	if os.path.abspath(__file__) == os.path.join('/', 'var', 'www', 'ubertool', 'ubertool_cts', 'manage.py'):
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_apache")
	elif hasFile and os.path.abspath(__file__) == local_path.localPath():
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_local")
	else:
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
