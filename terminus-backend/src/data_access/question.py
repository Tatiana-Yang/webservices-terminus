from .db_access import *
from .tag import get_tag_by_id_db
from statistics import mean

def get_questions_db():
	cursor = init_connection("SELECT * FROM TER_QUESTION WHERE disable=0")

	list_questions = []

	for question in cursor:
		list_questions.append({"id_question":question["id_question"],
								"question" : question["question"],
								"name_tag" : question["id_tag"],
								"difficulty" : question["difficulty"]
								})

	for question in list_questions:
		question['name_tag'] = get_tag_by_id_db(question['name_tag'])[0]

	return list_questions


def get_id_type_question(type_question):
    return type_question['id_type_question']

def insert_question_in_ter_question_ter_has_question(id_quiz,question,id_tag,id_type_choisi):
    query_string = 'INSERT INTO TER_QUESTION (question,id_tag,difficulty, disable, id_type_question) VALUES ("{}",{},NULL,0, {});'.format(question,id_tag,id_type_choisi)
    insert_into_db(query_string)
    query_string = "SELECT MAX(id_question) as NUM FROM TER_QUESTION;"
    cursor = init_connection(query_string)

    success = True
    id_question = -1
    for element in cursor:
        try:
            id_question = int(element["NUM"])
        except:
            success = False
            break
    if(success):
        query_string = 'INSERT INTO TER_HAS_QUESTION(id_quiz,id_question) VALUES ({},{});'.format(id_quiz,id_question)
        insert_into_db(query_string)
        print("question insert passed")
        return id_question
    else:
        print("failed")
        return -1


def insert_question_in_ter_has_question(id_quiz,id_question):
	query_string = 'INSERT INTO TER_HAS_QUESTION(id_quiz,id_question) VALUES ({},{});'.format(id_quiz,id_question)
	try:
		insert_into_db(query_string)
		print("question insert passed")
		return id_question
	except Exception as exc:
		print("failed not insert in TER_HAS_QUESTION")
		print(exc)
		return -1

def insert_answer_in_ter_answer_ter_has_answer(id_quiz,id_question,answer,correctness):
    query_string = 'INSERT INTO TER_ANSWER (answer) VALUES ("{}");'.format(answer)
    insert_into_db(query_string)
    query_string = "SELECT MAX(id_answer) as NUM FROM TER_ANSWER;"
    cursor = init_connection(query_string)

    success = True
    id_answer = -1
    for element in cursor:
        try:
            id_answer = int(element["NUM"])
        except:
            success = False
            break
    if(success):
        query_string = 'INSERT INTO TER_HAS_ANSWER(id_question,id_answer,correct) VALUES ({},{},{});'.format(id_question,id_answer,correctness)
        insert_into_db(query_string)
        print("answer insert passed")
    else:
        print("failed")

def insert_answer_in_ter_answer_ter_has_answer_with_id(id_quiz,id_question,answer,correctness):
    print(answer)
    query_string = 'INSERT INTO TER_ANSWER (answer) VALUES ("{}");'.format(answer)
    insert_into_db(query_string)
    query_string = "SELECT MAX(id_answer) as NUM FROM TER_ANSWER;"
    cursor = init_connection(query_string)

    success = True
    id_answer = -1
    for element in cursor:
        try:
            id_answer = int(element["NUM"])
        except:
            success = False
            break
    if(success):
        query_string = 'INSERT INTO TER_HAS_ANSWER(id_question,id_answer,correct) VALUES ({},{},{});'.format(id_question,id_answer,correctness)
        insert_into_db(query_string)
        print("answer insert passed")
    else:
        print("failed")

def update_rank_question(id):
	query_string = "UPDATE TER_QUESTION set disable = disable + 1 where id_question in (SELECT id_question from TER_HAS_QUESTION where id_quiz = {} )".format(id)
	try:
		insert_into_db(query_string)
	except:
		return -1
	return 1

# difficulty : 100 - hard; 50 - ok; 0 - easy
def update_difficulty_db(id_question, note):
    query_string = "SELECT * FROM TER_QUESTION WHERE id_question = {}".format(id_question)
    cursor = init_connection(query_string)

    difficulty = -1
    for elt in cursor:
        difficulty = elt['difficulty']

    if(difficulty == None or difficulty == -1):
        newDifficulty = note
    else:
        notes = [difficulty, note]
        newDifficulty = mean(notes)

    query_string_update = "UPDATE TER_QUESTION SET difficulty = {} WHERE id_question = {}".format(newDifficulty, id_question)
    try:
        insert_into_db(query_string_update)
    except:
        return -1
    return 1

def get_id_question_by_quiz_number_question_db(id_quiz,num_question):
    query_string ="SELECT * FROM TER_QUESTION \
            JOIN TER_HAS_QUESTION USING (id_question) WHERE id_quiz = {} AND disable=0;".format(id_quiz)
    cursor = init_connection(query_string)

    list_question = []
    cpt = 0
    for data in cursor:
        if cpt == num_question:
            return data['id_question']
        cpt +=1
    return -1


def readBlackListFile():
    #https://github.com/splorp/wordpress-comment-blacklist/blob/master/blacklist.txt
    with open('./conf/blackList.txt', 'r', encoding="utf-8") as file:
        listBlackList = file.readlines()

    newBlackList = []
    for word in listBlackList:
        newBlackList.append(word.strip())
    return newBlackList


def sentenceInBlackList(phrase):
    liste = phrase.split(" ")
    blackList = readBlackListFile()
    for word in liste:
        if word.lower() in blackList:
            return True
    return False

