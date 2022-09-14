from .db_access import *

def best_players_scoring_db(id_quiz):
	query_string = "SELECT * FROM TER_SCORE WHERE id_player in (SELECT id_player from TER_GET_SCORE WHERE id_quiz = {} ) ORDER BY score DESC LIMIT 10 ;".format(id_quiz)
	cursor = init_connection(query_string)

	list_best_players = []
	position = 1
	for player in cursor:
		list_best_players.append({'position' : position, 'nickname' : player['nickname'], 'score': player['score']})
		position += 1

	#print("LIST BEST PLAYER :",list_best_players)
	return list_best_players


def insert_player_score_db(list_pseudos, id_quiz):
	list_best_players = best_players_scoring_db(id_quiz)
	list_pseudos = list_pseudos[:10]

	if len(list_best_players) < 10:
		for player in list_pseudos:
			try:
				insert_player_in_get_score_db(player, id_quiz)
			except:
				return False
		return True

	list_best_players = list_best_players[-3:]
	list_pseudos = sorted(list_pseudos, key = lambda column : column[1], reverse=True)

	ok_flag = True

	for player in list_pseudos:
		if(player[1] >= list_best_players[0]['score']):
			ok_flag = insert_player_in_get_score_db(player, id_quiz)
		elif (player[1] >= list_best_players[1]['score']):
			ok_flag = insert_player_in_get_score_db(player, id_quiz)
		elif (player[1] >= list_best_players[2]['score']):
			ok_flag =insert_player_in_get_score_db(player, id_quiz)
		if(not ok_flag):
			break

		list_best_players = best_players_scoring_db(id_quiz)[-3:]

	list_best_players = best_players_scoring_db(id_quiz)
	return ok_flag

def insert_player_in_get_score_db(player, id_quiz):
	try:
		query_string = "INSERT INTO TER_SCORE (nickname, score) VALUES ('{}', {})".format(player[0], player[1])
		insert_into_db(query_string)

		query_string = "SELECT * FROM TER_SCORE ORDER BY id_player DESC LIMIT 1"
		cursor = init_connection(query_string)

		for player_db in cursor:
			query_string = "INSERT INTO TER_GET_SCORE (id_quiz, id_player) VALUES ({}, {})".format(id_quiz, player_db['id_player'])
			insert_into_db(query_string)
	except:
		return False

	return True