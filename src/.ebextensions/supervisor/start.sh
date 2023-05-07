#!/bin/bash

set -e

echo "Supervisor - starting setup"
. /opt/elasticbeanstalk/deployment/env

if [ ! -f /usr/bin/supervisord ]; then
    echo "installing supervisor"
    easy_install supervisor
else
    echo "supervisor already installed"
fi


if [ ! -d /etc/supervisor ]; then
    mkdir /etc/supervisor
    echo "create supervisor directory"
fi

if [ ! -d /etc/supervisor/conf.d ]; then
    mkdir /etc/supervisor/conf.d
    echo "create supervisor configs directory"
fi

. /opt/elasticbeanstalk/deployment/env && cat .ebextensions/supervisor/supervisord.conf > /etc/supervisor/supervisord.conf
. /opt/elasticbeanstalk/deployment/env && cat .ebextensions/supervisor/supervisord.conf > /etc/supervisord.conf
. /opt/elasticbeanstalk/deployment/env && cat .ebextensions/supervisor/ai_supervisor.conf > /etc/supervisor/conf.d/ai_supervisor.conf

if ps aux | grep "[/]usr/bin/supervisord"; then
    echo "supervisor is running"
else
    echo "starting supervisor"
    /usr/bin/supervisord
fi

/usr/bin/supervisorctl reread
/usr/bin/supervisorctl update

echo "Supervisor Running!"