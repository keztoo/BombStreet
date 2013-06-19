from cgi import escape
from urllib import unquote
import MySQLdb

# standard mod_python entry point
def index(req):

  # TODO - stick these in a config file !
  javascriptSubdir = "../../scripts"
  styleSubdir = "../../style"
  imagesSubdir = "../../images"

  map_name = req.form.getfirst('mapname', '')
  player_id = req.form.getfirst('userid', '')
  default_lat = req.form.getfirst('lat', '')
  default_lon = req.form.getfirst('lon', '')
  map_id = 0

  page = "Error Invalid Map Name"

  # connect to database
  db = MySQLdb.connect(host='localhost', db='kaboom', user='root', passwd='w00t')
  cursor = db.cursor()

  cursor.execute("""SELECT id FROM map WHERE map_name = %s""", (map_name,))
  result = cursor.fetchone()
  if result:
    map_id = result[0]

  if map_id == 0:
    page = "Error - Map Not Found"
  else:
    # now make sure user/map combo is unique
    cursor.execute("""SELECT id FROM user_map WHERE map_id = %s AND user_id = %s""", (map_id,player_id))
    result = cursor.fetchone()

    if result:
      page = "Error - User already in map"
    else:
      # insert new user/map combo in database
      cursor.execute("""INSERT INTO user_map (map_id, user_id, user_lat, user_lon) VALUES (%s, %s, %s, %s)""", (map_id, player_id, 1.1, -1.1))
      db.commit()

      # now get map data from database
      cursor.execute("""SELECT map_name, r1slat, r1slon, r1elat, r1elon, r2slat, r2slon, r2elat, r2elon, r3slat, r3slon, r3elat, r3elon FROM map WHERE map_name = %s""", (map_name,))
      result = cursor.fetchone()
      if result:
        map_name = result[0]
        r1slat = result[1]
        r1slon = result[2]
        r1elat = result[3]
        r1elon = result[4]

        r2slat = result[5]
        r2slon = result[6]
        r2elat = result[7]
        r2elon = result[8]

        r3slat = result[9]
        r3slon = result[10]
        r3elat = result[11]
        r3elon = result[12]

        # here we need to handle the template
        templateFileName = "/home/ken/websites/BombStreet/load_map.tmpl"
        f = open(templateFileName, "r")
        page = f.read()
        f.close()

        page = page.replace("@MACRO_player_id", str(player_id))
        page = page.replace("@MACRO_map_id", str(map_id))
        page = page.replace("@MACRO_default_lat", str(default_lat))
        page = page.replace("@MACRO_default_lon", str(default_lon))
        page = page.replace("@MACRO_javascript_subdirectory", javascriptSubdir)
        page = page.replace("@MACRO_image_subdirectory", imagesSubdir)
        page = page.replace("@MACRO_style_subdirectory", styleSubdir)

        page = page.replace("@MACRO_r1slat", r1slat)
        page = page.replace("@MACRO_r1slon", r1slon)
        page = page.replace("@MACRO_r1elat", r1elat)
        page = page.replace("@MACRO_r1elon", r1elon)
 
        page = page.replace("@MACRO_r2slat", r2slat)
        page = page.replace("@MACRO_r2slon", r2slon)
        page = page.replace("@MACRO_r2elat", r2elat)
        page = page.replace("@MACRO_r2elon", r2elon)

        page = page.replace("@MACRO_r3slat", r3slat)
        page = page.replace("@MACRO_r3slon", r3slon)
        page = page.replace("@MACRO_r3elat", r3elat)
        page = page.replace("@MACRO_r3elon", r3elon)

  return page

