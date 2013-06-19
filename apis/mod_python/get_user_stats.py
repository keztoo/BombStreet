from cgi import escape
from urllib import unquote
import MySQLdb

# standard mod_python entry point
def index(req):
  returnPage = "There was a problem with the request"

  map_id = req.form.getfirst('map_id','')
  user_id = req.form.getfirst('user_id','')

  if map_id != '' and user_id != '':
  # connect to database
    db = MySQLdb.connect(host='localhost', db='kaboom', user='root', passwd='w00t')
    cursor = db.cursor()

    # get kills
    cursor.execute("""SELECT COUNT(*) FROM kills_history WHERE sender_id = %s AND map_id = %s""", (user_id,map_id))
    result = cursor.fetchone()
    kills = 0
    if result:
      kills = str(result[0])

    # get hits
    cursor.execute("""SELECT COUNT(*) FROM kills_history WHERE recipient_id = %s AND map_id = %s""", (user_id,map_id))
    result = cursor.fetchone()
    hits = 0
    if result:
      hits = str(result[0])

    # get last activity
    cursor.execute("""SELECT last_updated FROM user_map WHERE user_id = %s""", (user_id,))
    result = cursor.fetchone()
    last_update = ''
    if result:
      last_update = str(result[0])

    returnPage = "\nInformation For Player %s\nKills:%s\nHits:%s\nLast Activity:%s" % (user_id, kills, hits, last_update)

  """
  f = open('/tmp/test.log', 'a')
  f.write(returnPage)
  f.close()
  """

  return returnPage


