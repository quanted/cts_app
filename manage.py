import os
import sys
import logging

if __name__ == "__main__":

    has_file = os.path.isfile("settings_local.py")

    logging.info(has_file)

    if has_file:
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_local")
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_local'
    elif os.path.abspath(__file__) == os.path.join('/', 'var', 'www', 'ubertool', 'ubertool_cts', 'manage.py'):
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_apache")
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_apache'
    else:
        print "gets here"
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
