from ..data_access.auth import *
from ..data_access.question import *
from ..data_access.quiz import *
from ..data_access.tag import *
from ..data_access.score import *
from ..data_access.type_question import *
import json
import sys
from flask import Blueprint, request, redirect, jsonify

bpapi = Blueprint('api', __name__, url_prefix='/api')


@bpapi.route("/")
def home():
	return "Accueil ! "

@bpapi.route("/get_tags")
def get_tags():
	tags = get_tags_db()
	return jsonify(tags)

@bpapi.route("/get_types_question")
def get_type_question():
	types_question = get_types_question_db()
	return jsonify(types_question)

@bpapi.route("/get_questions")
def get_questions():
	return jsonify(get_questions_db())

@bpapi.route("/get_tag/<id>")
def get_tag_by_id(id):
	return jsonify(get_tag_by_id_db(id))


@bpapi.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = request.get_json()
		user_login = user['login']
		user_pass = user['pwd']
		#print(dir(data_access), file=sys.stderr)
		hasAccount = has_account_db(user_login, user_pass)
		if hasAccount != -1:
			return jsonify(hasAccount)
		return redirect('/')
	else:
		return '<form action="" method="post">login <input type="text" name="login" /><br>Password <input type="text" name="pwd" /><br><input type="submit" value="Envoyer" /></form>'

@bpapi.route('/user/update', methods=['GET', 'POST'])
def userUpdate():
	if request.method == 'POST':
		user = request.get_json()
		user_id = int(user['id'])
		user_name = user['name']
		user_login = user['login']
		user_password = user['pwd']
		updated = update_user_db(user_id, user_name, user_login, user_password)
		if not updated:
			return "error"
		return jsonify(updated)
	else:
		return '<form action="" method="post">id<input type="text" name="id" /> <br> name <input type="text" name="name" /><br> login <input type="text" name="login" /><br>Password <input type="text" name="pwd" /><br><input type="submit" value="Envoyer" /></form>'


@bpapi.route("/create_user", methods=['GET', 'POST'])
def create_user():
	if request.method == 'POST':
		user = request.get_json()
		user_name = user['name']
		user_login = user['login']
		user_pass = user['pwd']
		isCreate = create_user_db(user_name, user_login, user_pass)
		if isCreate:
			hasAccount = has_account_db(user_login, user_pass)
			return jsonify(hasAccount)
		return "Not add"
	else:
		return '<form action="" method="post">Name <input type="text" name="name" /><br>login <input type="text" name="login" /><br>Password <input type="text" name="pwd" /><br><input type="submit" value="Envoyer" /></form>'

@bpapi.route("/user/delete/<id>")
def userDelete(id):
	return delete_user_db(id)

@bpapi.route('/record_score', methods=['POST'])
def record_score():
	response = request.get_json()
	list_pseudos = response['best_players']
	id_quiz = response['id_quiz']

	success = insert_player_score_db(list_pseudos,id_quiz)
	if success:
		return "success"
	return -1

@bpapi.route('/best_player/<id_quiz>')
def best_player(id_quiz):
	return jsonify(best_players_scoring_db(id_quiz))

@bpapi.route("/get_user_quiz/<id>") #todo transformer en post
def get_user_quiz(id):
	return jsonify(get_user_quiz_db(id))

@bpapi.route("/get_quiz/<id_quiz>")
def get_quiz(id_quiz) : 
	return jsonify(get_quiz_db(id_quiz))

@bpapi.route("/insert_quiz", methods=["POST"])
def insert_quiz():
    quizz = request.get_json()
    insert_quiz_in_db(quizz)
    return "sucess"



##These routes are pure tests for the websockets
@bpapi.route("/socket_test_create_game")
def socket_test_creation():
	return '<h1>Launching the game<h1>\
		<button onclick=launch_game()>Launch</button>\
		<button onclick=next_question()>Next q</button>\
	<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>\
	<script type="text/javascript" charset="utf-8">\
		let socket = io();\
		let pin_g = "";\
		socket.on("connect", function() {\
			socket.emit("create_game",1);\
		});\
		socket.on("game_created", (arg) => {\
			console.log("The game was created with the pin :", arg);\
			pin_g = arg;\
		});\
		function launch_game(){\
			socket.emit("launch_game",{pin:pin_g})\
		}\
		function next_question(){\
			socket.emit("next_question",{pin:pin_g})\
		}\
		socket.on("message" ,(args) =>{\
							console.log(args)\
						})\
	</script>'

@bpapi.route("/socket_test_join_game",methods=['GET','POST'])
def socket_test_join_game():
	if request.method == 'POST':
		game = request.get_json()
		pin = game['pin']
		pseudo =  game['pseudo']
		return '<h1>Joining the game<h1>\
					<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>\
					<script type="text/javascript" charset="utf-8">\
						var socket = io();\
						socket.on("connect", function() {\
							socket.emit("join_game",{ pin:"'+pin+'",pseudo:"'+pseudo+'"});\
						});\
						socket.on("message" ,(args) =>{\
							console.log(args)\
						})\
					</script>'
	else:
		return '<form action="" method="post">Join game <input type="text" name="pin" /><br>Pseudo <input type="text" name="pseudo" /><br><input type="submit" value="Envoyer" /></form>'


@bpapi.route("/generate_quiz/tag=<tagId>&nb=<nb>")
def generate_quiz_tag(tagId, nb):
	if(nb == "0"):
		nb = 10
	if(tagId == "0"):
		nb = str(abs(int(nb)))
		return jsonify(generate_quiz_nb_db(nb))
	return jsonify(generate_quiz_from_tag_db(tagId, nb))

@bpapi.route("/update_quiz", methods=["POST"])
def updateQuiz():
    quiz = request.get_json()
    return jsonify(update_quiz_in_db(quiz))

@bpapi.route("/insert_quiz_generate", methods=["POST"])
def insert_quiz_generate():
    quiz = request.get_json()
    insert_quiz_generate_in_db(quiz)
    return "sucess"

