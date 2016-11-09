import os
import sys
import logging

if __name__ == "__main__":

    if os.path.abspath(__file__) == os.path.join('/', 'var', 'www', 'ubertool', 'ubertool_cts', 'manage.py'):
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_apache")
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_apache'
    else:
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
