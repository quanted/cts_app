import os
import sys
import logging

if __name__ == "__main__":
	
	try:
		import local_path
	except ImportError:
		pass

	if os.path.abspath(__file__) == os.path.join('/', 'var', 'www', 'ubertool', 'ubertool_cts', 'manage.py'):
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_apache")
	elif os.path.abspath(__file__) == local_path.localPath():
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_local")
	else:
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_apache")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
