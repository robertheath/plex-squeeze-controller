from server import Server
from player import Player
import time

NAME = "SqueezeControl"
SERVER_ADDRESS = "192.168.1.74"
ART         	= 'art-default.jpg'
ICON   		= 'icon-default.png'

####################################################################################################
def Start():
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

    ObjectContainer.title1 = NAME
    ObjectContainer.view_group="InfoList"
    ObjectContainer.art = R(ART)

####################################################################################################
@handler('/music/squeezecontrol', NAME)
def MainMenu():
    sc = Server(hostname=SERVER_ADDRESS, port=9090, username="", password="")
    sc.connect()

    oc = ObjectContainer()
    for player in sc.get_players():
	    player_id = str(player.get_ref())
	    current_time = str(time.time())

	    oc.add(DirectoryObject(key = Callback(ProcessRequest, title = player_id, params = {'order': 'hotness'}),
 				   title = player.get_name(), 
				   tagline=player.get_track_artist(), 
				   summary=player.get_track_current_title(), 
				   duration=player.get_track_duration(), 
				   thumb = Resource.ContentsOfURLWithFallback("http://"+SERVER_ADDRESS+":9000/music/current/cover.jpg?player="+player_id+"&time="+current_time)
				   )
		   )
    
    return oc

####################################################################################################
@route('/music/squeezecontrol/{title}', params = dict, offset = int, allow_sync = True)
def ProcessRequest(title, params, offset = 0, id = -1, type = "default"):
	sc = Server(hostname=SERVER_ADDRESS, port=9090, username="", password="")
	sc.connect()
	
	player = sc.get_player(title);
	oc = ObjectContainer(title2 = player.get_name())
	
	for item in player.playlist_get_info():
		track_title = player.request("songinfo 1 1 track_id:"+str(item['id']))[8:]
		track_url = player.request("songinfo 2 1 track_id:"+str(item['id'])+" tags:u")[21:]

		oc.add(DirectoryObject(key = track_url,
				       title = track_title,
				       duration = int(item['duration'])
				   )
		       )

	return oc
