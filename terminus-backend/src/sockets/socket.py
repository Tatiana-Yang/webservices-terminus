from random import randint
from socket import socket
from ..data_access.auth import *
from ..data_access.question import *
from ..data_access.quiz import *
from ..data_access.tag import *
from ..data_access.score import *

from .game import QuizGame

import json
import sys
import random
import string

from flask import Blueprint, request, redirect, jsonify
from flask_socketio import SocketIO, send,emit, join_room,leave_room, disconnect

from .. import socketio

s=10
rooms = {} # the list of all the ongoing games
#Contains the following :
#{pin (game_pin) : quizGame}
answer_count = 0
answer_false = 0

def pin_generator():
	global s
	return ''.join((random.choice(string.ascii_letters + string.digits) for x in range(s)))


# 1 - Function utils : 
# Test de ping
@socketio.on('pingServer')
def pingServer(data):
	print(data)

def get_correct_answers(question):
	answers_nums = []
	cpt = 0
	for answer in question  :
		if(answer['correct'] == 1):
			answers_nums.append(cpt)
		cpt+=1
	return answers_nums

# 1 - User picked a quiz to create
#TODO FRONT : GET THE PIN AND ASSOCIATE IT TO A DYNAMIC URL THAT WE CAN JOIN
@socketio.on('create_game')
def create_game(data):
	global rooms
	pin = pin_generator()
	id_quiz = data['id']
	join_room(pin)
	game = QuizGame(id_quiz)
	rooms[pin] = game 
	emit("set_pin",pin)

# 2 - Join with a pin
@socketio.on('join_game')
def on_join_game(data):
    global rooms
    userpseudo = data["pseudo"]
    if data['pin'] in rooms:
            if(rooms[data['pin']].get_question_num() == 0): #check the status of the game
                if(rooms[data['pin']].register_player(data['pseudo']) != -1):
                    join_room(data["pin"])
                    #emit('subscribed',userpseudo + ' joined the game')
                    emit("set_users_pseudo",list(rooms[data['pin']].get_all_pseudos()),to=data['pin']) #broadcast to all the room that pseudo has entered
                else :
                    emit('on_connect_failed',"-2")
            else:
                emit('on_connect_failed',"-3")
    else:
        emit('on_connect_failed',"-1")

# 3 - Launching the game 
@socketio.on('launch_game')
def on_launch(data):
	global rooms
	question = get_quiz_by_question_number_db(rooms[data['pin']].get_id_quiz(),rooms[data['pin']].get_question_num())
	colors = get_colors_from_db(rooms[data['pin']].get_id_quiz())
	id_quiz = rooms[data['pin']].get_id_quiz()
	if len(question) != 0:	#send the first question
		rooms[data['pin']].set_current_question(question)
		rooms[data['pin']].next_question_num()
		rooms[data['pin']].set_current_answers(get_correct_answers(question['answers']))
		emit("init_underground_trail",colors)
		question['eliminated'] = len(rooms[data['pin']].players) - rooms[data['pin']].players_alive
		emit("set_question",question,to=data['pin'])
	else:
		rooms[data['pin']].update_players_scores();
		insert_player_score_db(rooms[data['pin']].get_scores(), id_quiz)
		toSend = (1,rooms[data['pin']].get_scores_sorted(), best_players_scoring_db(id_quiz))
		emit("game_end", toSend,to=data['pin'])

#Sending questions to the audience
@socketio.on('next_question')
def get_next_question(data):
	global rooms
	global answer_count
	global answer_false

	note = 100
	if answer_count != 0:
		note = (100 * answer_false)/answer_count
	answer_false = 0
	answer_count = 0
	id_last_quest = get_id_question_by_quiz_number_question_db(rooms[data['pin']].get_id_quiz(),rooms[data['pin']].get_question_num()-1)
	update_difficulty_db(id_last_quest, note)

	question = get_quiz_by_question_number_db(rooms[data['pin']].get_id_quiz(),rooms[data['pin']].get_question_num())
	id_quiz = rooms[data['pin']].get_id_quiz()
	if len(question) != 0:	#send the first question
		rooms[data['pin']].set_current_question(question)
		rooms[data['pin']].next_question_num()
		rooms[data['pin']].set_current_answers(get_correct_answers(question['answers']))
		question['eliminated'] = len(rooms[data['pin']].players) - rooms[data['pin']].players_alive
		emit("set_question",question,to=data['pin'])
	else:
		rooms[data['pin']].update_players_scores()
		insert_player_score_db(rooms[data['pin']].get_scores(), id_quiz)
		toSend = (1,rooms[data['pin']].get_scores_sorted(), best_players_scoring_db(id_quiz))
		emit("game_end", toSend,to=data['pin'])

@socketio.on('send_answer')
def get_player_answer(data): # data[pin, pseudo, answer num]
	global answer_count
	global answer_false

	answer_size = len(rooms[data['pin']].get_current_answers())
	rooms[data['pin']].ans_recieved +=1
	if(data['answer_num'] == -1):
		answer_false += 1
		answer_count += 1
		emit("set_status",-1)
		rooms[data['pin']].register_eliminated(data['pseudo'])
		if(rooms[data['pin']].get_total_alive()):
			emit('all_answers_recieved',to=data['pin'])
		return
	if rooms[data['pin']].check_players_eliminated(data['pseudo']):
		answer_false += 1
		answer_count += 1

		emit("set_status",-1)
		rooms[data['pin']].register_eliminated(data['pseudo'])
		if(rooms[data['pin']].get_total_alive()):
			emit('all_answers_recieved',to=data['pin'])
		return
	if answer_size == 1:
		if not (rooms[data['pin']].get_current_answers()[0] == data['answer_num'][0]):
			answer_false += 1
			answer_count += 1

			emit("set_status",-1)
			rooms[data['pin']].register_eliminated(data['pseudo'])
			if(rooms[data['pin']].get_total_alive()):
				emit('all_answers_recieved',to=data['pin'])
			return
		else:
			answer_count += 1
			emit("set_status",1)
			rooms[data['pin']].add_player_in_queue(data['pseudo'])	
			if(rooms[data['pin']].get_total_alive()):
				emit('all_answers_recieved',to=data['pin'])
			return	
	else:
		if answer_size != len(data['answer_num']):
			answer_false += 1
			answer_count += 1

			emit("set_status",-1)
			rooms[data['pin']].register_eliminated(data['pseudo'])
			if(rooms[data['pin']].get_total_alive()):
				emit('all_answers_recieved',to=data['pin'])
			return
		else :
			current_ans = rooms[data['pin']].get_current_answers()
			for ans_num in data['answer_num']:
				if(ans_num not in current_ans):
					answer_false += 1
					answer_count += 1
					emit('set_status',-1)
					rooms[data['pin']].register_eliminated(data['pseudo'])
					if(rooms[data['pin']].get_total_alive()):
						emit('all_answers_recieved',to=data['pin'])
					return
			answer_count += 1
			emit('set_status',1)
			rooms[data['pin']].add_player_in_queue(data['pseudo'])	

	if(rooms[data['pin']].get_total_alive()):
		emit('all_answers_recieved',to=data['pin'])

@socketio.on('request_bonus')		
def request_bonus(data):
	print("A bonus has been requested")
	emit("bonus_request",{'pseudo':data['pseudo'],'bonus_type':data['bonus']},to=data['pin'])
	if(data['bonus'] == 0):
		print('TIME FOR A 50/50') #NO FIFTY FIFTY ON MULTI
		to_send = fifty_fifty_datas(data['pin'])
		emit("bonus_time",to_send)
	else:
		print('TIME FOR THE PUBLIC CALL !')
		emit("bonus_time",{"bonus":"public"})
		emit('public_call',to=data['pin'])



@socketio.on('send_answer_bonus')	
def get_player_bonus_ans(data):
	rooms[data['pin']].ans_recieved +=1
	question = rooms[data['pin']].get_current_question()
	win = False
	for ans in question['answers']:
		if(data['answer'] == ans['answer'] and ans['correct'] == 1):
			win = True
	if win:
		emit('set_status',1)
		rooms[data['pin']].add_player_in_queue(data['pseudo'])	
	else:
		emit('set_status',-1)
		rooms[data['pin']].register_eliminated(data['pseudo'])
	if(rooms[data['pin']].get_total_alive()):
		emit('all_answers_recieved',to=data['pin'])

def fifty_fifty_datas(pin):
	global rooms
	question = rooms[pin].get_current_question()
	ans = rooms[pin].get_current_answers()
	r1 = randint(0,len(question['answers'])-1)
	while(r1 == ans[0]):
		r1 = randint(0,len(question['answers'])-1)
	rooms[pin].set_current_answers([0])
	return {"bonus":"fifty","correct":question['answers'][ans[0]],"not":question['answers'][r1]} #TODO randomiser


@socketio.on('send_answer_bonus_call')
def get_answer_bonus_call(data):
	answer_size = len(rooms[data['pin']].get_current_answers())
	question = rooms[data['pin']].get_current_question()
	if(data['answer_num'] == -1):
		return
	if rooms[data['pin']].check_players_eliminated(data['pseudo']):
		if answer_size == 1:
			rooms[data['pin']].set_public_call_stats(question['answers'][data['answer_num'][0]])
		else:
			for ans_num in data['answer_num']:
				rooms[data['pin']].set_public_call_stats(question['answers'][ans_num])
	

@socketio.on('get_public_answers')
def get_public_answers(data):
	emit("public_ans",rooms[data['pin']].get_public_call_stats())