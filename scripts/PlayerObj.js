// *******************
// * a player object *
// *******************
function PlayerObj(map, mapId, playerId, playerName, playerType, playerLat, playerLon, playerIcon) 
{
	// attributes ... 
	this.playerId = playerId;
	this.playerMapId = mapId;
	this.playerName = playerName;
	this.playerType = playerType; // valid types = {'me', 'enemy', 'team'}
	this.playerLat = playerLat;
	this.playerLon = playerLon;
	this.playerIcon = playerIcon;

        // we create a marker
        this.myMarker = new google.maps.Marker({    
          position: new google.maps.LatLng(playerLat, playerLon), 
          map: map
        });  
        this.myMarker.setIcon(playerIcon);

        // we add a listener for on click events
        var me = this;
        google.maps.event.addListener(this.myMarker, "click", function () {
          var postStr = "map_id=" + me.playerMapId + "&user_id=" + me.playerId;
          kajaxPostServer('get_user_stats.py', postStr, function (resp) {
              alert(resp);
            });
        });

	// methods ... 
	PlayerObj.prototype.replaceAll = function (find, replace, str){
		return str.replace(new RegExp(find, 'g'), replace);
	}

	PlayerObj.prototype.setName = function (newName){
		this.playerName = newName;
		return(this.playerName);
	}

	PlayerObj.prototype.getName = function (){ return(this.playerName); }

	PlayerObj.prototype.setPosition = function (newLat, newLon){
		this.playerLat = newLat;
		this.playerLon = newLon;
                this.myMarker.setPosition(new google.maps.LatLng(newLat, newLon));
		return(0);
	}

	PlayerObj.prototype.toString = function (){ return(this.playerName); }
}

