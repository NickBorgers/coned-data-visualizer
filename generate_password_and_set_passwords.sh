#!/bin/bash

generate_password() {
    echo $(head -2 /dev/urandom | tr -dc A-Za-z0-9 | head -c 13 ; echo "")
}

ELASTIC_PASSWORD=$(generate_password)
KIBANA_PASSWORD=$(generate_password)

sed -i "s/ELASTIC_PASSWORD=.*/ELASTIC_PASSWORD=$ELASTIC_PASSWORD/" .env
sed -i "s/KIBANA_PASSWORD=.*/KIBANA_PASSWORD=$KIBANA_PASSWORD/" .env