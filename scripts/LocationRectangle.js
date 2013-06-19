// *******************************
// * a Location Rectangle object *
// *******************************
function LocationRectangle(map, locationName, recStartLat, recStartLon, recEndLat, recEndLon, recColor, countDownInitializer, countDownDivName, weaponDivName)
{
	// ** attributes ... **
	this.locName = locationName;
	this.recStartLat = recStartLat;
	this.recStartLon = recStartLon;
	this.recEndLat = recEndLat;
	this.recEndLon = recEndLon;
	this.recColor = recColor;
	this.recCountDownInitializer = countDownInitializer;
	this.recCountDown = countDownInitializer;
	this.recUserWeaponCount = 0;
	this.countDownDivName = countDownDivName;
	this.weaponDivName = weaponDivName;

        this.gmRect = new google.maps.Rectangle({
          strokeColor: recColor,
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: recColor,
          fillOpacity: 0.35,
          map: map,
          bounds: new google.maps.LatLngBounds(
            new google.maps.LatLng(recStartLat, recStartLon), // sw
            new google.maps.LatLng(recEndLat, recEndLon)) // ne
        });
        map.fitBounds(this.gmRect.getBounds());

	// ** methods ... **
	LocationRectangle.prototype.replaceAll = function (find, replace, str){
		return str.replace(new RegExp(find, 'g'), replace);
	}

	LocationRectangle.prototype.setName = function (newName){
		this.locName = newName;
		return(this.locName);
	}
	LocationRectangle.prototype.getName = function (){ return(this.locName); }

	LocationRectangle.prototype.toString = function (){ return(this.locName); }
}

