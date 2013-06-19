from cgi import escape
from urllib import unquote
import MySQLdb
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    print "lon1 in radians", lon1
    print "lat1 in radians", lat1
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    print "\na ", a, "\n"
    c = 2 * asin(sqrt(a))
    print "\nc is ", c
    km = 6367 * c
    print "\nkm is ", km
    return km * 0.621371 # miles
    #return km # of kms 


# standard mod_python entry point
def index(req):
  returnPage = "-1"

  # get user info 
  map_id = req.form.getfirst('map_id','')
  user_id = req.form.getfirst('user_id','')

  # we can get a variable number of lat,lons
  # so we handle that here
  nextLatLon = 0
  exitFlag = 0
  latLons = []
  while exitFlag == 0:
    nextLatLon = nextLatLon + 1
    nextLatName = 'lat' + str(nextLatLon)
    nextLonName = 'lon' + str(nextLatLon)
    user_lat = req.form.getfirst(nextLatName,'')
    user_lon = req.form.getfirst(nextLonName,'')

    if user_lat == '':
      exitFlag = 1
    else:
      tmpDict = {'lat':str(user_lat), 'lon':str(user_lon)}
      latLons.append( tmpDict )

  if map_id != '' and user_id != '' and nextLatLon > 0:
    # connect to database
    db = MySQLdb.connect(host='localhost', db='kaboom', user='root', passwd='w00t')
    cursor = db.cursor()

    # get a list of players currently in the room/map
    cursor.execute("""SELECT user_id, user_lat, user_lon FROM user_map WHERE map_id = %s""", ( map_id, ))
    results = cursor.fetchall()
    players = []
    if results:
      for result in results:
        tmpDict = {'user_id':int(result[0]), 'user_lat':result[1], 'user_lon':result[2]}
        players.append(tmpDict)

    # here we need to spin through each bomb posted
    # and for each player in the room we need to create
    # an entry in the detonation_q table 
    # [map_id, sender_id, recipient_id, lat, lon]
    # note sender is user_id, recipient_id is player_id
    for latLon in latLons:
      for player in players:
        player_id = player['user_id']
        sql = "INSERT INTO detonation_q (map_id, sender_id, recipient_id, bomb_lat, bomb_lon) VALUES (%s, %s, %s, %s, %s)" % (map_id, user_id, player_id, latLon['lat'], latLon['lon'])
        cursor.execute( sql )

        # we also do collision detection and create an 
        # entry in the collided table if appropriate
        distanceInMiles = haversine(latLon['lat'], latLon['lon'], player['user_lat'], player['user_lon'])
        #if distanceInMiles < 0.02:
        if distanceInMiles < 0.0075:
          # we have a hit on player player_id on a bomb detonated by user user_id!
          sql = "INSERT INTO kills (map_id, sender_id, recipient_id, bomb_lat, bomb_lon) VALUES (%s, %s, %s, %s, %s)" % (map_id, user_id, player_id, latLon['lat'], latLon['lon'])
          cursor.execute( sql )
          sql = "INSERT INTO kills_history (map_id, sender_id, recipient_id, bomb_lat, bomb_lon) VALUES (%s, %s, %s, %s, %s)" % (map_id, user_id, player_id, latLon['lat'], latLon['lon'])
          cursor.execute( sql )

          f = open('/tmp/test.log', 'a')
          f.write( "\nPlayer:%s killed player:%s" % (user_id, player_id) )
          f.close()

    db.commit()
    db.close()
    returnPage = "0"

  return returnPage

