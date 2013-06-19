// *****************
// * a bomb object *
// *****************
function BombObj(map, bombLat, bombLon) 
{
	// ** attributes ... **
	this.map = map;
	this.bombLat = bombLat;
	this.bombLon = bombLon;
        this.bombState = 0; // 0 = inactive, 1 = armed
        this.bombInactiveIcon = "../../images/bomb_inactive.png";
        this.bombArmedIcon = "../../images/bomb_armed.png";
        this.bombIcons = [this.bombInactiveIcon, this.bombArmedIcon];

        // we create a marker
        this.bombMarker = new google.maps.Marker({    
          position: new google.maps.LatLng(bombLat, bombLon), 
          map: map
        });  
        this.bombMarker.setIcon(this.bombInactiveIcon);

        var me = this;

        // we add a listener for on click events
        google.maps.event.addListener(this.bombMarker, "click", function () {
            me.bombState = (me.bombState + 1) % 2;
            me.bombMarker.setIcon(me.bombIcons[me.bombState]);
        });

	// ** methods ... **
	BombObj.prototype.replaceAll = function (find, replace, str){
		return str.replace(new RegExp(find, 'g'), replace);
	}

	BombObj.prototype.setState = function (newState){
		this.bombState = newState;
		return(this.bombState);
	}

	BombObj.prototype.getState = function (){ return(this.bombState); }

	BombObj.prototype.toString = function (){ return(this.bombState); }
}

