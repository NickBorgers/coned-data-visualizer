# ConEd Usage Visualizer
I don't like how ConEd represents electricity usage data, and want something that appeals to me visually.

I've used The Elastic Stack for this in the past and have containerized it before, so that seems easy.

Note: this project isn't very useful to anyone but me because of what I decided to do with `macvlan` networks. I did this to isolate this software on my LAN because my host has access to subnets of various sensitivity. This makes the docker-relevant networking much more complicated and confusing. If you wanted to use this I'd primarily recommend ripping all that out and going back to using Docker-provided DNS resolution between containers.

## Configuration
You must [follow the directions published for the underlying Python package for interacting with ConEd's website](https://github.com/bvlaicu/coned).

Then, you can populate a `./.credentials.env` file like:
```
LOGIN_EMAIL_ADDRESS=whoever@example.com
LOGIN_PASSWORD=password
LOGIN_TOTP_SECRET=JBSWY3DPEHPK3PXP
ACCOUNT_UUID=b6a7954a-f9a0-46bf-92a5-2ccc8e50a755
METER_NUMBER=123456890
```
This will feed data to the ConEd Collector container.

## Get this running
Dependencies:
1. Aforementioned setup for ConEd interaction
1. Docker Compose; I'm actually running this with Podman + their support for interoperability with Docker Compose
1. Make, if you want any semblance of security

Recommended way to start this up is to run:
```
make
```
That will generate unique password for Elasticsearch and Kibana.

Note: even in this configuration there will be a user `viewer` and password `password`; but it lacks privilege to do anything destructive.

You technically can just run `docker-compose up` but it will use the passwords that have been comitted into the public repo. Whether or not this really matters depends on the level of network exposure for the endpoints.

## Weird thing I did
I'm running this in an isolated VLAN, so the containers will try to interact with a specific network interface that probably doesn't exist on your host and try to claim IP addresses that probably don't exist on your network.

If you rip all of that out and/or adjust it for your environment, you should have the containers up and running.

In my environment I visit Kibana @ http://10.212.99.7:80 and login with the username `viewer` and password `password`. There is a Dashboard already created and ready to use which shows my electrical power consumption. You'll likely want to adjust the timeframe of the search for the data to be meaningful, especially as ConEd provides data with a fairly significant lag (~1.5 hours).