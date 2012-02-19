#!/usr/bin/env python
import settings
import web
from web import form
from sunlightapi import sunlight, SunlightApiError
from transparencydata import TransparencyData
import RTC
import os

sunlight.apikey = settings.API_KEY
transparency = TransparencyData(settings.API_KEY)
RTC.apikey = settings.API_KEY
templates = web.template.render(settings.TEMPLATES_PATH)

db = web.database(dbn='sqlite', db=settings.DATABASE_PATH)

urls = (
'/','index',
'/faq/','faq',
'/district/of/(.+)/(.+)/', 'district',
'/district/', 'zipdistrict',
'/legislator/(.+)/(.+)/', 'legislator',
'/lookup/', 'lookup'
)
app = web.application(urls, globals(),autoreload=False)


vzip = form.regexp(r"[0-9][0-9][0-9][0-9][0-9]", "must be a valid zip code")
zipcode_form = form.Form(
	form.Textbox("zipcode",description="Zip Code")
)

class faq:
	def GET(self):
		return templates.faq()

class index:
	def GET(self):
		form = zipcode_form()
		senatecount = db.query("SELECT count(id) as total FROM positions WHERE position=1 AND title=\"Sen\"")[0]['total']
		housecount = db.query("SELECT count(id) as total FROM positions WHERE position=1 AND title=\"Rep\"")[0]['total']
		return templates.index(form,senatecount,housecount)

class zipdistrict:
	def POST(self):
		form = zipcode_form()
		if not form.validates():
			return render.index(form)
		else:
			z = form['zipcode'].value
		totalantis = []
		totalpros = []
		positions = []
		totalbigs = []

		# get people
		people = sunlight.legislators.allForZip(str(z))
		for peop in people:
			# get position
			row = db.select("positions",where="id = \"%s\"" %(peop.crp_id))[0]
			positions.append(row.position)
			# calculate total anti money
			antimoney = transparency.contributions(cycle='2010|2011|2012', contributor_industry=settings.GROUPS_OPPOSE_STRING, recipient_ext_id=peop.crp_id)
			totalanti = 0.00
			for each in antimoney:
				totalanti += float(each['amount'])
			totalantis.append(int(totalanti))
			# calculate total pro money
			promoney = transparency.contributions(cycle='2010|2011|2012', contributor_industry=settings.GROUPS_SUPPORT_STRING, recipient_ext_id=peop.crp_id)
			totalpro = 0.00
			for each in promoney:
				totalpro += float(each['amount'])
			totalpros.append(int(totalpro))
			# calculate big oil gas money
			bigoilmoney = transparency.contributions(cycle='2010|2011|2012', contributor_industry='E1110', recipient_ext_id=peop.crp_id)
			totalbig = 0.00
			for each in bigoilmoney:
				totalbig += float(each['amount'])
			totalbigs.append(totalbig)
		print len(people),len(positions),len(totalantis),len(totalpros),len(totalbigs)
		return templates.district(people, positions, totalantis, totalpros, totalbigs)


class district:
	def GET(self,lat,elon):
		totalantis = []
		totalpros = []
		totalbigs = []
		positions = []

		people = sunlight.legislators.allForLatLong(lat,elon)
		for peop in people:
			# get position
			row = db.select("positions",where="id = \"%s\"" %(peop.crp_id))[0]
			positions.append(row.position)
			# calculate total anti money
			antimoney = transparency.contributions(cycle=settings.DONATION_YEARS_STRING, contributor_industry=settings.GROUPS_OPPOSE_STRING, recipient_ext_id=peop.crp_id)
			totalanti = 0.00
			for each in antimoney:
				totalanti += float(each['amount'])
			totalantis.append(int(totalanti))
			# calculate total pro money
			groups_support = settings.GROUPS_SUPPORT.join('|')
			promoney = transparency.contributions(cycle=settings.DONATION_YEARS_STRING, contributor_industry=GROUPS_SUPPORT_STRING, recipient_ext_id=peop.crp_id)
			totalpro = 0.00
			for each in promoney:
				totalpro += float(each['amount'])
			totalpros.append(int(totalpro))
			# calculate big oil gas money
			bigoilmoney = transparency.contributions(cycle=settings.DONATION_YEARS_STRING, contributor_industry='E1110', recipient_ext_id=peop.crp_id)
			totalbig = 0.00
			for each in bigoilmoney:
				totalbig += float(each['amount'])
			totalbigs.append(int(totalbig))
			

		return templates.district(people, positions, totalantis, totalpros, totalbigs)

class legislator:
	def GET(self,state,lastname):
		person = sunlight.legislators.get(state=state,lastname=lastname)
		# get position
		row = db.select("positions",where="id = \"%s\"" %(person.crp_id))[0]
		position = row.position
		# calculate total anti money
		antimoney = transparency.contributions(cycle=settings.DONATION_YEARS_STRING, contributor_industry=settings.GROUPS_OPPOSE_STRING, recipient_ext_id=person.crp_id)
		totalanti = 0.00
		for each in antimoney:
			totalanti += float(each['amount'])
		# calculate total pro money
		promoney = transparency.contributions(cycle=settings.DONATION_YEARS_STRING, contributor_industry=settings.GROUPS_SUPPORT_STRING, recipient_ext_id=person.crp_id)
		totalpro = 0.00
		for each in promoney:
			totalpro += float(each['amount'])
		#calculate total big oil & gas money
		bigoilmoney = transparency.contributions(cycle=settings.DONATION_YEARS_STRING, contributor_industry='E1110', recipient_ext_id=person.crp_id)
		totalbig = 0.00
		for each in bigoilmoney:
			totalbig += float(each['amount'])
															 
		return templates.legislator(person, position, int(totalanti), int(totalpro), int(totalbig))

if __name__ == "__main__":
	app.run()
