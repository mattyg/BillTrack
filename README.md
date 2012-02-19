BillTrack
===

Easily create a website for any bill in Federal Congress. The site will include:
- Legislator lookup with geolocation or zip code
- Legisilator's positions and donations from pro/anti bill groups


Example Sites:
===
- http://killkxl.com


Dependencies
===
- web.py
- sunlight api
- sunlight transparencydata api

Setup:
===
Edit the following variables in settings.py
- HOUSE_BILL and SENATE_BILL with the bill ids for the house and senate bill versions
- GROUPS_SUPPORT and GROUPS_OPPOSE with the CRP codes for supportive and opponant groups of the bills (group codes listed in CRP_categories.txt, use data from maplight.org)  
- API_KEY with your sunlight services api key (get one here: http://http://services.sunlightlabs.com/)

Edit the following templates:
- index.html with information about the bills you are trying to draw attention to
- faq.html with an FAQ about the bills
