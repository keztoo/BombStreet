from cgi import escape
from urllib import unquote
import MySQLdb

# standard mod_python entry point
def index(req):
  returnPage = "Map Created Successfully"

  # get sw and ne coords for rect1
  r1slat = req.form.getfirst('r1slat','')
  r1slon = req.form.getfirst('r1slon','')
  r1elat = req.form.getfirst('r1elat','')
  r1elon = req.form.getfirst('r1elon','')

  # get sw and ne coords for rect2
  r2slat = req.form.getfirst('r2slat','')
  r2slon = req.form.getfirst('r2slon','')
  r2elat = req.form.getfirst('r2elat','')
  r2elon = req.form.getfirst('r2elon','')

  # get sw and ne coords for rect3
  r3slat = req.form.getfirst('r3slat','')
  r3slon = req.form.getfirst('r3slon','')
  r3elat = req.form.getfirst('r3elat','')
  r3elon = req.form.getfirst('r3elon','')

  map_name = req.form.getfirst('mapname','')

  if r1slat == '' or r1slon == '' or r1elat == '' or r1elon == '' or r2slat == '' or r2slon == '' or r2elat == '' or r2elon == '' or r3slat == '' or r3slon == '' or r3elat == '' or r3elon == '': 
    returnPage = "Error bad input!"
  else:
  # connect to database
    db = MySQLdb.connect(host='localhost', db='kaboom', user='root', passwd='w00t')
    cursor = db.cursor()
    cursor.execute("""INSERT INTO map (map_name, r1slat, r1slon, r1elat, r1elon, r2slat, r2slon, r2elat, r2elon, r3slat, r3slon, r3elat, r3elon) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (map_name, r1slat, r1slon, r1elat, r1elon, r2slat, r2slon, r2elat, r2elon, r3slat, r3slon, r3elat, r3elon))
    db.commit()
    db.close()

  baseTop = "<html><head></head><body>Hit your browser's back button<br/><br/>\n"
  baseBottom = "</body></html>"
  return baseTop + returnPage + " - " + map_name + baseBottom


