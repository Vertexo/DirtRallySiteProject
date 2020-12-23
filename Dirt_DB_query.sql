-- General SQL query call for event data
SELECT *
FROM scrapping_eventinfo
JOIN scrapping_leaderboard ON scrapping_leaderboard.event_info_id=scrapping_eventinfo.id
WHERE 
		scrapping_eventinfo.stage LIKE '%Waldaufstieg%'
	AND scrapping_leaderboard.name = 'nagler'
	AND scrapping_leaderboard.country_name = 'Latvia'
	AND scrapping_leaderboard.vehicle LIKE '%Volkswagen%'

ORDER BY scrapping_leaderboard.time_seconds ASC





-- Order column values by their frequency
SELECT vehicle, COUNT(vehicle) AS MOST_FREQUENT
FROM scrapping_leaderboard
JOIN scrapping_eventinfo ON scrapping_leaderboard.event_info_id=scrapping_eventinfo.id
GROUP BY vehicle
ORDER BY COUNT(vehicle) DESC