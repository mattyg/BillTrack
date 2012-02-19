from sunlightapi import sunlight, SunlightApiError
import RTC
import sqlite3


RTC.apikey = 'b281fd9d3a124f53970f623de12b0596'
sunlight.apikey = RTC.apikey

class positions:
	db = None
	def __init__(self):
		self.con = sqlite3.connect('kxltrackdata.db')
		self.db = self.con.cursor()
		self.db.execute('''CREATE TABLE IF NOT EXISTS \"bills\" (id INTEGER PRIMARY KEY UNIQUE, text TEXT, acted_at TEXT)''')
		self.db.execute('''CREATE TABLE IF NOT EXISTS \"positions\" (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, crp_id VARCHAR(10), cosponsor INTEGER NOT NULL DEFAULT 0, position INTEGER NOT NULL DEFAULT 1)''')		
		self.con.commit()

	def update(self):
		'''Get most recent data & add/update db'''
		# bill bill
		bill = RTC.Bill.get_bill(bill_id='hr3811-112')
		self.db.execute("REPLACE INTO bills (id, text, acted_at) VALUES (\"hr3811-112\", \"%s\", \"%s\")" %(bill['last_action']['text'],bill['last_action']['acted_at']))
		self.db.execute("UPDATE positions SET cosponsor=1, position=1 WHERE bioguide_id=\"%s\"" %(bill['sponsor_id']))
		for crp_id in bill['cosponsor_ids']:
			self.db.execute("UPDATE positions SET cosponsor=1, position=1 WHERE bioguide_id=\"%s\"" %(crp_id))
			print crp_id

		# bill bill
		bill = RTC.Bill.get_bill(bill_id='s2041-112')
		self.db.execute("REPLACE INTO bills (id, text, acted_at) VALUES (\"s2041-112\", \"%s\", \"%s\")" %(bill['last_action']['text'],bill['last_action']['acted_at']))
		self.db.execute("UPDATE positions SET cosponsor=1, position=1 WHERE bioguide_id=\"%s\"" %(bill['sponsor_id']))
		for crp_id in bill['cosponsor_ids']:
			self.db.execute("UPDATE positions SET cosponsor=1 , position=1 WHERE bioguide_id=\"%s\"" %(crp_id))

		self.con.commit()

	def initlegislators(self):
		self.db.execute("DELETE FROM positions")
		people = sunlight.legislators.getList(in_office=1)
		for each in people:				
			self.db.execute("INSERT INTO positions (id, bioguide_id, title, cosponsor, position) VALUES (\"%s\", \"%s\", \"%s\", 0, 2)" %(each.crp_id,each.bioguide_id,each.title))
		self.update()
		
		self.con.commit()

if __name__ == "__main__":
	positions().initlegislators()
