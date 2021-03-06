#! /usr/bin/env python
from random import SystemRandom
from subprocess import call


def install_reqs():
    call("pip install -r reqs/dev.txt", shell=True)


def update_virtualenv_hooks():
    call("sed 's/PROJECT_NAME/{{ project_name }}/' bin/temp_postactivate > bin/postactivate", shell=True)
    call("rm bin/temp_postactivate", shell=True)


def setup_database():
    SECRET_KEY = '{{ secret_key }}'
    print "Let's setup the local MySQL Database:"
    local_db_name = raw_input('Local Database Name: ')
    local_db_user = raw_input('Local Database User: ')
    local_db_pwd = raw_input('Local Database Password: ')

    call("sed 's/DATABASE_NAME/{}/g;s/DATABASE_USER/{}/g' {{ project_name }}/settings/temp_dev.py > {{ project_name }}/settings/dev.py".format(local_db_name, local_db_user), shell=True)
    call("sed 's/DATABASE_PASSWORD/{}/g;s/_SECRET_KEY/{}/g' {{ project_name }}/settings/local.py.example > {{ project_name }}/settings/local.py".format(local_db_pwd, SECRET_KEY), shell=True)
    call("rm {{ project_name }}/settings/temp_dev.py", shell=True)
    print "\n...Local DB variables setup\n"

    print "Let's setup the production MySQL Database:"
    prod_db_name = raw_input('Production Database Name: ')
    prod_db_user = raw_input('Production Database User: ')

    call("sed 's/DATABASE_NAME/{}/g;s/DATABASE_USER/{}/g' {{ project_name }}/settings/temp_prod.py > {{ project_name }}/settings/prod.py".format(prod_db_name, prod_db_user), shell=True)
    call("rm {{ project_name }}/settings/temp_prod.py", shell=True)
    print "\n...Production DB variables setup"
    print "NOTE: You will need to update your local.py file on production with the correct password.\n"


if __name__ == "__main__":
    print "\nInstalling Requirements"
    print "===========================\n"
    install_reqs()
    print "...done!"

    print "\nUpdating Virtualenv Hook"
    print "===========================\n"
    update_virtualenv_hooks()
    print "...done!"

    print "\nAdding Database Information"
    print "===========================\n"
    setup_database()
    print "...done!"
