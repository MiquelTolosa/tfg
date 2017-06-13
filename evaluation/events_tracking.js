function fromWhereFromLocation(){
	/* Gets from where is fired the event in case we need it */
	var loc = window.location.pathname;
	if(/^\/artist\//g.test(loc)){
		return "artist_profile";
	}if(/^\/main_app\/page\/news\//g.test(loc)){
		return "news_page";
	}if(/^\/main_app\/page\/shop\//g.test(loc)){
		return "mercha_page";
	}if(/^\/main_app\/page\/events\//g.test(loc)){
		return "events_page";
	}else{
		return loc;
	}
}

function reinforcementGAEvent(entity, action, from_where){
	if(!from_where){ //we have to detect from where has been interacted
		from_where = fromWhereFromLocation();
	}
	googleAnalyticsEvent(entity, action, from_where);
}

function googleAnalyticsEvent(category, action, label){
	/* Sends Google Analytics events */
	// console.log('Category: ' + category + ' - Action: ' + action + ' - Label: ' + label);
	ga('send', {
		hitType: 'event',
		eventCategory: category,
		eventAction: action,
		eventLabel: label
	});
}

function multipleEntityClickEvents($targ, from_where, events){
	/**
     * Used to set multiple click events on a target parent element
     *
     * @method multipleEntityClickEvents
     * @param $targ {DOM} the parent DOM element where we will search event classes comming from "events" paramenter
     * @param url {string} the url to call
     * @param events {JSON} dictionary where keys are css classes and each key has the action and the entity of the event,
     	for example: events = {
			"bkbn-play_song": ["play", "Song"],
			"bkbn-name_user": ["open", "Artist"],
		}
     */
	var rif_anti_class = "js-reinfEv_listening"; //we need a class to avoid multiple events listening to same events
	var aux_attrs = ["reinfEv-entity", "reinfEv-action", "reinfEv-from_where"]; //we set the attributes on each element
	//we iterate trought the events dictionary
	for (var class_key in events) {
		if (events.hasOwnProperty(class_key)) { 
			var event_inf = events[class_key]; // event_inf = [""]
			var action = event_inf[0];
			var entity = event_inf[1];
			var aux_attt_values = [entity, action, from_where];
			var $els = $targ.find("."+class_key).not("."+rif_anti_class);
			if($els.length){
				for (var i = aux_attrs.length - 1; i >= 0; i--) {
					$els.attr(aux_attrs[i], aux_attt_values[i])
				}
				$els.click(function(){ //reinforcement event on click
					var $t = $(this);
					var fun_params_array = [];
					for (var i = 0; i < aux_attrs.length; i++) { // we catch all the attributes setted before
						fun_params_array.push($t.attr(aux_attrs[i]));
					}
					reinforcementGAEvent.apply(null, fun_params_array); //call reinforcement event function
				});
				$els.addClass(rif_anti_class); //add anti-class to prevent multiple undesired click events on same element
			}
		}
	}	
}

function songMultipleEvConf(){
	/* Returns generic song configurations for reinforcement events */
	return {
		"bkbn-play_song": ["play", "Song"],
		"bkbn-download_song": ["download", "Song"],
		"bkbn-name_song": ["open", "Song"],
		"bkbn-name_user": ["open", "Artist"],
		"bkbn-hashtag_name": ["open", "Hashtag"],
		"bkbn-name_album": ["open", "Album"],
	};
}

function songMultipleEntityClickEvents($targ, from_where){
	multipleEntityClickEvents($targ, from_where, songMultipleEvConf());
}

/*
Important buttons on monkingme app
To track an html button you have to set the "js-tracked_button" class and "data-button-which" attribute.
*/
$(function(){
   trackImportantButton($("body"));
});

function trackImportantButtonHandler(){
	var which = $(this).attr("data-button-which");
	var location = $(this).attr("data-button-location");
	googleAnalyticsEvent("Button", which, location);
}

function trackImportantButton($targ){
	/* Important buttons to track onclick, like Upload button or search bar click */
	$targ.find(".js-tracked_button").offon('click', trackImportantButtonHandler);
}

