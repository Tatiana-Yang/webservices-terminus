from .db_access import *

def get_types_question_db():
	cursor = init_connection("SELECT * FROM TER_TYPE_QUESTION")

	list_types_question_db = []
	for type_question in cursor:
		list_types_question_db.append({"id_type_question" : type_question["id_type_question"],
						 "name_type_question" : type_question["name_type_question"]})

	return list_types_question_db