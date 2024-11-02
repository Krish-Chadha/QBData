import pandas as pd
import json
inner_json = None

def calculate_passer_rating(CMP, ATT, YDS, TD, INT):
    # Step 1: Calculate each component
    a = ((CMP / ATT) - 0.3) * 5
    b = ((YDS / ATT) - 3) * 0.25
    c = (TD / ATT) * 20
    d = 2.375 - ((INT / ATT) * 25)
    
    # Step 2: Apply the conditions
    a = min(max(a, 0), 2.375)
    b = min(max(b, 0), 2.375)
    c = min(max(c, 0), 2.375)
    d = min(max(d, 0), 2.375)
    
    # Step 3: Calculate the passer rating
    passer_rating = ((a + b + c + d) / 6) * 100
    return passer_rating

single_season = {
	"total_team_yds": 0,
	"total_team_points": 0,
	"total_team_tds": 0,
	"total_yards": 0,
	"total_tds": 0,
	"passing_yards": 0,
	"passing_attempts": 0,
	"passing_completions": 0,
	"passing_tds": 0,
	"interceptions": 0,
	"rushing_yards": 0,
	"rushing attempts": 0,
	"fumbles": 0,
	"times_sacked": 0,
	"total_snaps" : 0,
	"percent_of_snaps": 0,
	"games_played": 0,
	"snap_share_over_70": 0,
	"passer_rating": 0,
	"kcomp": 0
}



qb_stats = {
	"game_ids_all": [
		
	],
	"game_ids_70": [
		
	],
	"2022": single_season,
	"2021": single_season,
	"2019": single_season,
	"2018": single_season,
	"2017": single_season,
	"2016": single_season,
	"2015": single_season,
	"2014": single_season,
	"2013": single_season,
	"2012": single_season,
	"2012-2022": single_season

    
}

qbs = {}
for i in range(2012, 2022, 1):  
	data = pd.read_csv("QB_stats_"+i+"_.csv")
	for index, game in data.iterrows():
		player = game['player']
		season = game['season']
		if player not in qbs:
			qbs[player] = qb_stats
		current_season = qbs[player][season]
		qb = qbs[player]
	
		qbs[player]["game_ids"].append(game['game'])

		current_season = qbs[player]["game_ids"][i]
		
		current_season["passing_yards"] += game["pass_yds"]
		current_season["passing_attempts"] += game["pass_att"]
		current_season["passing_completions"] += game["pass_cmp"]
		current_season["passing_tds"] += game["pass_tds"]
		current_season["interceptions"] += game["pass_int"]
		
		current_season["rushing_yards"] += game["rush_yds"]
		current_season["fumbles"] += game["fumbles"]
		current_season["rushing attempts"] += game["rush_att"]
		
		current_season["times_sacked"] += game["times_sacked"]
		
		current_season["total_snaps"] += game["snap_count_offense"]
		current_season["percent_of_snaps"] += game["snap_count_offense_pct"]
		current_season["games_played"] += 1  # Assuming each game represents one game played
		current_season["snap_share_over_70"] += 1 if game["snap_count_offense_pct"] > .70 else 0
		
		current_season["total_tds"] += game["pass_tds"] + game["rush_tds"]
		current_season["total_yards"] += game["pass_yds"] + game["rush_yds"]
		
		current_season["passer_rating"] = calculate_passer_rating(current_season["passing_completions"], current_season["passing_attempts"], current_season["passing_yards"], current_season["passing_tds"], current_season["interceptions"])
		
		
