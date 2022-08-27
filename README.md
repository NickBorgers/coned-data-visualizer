# ConEd Usage Visualizer
I don't like how ConEd represents electricity usage data, and want something that appeals to me visually.

I've used The Elastic Stack for this in the past and have containerized it before, so that seems easy.

## Configuration
You must [follow the directions published for the underlying Python package for interacting with ConEd's website]().

Then, you can populate a `./.credentials.env` file like:
```
LOGIN_EMAIL_ADDRESS=whoever@example.com
LOGIN_PASSWORD=password
LOGIN_TOTP_SECRET=JBSWY3DPEHPK3PXP
ACCOUNT_UUID=b6a7954a-f9a0-46bf-92a5-2ccc8e50a755
METER_NUMBER=123456890
```
This will feed data to the ConEd Collector container.