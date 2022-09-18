import os
import asyncio
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from coned import Meter

print("Starting retrieval and report cycle------------")

# Read configuration from ENV_VARs
email = os.getenv("LOGIN_EMAIL_ADDRESS", "whoever@example.com")
password = os.getenv("LOGIN_PASSWORD", "password")
mfa_secret = os.getenv("LOGIN_TOTP_SECRET", "JBSWY3DPEHPK3PXP")
account_uuid = os.getenv("ACCOUNT_UUID", "b6a7954a-f9a0-46bf-92a5-2ccc8e50a755")
meter_number = os.getenv("METER_NUMBER", "123456890")
site = os.getenv("SITE", Meter.SITE_CONED)
dollar_cost_per_kwh = float(os.getenv("COST_PER_KWH", "0.3"))

# Elasticsearch configuration
elasticsearch_url = os.getenv("ELASTIC_URL", "https://elasticsearch:9200")
elasticsearch_username = os.getenv("ELASTIC_USERNAME", "elastic")
elasticsearch_password = os.getenv("ELASTIC_PASSWORD", "dontcare")

try:
    # Create connection with Elasticsearch
    es = Elasticsearch(
        elasticsearch_url,
        ca_certs="/app/certs/ca/ca.crt",
        basic_auth=(elasticsearch_username, elasticsearch_password)
    )
except:
    print("Failed to initialize Elasticsearch client, cannot proceed")
    print("Sit here and wait so we don't hammer Elasticsearch")
    for i in range(30):
        time.sleep(1)
    exit(1)

# Get timeout for all requests
timeout_seconds = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "90"))

# Create Meter object with all configuration
meter = Meter(
    email=email,
    password=password,
    mfa_type=Meter.MFA_TYPE_TOTP,
    mfa_secret=mfa_secret,
    account_uuid=account_uuid,
    meter_number=meter_number,
    site=site)

# Create async event loop for Chromium interaction with ConEd
event_loop = asyncio.get_event_loop()

print("About to start making request to ConEd------------")

# Get results by using Chromium to interact with ConEd
try:
    coned_readings = event_loop.run_until_complete(asyncio.wait_for(meter.all_reads(), timeout_seconds))
except:
    print("Failed to get data from ConEd!")
    if os.getenv("DOCKER_BUILD", "RUNTIME") != "BUILD":
        # Unless we're doing a docker build, sleep for 10 minutes so we don't hammer ConEd
        print("Sit here and wait so we don't hammer ConEd")
        for i in range(600):
            time.sleep(1)
        exit(1)
    # If we got here we're doing a Docker build and we only ran to download Chromium into the image. Just pretend everything went fine, we knew we would fail
    print("We're doing a Docker build, so exit and pretend everything worked!")
    exit(0)

print("Got resutls from ConEd------------------")
print("Latest was:")
print("Start time: " + coned_readings[-1]['start_time'])
print("End time: " + coned_readings[-1]['end_time'])
print("Value: " + str(coned_readings[-1]['value']))
print("Unit of measurement: " + coned_readings[-1]['unit_of_measurement'])

report_documents = []
for reading in coned_readings:
    report_document = {
        # Start time for reading
        "start_time": reading['start_time'],
        # End time for reading
        "end_time": reading['end_time'],
        # Value for reading
        "value": reading['value'],
        # Unit of measurement for reading
        "unit_of_measurement": reading['unit_of_measurement'],
        # Calculate cost based on $ per kWH configuration
        "cost_in_dollars": reading['value']*dollar_cost_per_kwh,
        # Timestamp for indexing
        "timestamp": datetime.now(),
    }

    # Index this report document
    resp = es.index(index="coned-usage-readings", id=reading['end_time'], document=report_document)
    print("Attempted to push document to Elasticsearch----------------")
    print(resp['result'])

print("Sleeping for 4 hours before I die and get restarted--------------")
# Sleep for 4 hours to delay next run
# 14400 = 4 * 60 * 60
# This loop means you can easily Ctrl+C the script while it sleeps
for i in range(14400):
   time.sleep(1)
