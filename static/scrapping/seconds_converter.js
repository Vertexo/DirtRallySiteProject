function time_converter() {

		var time_cell_count = document.getElementsByClassName('time_to_convert').length;
		for (var i = 0; i < time_cell_count; i++) {
			var time_seconds = document.getElementsByClassName('time_to_convert')[i].innerHTML;

			if (time_seconds != '') {
				var hours = 0
				var minutes = 0
				
				if (time_seconds < 3600) {
					minutes = parseInt(time_seconds / 60)
	        		var seconds = time_seconds % 60
				}

				else if (time_seconds < 60) {
	        		seconds = time_seconds[i]
				}

				else {
			        hours = parseInt(time_seconds / 3600)
			        var remainder = time_seconds % 3600
			        if (remainder < 60) {
			            seconds = remainder
			        }
			        else {
			            minutes = parseInt(remainder / 60)
			            seconds = remainder % 60
			        }
			    }

			    var time_format = hours.toString() + 'h ' + minutes.toString() + 'm ' + seconds.toFixed(3) + 's'
				document.getElementsByClassName('time_to_convert')[i].innerHTML = time_format

			}
		}

	}

	time_converter();