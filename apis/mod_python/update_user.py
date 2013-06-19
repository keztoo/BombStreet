from cgi import escape
from urllib import unquote
import MySQLdb

# standard mod_python entry point
def index(req):
  returnPage = "List of player triplets (id,lat,lon)"

  # get user info 
  map_id = req.form.getfirst('map_id','')
  this_user_id = req.form.getfirst('user_id','')
  user_lat = req.form.getfirst('user_lat','')
  user_lon = req.form.getfirst('user_lon','')

  if map_id == '' or this_user_id == '' or user_lat == '' or user_lon == '':
    returnPage = "Error bad input!"
  else:
    # connect to database
    db = MySQLdb.connect(host='localhost', db='kaboom', user='root', passwd='w00t')
    cursor = db.cursor()

    cursor.execute("""UPDATE user_map set user_lat = %s, user_lon = %s, last_updated = NOW() WHERE map_id = %s AND user_id = %s""", (user_lat, user_lon, map_id, this_user_id))
    db.commit()

    # now we need a list of players and current cooords
    cursor.execute("""SELECT user_id, user_lat, user_lon FROM user_map WHERE map_id = %s AND user_id != %s""", (map_id, this_user_id))
    results = cursor.fetchall()
    returnPage = "var otherPlayers=["
    if results:
      for result in results:
        user_id = str(result[0])
        user_lat = result[1]
        user_lon = result[2]
        returnPage = returnPage + user_id + "," + user_lat + "," + user_lon + ","

      returnPage = returnPage[:-1]

    returnPage = returnPage + "];"

    # here we pick up any new explosions for this user
    cursor.execute("""SELECT bomb_lat, bomb_lon, id FROM detonation_q WHERE map_id = %s AND recipient_id = %s""", (map_id, this_user_id))
    results = cursor.fetchall()
    returnPage = returnPage + "\nvar PL=" + this_user_id + ";var newExplosions=["
    idsToDelete = []
    if results:
      for result in results:
        bomb_lat = result[0]
        bomb_lon = result[1]
        rec_id = result[2]
        idsToDelete.append(rec_id)
        returnPage = returnPage + bomb_lat + "," + bomb_lon + ","

      returnPage = returnPage[:-1]

    returnPage = returnPage + "];"

    # and finally, here we delete any explosions we are sending 
    # so that we only send an explosion once to each recipient
    if len(idsToDelete) > 0:
      idList = "("
      for id in idsToDelete:
        idList = idList + str(id) + ","
      idList = idList[:-1]
      idList = idList + ")"
      sql = "DELETE FROM detonation_q WHERE id IN " + idList
      cursor.execute(sql)
      db.commit()

    # TODO combine these two duplicate blocks (above and below here)!

    # here we pick up any new kills or hits for this user
    cursor.execute("""SELECT id, sender_id, recipient_id FROM kills WHERE map_id = %s AND sender_id = %s OR recipient_id = %s""", (map_id, this_user_id, this_user_id))
    results = cursor.fetchall()
    returnPage = returnPage + "\nvar newHits=["
    idsToDelete = []
    if results:
      for result in results:
        record_id = result[0]
        snd_id = str(result[1])
        rcv_id = str(result[2])
        idsToDelete.append(record_id)
        if snd_id == this_user_id:
          returnPage = returnPage + "'k'" + ',' + rcv_id + ','
        else:
          returnPage = returnPage + "'h'" + ',' + snd_id + ','

      returnPage = returnPage[:-1]

    returnPage = returnPage + "];"

    # and finally, here we delete any kills we are sending 
    # so that we only send a kill notification once to each recipient
    #if len(idsToDelete) > 0:
    if len(idsToDelete) > 0:
      idList = "("
      for id in idsToDelete:
        idList = idList + str(id) + ","
      idList = idList[:-1]
      idList = idList + ")"
      sql = "DELETE FROM kills WHERE id IN " + idList
      cursor.execute(sql)
      db.commit()

    # one additional thing we can do is time out users from this map
    # someTimeStamp = '01:00:00' or hour, or someTimeStamp = '00:05:00' 5 minutes
    # select id from user_map where timediff(now(), last_updated) > '24:05:00';
    # will give a list of user ids to remove from the map (you will need to 
    # add these to a remove q for each active user)


  """
  if str(this_user_id) == '1':
    f = open('/tmp/test.log', 'a')
    f.write("\n" + returnPage)
    f.close()
  """

  return returnPage

