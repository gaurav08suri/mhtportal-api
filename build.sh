#!/bin/bash

command_exists () {
    type "$1" &> /dev/null; 
}

if [ ! -d "$PWD/logs/" ];
then
    echo "creating logs directory";
    echo ""
    mkdir $PWD/logs;
    sleep 1;
fi

if [ ! -d "$PWD/database/postgresql/" ];
then
    echo "creating database directory";
    echo ""
    mkdir -p $PWD/database/postgresql;
    sleep 1;
fi

echo "------------------------------------------------------------------------";
echo "";
echo "Building Docker Containers. Sit tight, it'll be over in a minute or two";
echo "";
echo "------------------------------------------------------------------------";
if ! command_exists docker-compose;
then
echo "oh snap! You don't have docker installed";
exit 1;
fi

status=`docker-compose ps | grep -i "mhtportal" | wc -l`;
if [[ $status != 5 ]];
then
    docker-compose up -d;
    echo "Waiting for all containers to start properly. Be Patient, now!"
    sleep 15;
else
    echo "Containers are already up and running.";
    echo "If you want to force restart containers, you can do so using following";
    echo "command: 'docker-compose restart' "
    sleep 1;
fi

echo "------------------------------------------------------------------------";
echo "";
echo "Creating default superuser. I promise this the last one!";
echo "";
echo "------------------------------------------------------------------------";
sleep 10;
docker-compose run web bash -c 'echo "from django.contrib.auth.models import User; \
                                User.objects.filter(email=\"jon@snow.com\").delete(); \
                                User.objects.create_superuser(\"jon\", \"jon@snow.com\", \
                                \"youknownothing\")" | python manage.py shell;';

sleep 1;
echo "Alright, unless there are any errors, I'm pretty much done here."
echo "See you again!"
