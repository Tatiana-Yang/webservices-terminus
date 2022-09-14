from .db_access import *
from .question import *
from .tag import *

def get_user_quiz_db(id_user):
    query_string = "SELECT * FROM TER_QUIZ WHERE id_quiz IN (SELECT id_quiz FROM TER_CREATE_QUIZ WHERE id_user = {})".format(id_user)
    cursor = init_connection(query_string)

    list_quizs = []
    for quiz in cursor:
        list_quizs.append({'id_quiz': quiz['id_quiz'],'name_quiz' : quiz['name_quiz']})
    return list_quizs

def get_quiz_db(id_quiz):
    query_string ="SELECT * FROM TER_QUIZ \
                    JOIN TER_HAS_QUESTION USING (id_quiz)\
                    JOIN TER_QUESTION USING (id_question)\
                    JOIN TER_HAS_ANSWER USING (id_question)\
                    JOIN TER_TYPE_QUESTION USING (id_type_question)\
                    JOIN TER_ANSWER USING (id_answer) WHERE id_quiz = {} AND disable=0;".format(id_quiz)
    cursor = init_connection(query_string)

    #quiz_object = {'id_quiz':id_quiz}
    questions ={'id_quiz':id_quiz, "name_quiz": '', "questions": []}
    idQuestion = ''
    answers = []
    id_type =  ''
    id_tag = ''
    question_name = ''
    for data in cursor:
        if questions.get('name_quiz') == '':
            questions['name_quiz'] = data['name_quiz']

        if(idQuestion != data["id_question"] ):
            id = 0
            if idQuestion != '':
                questions.get('questions').append({"id_question": idQuestion, "question_name": question_name, "question_tag": id_tag, "question_type": id_type, "answers": answers })
            id_type =  {"id_type_question" : data["id_type_question"],"name_type_question" : data["name_type_question"]}
            id_tag = data["id_tag"]
            question_name = data["question"]
            idQuestion = data["id_question"]
            answers = []

        answers.append({'answer_name': data['answer'],'is_correct' : data['correct'], 'answer_num': id})
        id += 1
    questions.get('questions').append({"id_question": idQuestion, "question_name": question_name, "answers": answers, "question_type": id_type, "question_tag": id_tag })
    return questions

def get_quiz_by_question_number_db(id_quiz,num_question):
    query_string ="SELECT * FROM TER_QUIZ \
            JOIN TER_HAS_QUESTION USING (id_quiz)\
            JOIN TER_QUESTION USING (id_question)\
            JOIN TER_HAS_ANSWER USING (id_question)\
            JOIN TER_ANSWER USING (id_answer) WHERE id_quiz = {} AND disable=0;".format(id_quiz)
    cursor = init_connection(query_string)
    question_object = {}
    for data in cursor:
        if question_object.get(data['question'],-1) != -1:
            question_object[data['question']].append({'answer': data['answer'],'correct' : data['correct']})
        else:
            question_object[data['question']] = [{'answer':data['answer'],'correct': data['correct']}]
    cpt = 0
    for element in question_object.items():
        if cpt == num_question:
            return {'question' : element[0],'answers':element[1]}
        cpt +=1
    return {}

def insert_quiz_in_ter_quiz_ter_create_quiz(name_quiz,id_user):
    query_string = 'INSERT INTO TER_QUIZ (name_quiz) VALUES ("{}");'.format(name_quiz)
    insert_into_db(query_string)
    query_string = "SELECT MAX(id_quiz) as NUM FROM TER_QUIZ;"
    cursor = init_connection(query_string)

    success = True
    id_quiz = -1
    for element in cursor:
        try:
            id_quiz = int(element["NUM"])
        except:
            success = False
            break
    if(success):
        query_string = 'INSERT INTO TER_CREATE_QUIZ(id_user,id_quiz) VALUES ({},{});'.format(id_user,id_quiz)
        insert_into_db(query_string)
        print("quiz insert passed")
        return id_quiz
    else:
        print("failed not insert on db TER_CREATE_QUIZ")
        return -1

def insert_quiz_in_db(quizz):
    id_user = quizz['id']
    name_quiz = quizz['nomQuizz']
    questions = quizz['questions']

    id_quiz = insert_quiz_in_ter_quiz_ter_create_quiz(name_quiz,int(id_user))
    if(id_quiz != -1):
        for question in questions:
            id_type = get_id_type_question(question['typeChoisi'])
            id_question = insert_question_in_ter_question_ter_has_question(id_quiz,question['intitule'],question['themeChoisi'], id_type )
            if(id_question != -1):
                answers = question['answers']
                correctness = question['checkedAnswers']
                for index,answer in enumerate(answers):
                    isCorrect = 1 if str(index) in correctness else 0
                    insert_answer_in_ter_answer_ter_has_answer(id_quiz,id_question,answer,isCorrect)


def insert_quiz_generate_in_db(quiz):
    id_user = quiz['id']
    name_quiz = quiz['nomQuizz']
    questions = quiz['questions']

    id_quiz = insert_quiz_in_ter_quiz_ter_create_quiz(name_quiz,int(id_user))
    for question in questions:
        id_question = insert_question_in_ter_has_question(id_quiz,question['id_question'])

############################################### GENERATE QUIZ ####################################################################

def generate_quiz_from_tag_db(tag, nbQuestions):
	query_string = "SELECT * FROM TER_QUESTION WHERE id_tag = {} AND disable = 0 ORDER BY RANDOM() LIMIT {}".format(tag, nbQuestions)
	cursor = init_connection(query_string)
	list_questions = []
	for question in cursor:
		list_questions.append({"id_question":question["id_question"],
								"intitule" : question["question"],
								"name_tag" : get_tag_by_id_db(tag)[0],
								"difficulty" : question["difficulty"]
								})
	return list_questions

def generate_quiz_nb_db(nbQuestions):
	query_string = "SELECT * FROM TER_QUESTION WHERE disable = 0 ORDER BY RANDOM() LIMIT {}".format(nbQuestions)
	cursor = init_connection(query_string)
	list_questions = []
	for question in cursor:
		list_questions.append({"id_question":question["id_question"],
								"intitule" : question["question"],
								"name_tag" : question["id_tag"],
								"difficulty" : question["difficulty"]
								})

	for question in list_questions:
		question['name_tag'] = get_tag_by_id_db(question['name_tag'])[0]

	return list_questions

def get_colors_from_db(id_quiz):
    query_string = "SELECT color_tag FROM TER_QUIZ\
                    JOIN TER_HAS_QUESTION using (id_quiz)\
                    JOIN TER_QUESTION using(id_question)\
                    JOIN TER_TAG using (id_tag)\
                    WHERE id_quiz = {}".format(id_quiz)
    cursor = init_connection(query_string)
    colors = []
    for color in cursor:
        colors.append(color['color_tag'])
    return colors


############################################### UPDATE QUIZ ####################################################################

def update_quiz_in_db(quizz):
    id_quiz = quizz['id_quiz']
    name_quiz = quizz['nomQuizz']
    questions = quizz['questions']

    update_rank_question(id_quiz)
    for question in questions:
        id_type = get_id_type_question(question['typeChoisi'])
        id_question = insert_question_in_ter_question_ter_has_question(id_quiz,question['intitule'],question['themeChoisi'], id_type)
        if(id_question != -1):
            answers = question['answers']
            correctness = question['checkedAnswers']
            for index,answer in enumerate(answers):
                isCorrect = 1 if str(index) in correctness else 0
                insert_answer_in_ter_answer_ter_has_answer_with_id(id_quiz,id_question,answer,isCorrect)
    return "ok"

def quiz_content_blackList(quiz):
    name_quiz = quiz['nomQuizz']
    questions = quiz['questions']
    if(sentenceInBlackList(name_quiz)):
        return True
    for question in questions:
        if(sentenceInBlackList(question['intitule'])):
            return True
    return False