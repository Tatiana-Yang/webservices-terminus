from .db_access import *

############################################### CREATE USER/ AUTHENTIFICATION ####################################################################

def has_account_id_db(id_user):
	query_string = "SELECT * FROM TER_USER WHERE id_user ='{}'".format(id_user)
	cursor = init_connection(query_string)

	list_users = []
	for user in cursor:
		list_users.append(user["id_user"])
		list_users.append(user["name_user"])
		list_users.append(user["login_user"])

	if len(list_users) == 0:
		return -1
	else:
		return list_users

def has_account_db(user_login, user_pass):
	query_string = "SELECT * FROM TER_USER WHERE login_user = '{}' AND password_user = '{}'".format(user_login, user_pass)
	cursor = init_connection(query_string)

	list_users = []
	for user in cursor:
		list_users.append(user["id_user"])
		list_users.append(user["name_user"])
		list_users.append(user["login_user"])

	if len(list_users) == 0:
		return -1
	else:
		return list_users

def login_already_use_db(user_login):
	query_string = "SELECT * FROM TER_USER WHERE login_user = '{}'".format(user_login)
	cursor = init_connection(query_string)

	list_users = []
	for user in cursor:
		list_users.append(user["id_user"])

	if len(list_users) == 0:
		return False
	else:
		return True


def create_user_db(user_name, user_login, user_pass):
	login_use = login_already_use_db(user_login)
	if not login_use:
		query_string = "INSERT INTO TER_USER (name_user, login_user, password_user) VALUES ('{}', '{}', '{}')".format(user_name, user_login, user_pass)
		try:
			insert_into_db(query_string)
		except Exception as e :
			print(e)
			return False
		else:
			return True
	return False



def update_user_db(id_user, name_user, login_user, password_user):
	login_use = login_already_use_db(login_user)
	if not login_use:
		query_string = "UPDATE TER_USER SET name_user = CASE WHEN coalesce('{name}', '')='' THEN name_user ELSE '{name}' END,\
											login_user = CASE WHEN coalesce('{login}', '')='' THEN login_user ELSE '{login}' END,\
											password_user = CASE WHEN coalesce('{password}', '')='' THEN password_user ELSE '{password}' END \
											WHERE id_user = {id}".format(name=name_user, login=login_user, password=password_user, id=id_user)
		try: 
			insert_into_db(query_string)
		except:
			return False
		return has_account_id_db(id_user)
	return False

def delete_user_db(id_user):
	query_string = "DELETE FROM TER_CREATE_QUIZ WHERE id_user = '{}'".format(id_user)
	query_string1 = "DELETE FROM TER_USER WHERE id_user = '{}'".format(id_user)
	try:
		insert_into_db(query_string)
		insert_into_db(query_string1)
	except:
		return "error"
	return "deleted"
