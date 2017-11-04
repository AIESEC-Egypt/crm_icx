Install
=========

This is where you write how to get a new laptop to run this project.

Setup your Database
=========

1. Initially you need to put the committees in place.
2. Through the python shell navigate to crm_icx.core.cron
3. import request_committees()
4. Run it
5. You should now have the lcs and mcs ready in the database.
6. Run "python manage.py runcrons" to initiate the crons to update the applications and opportunities
