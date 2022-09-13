# USF class monitor
The scripts class\_mon.py and usf\_reg.py are for the USF class monitor. They are meant to be run from a non-headless machine such as your laptop to then kick off a selenium script which controls Firefox to *attempt* to register you for the class, it has a bug with trying to click the final register button.

## Setting up
Edit the class\_mon.py file to include your CRNs and the class year you're intending to register for. In the usf\_reg.py class put in your login details where the comments tell you to. 

## Why not use requests?
Because if you have ever tried to make it fool the Shibboleth CAS SSO system USF uses for their NetID you'll realize it's very complicated to get it to accept your client. I had tried since I was a freshman to get this to work and I had eventually relented and used Selenium. If you find a way to fix either the registration button click bug or re-implement this in requests, definitely submit a pull request as that would allow for a lot more efficiency.

## Related projects
There is a freemium app called [Coursicle](https://www.coursicle.com) which supports sending push notifications to your phone when a space opens up in a class (actually helped me secure a seat in Advanced Javascript) and also another app called [USF Class Nodeifier](https://github.com/luqmaan/USFClassNodeifier) which also scrapes the schedule search but texts the user using Twilio.
