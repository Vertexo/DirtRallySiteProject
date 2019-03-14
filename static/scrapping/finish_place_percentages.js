function finish_place_percentages() {

		var cell_count = document.getElementsByClassName('percentages_events_finished').length;
		for (var i = 0; i < cell_count; i++) {

			var events_finished = document.getElementsByClassName('percentages_events_finished')[i].innerHTML;
			var first_places = document.getElementsByClassName('percentages_first_places')[i].innerHTML;
			var top_3 = document.getElementsByClassName('percentages_top_3')[i].innerHTML;
			var top_10 = document.getElementsByClassName('percentages_top_10')[i].innerHTML;
			var top_100 = document.getElementsByClassName('percentages_top_100')[i].innerHTML;

			var first_places_percentage = (parseInt(first_places) / parseInt(events_finished) * 100).toFixed(2);
			var top_3_percentage = (parseInt(top_3) / parseInt(events_finished) * 100).toFixed(2);
			var top_10_percentage = (parseInt(top_10) / parseInt(events_finished) * 100).toFixed(2);
			var top_100_percentage = (parseInt(top_100) / parseInt(events_finished) * 100).toFixed(2);

			if (events_finished != 0) {
				document.getElementsByClassName('percentages_first_places')[i].innerHTML = first_places + '<span style="color: red; font-size: 14px;"> (' + first_places_percentage + '%)</span>'
				document.getElementsByClassName('percentages_top_3')[i].innerHTML = top_3 + '<span style="color: red; font-size: 14px;"> (' + top_3_percentage + '%)</span>'
				document.getElementsByClassName('percentages_top_10')[i].innerHTML = top_10 + '<span style="color: red; font-size: 14px;"> (' + top_10_percentage + '%)</span>'
				document.getElementsByClassName('percentages_top_100')[i].innerHTML = top_100 + '<span style="color: red; font-size: 14px;"> (' + top_100_percentage + '%)</span>'
			}	
		}

	}


	finish_place_percentages();