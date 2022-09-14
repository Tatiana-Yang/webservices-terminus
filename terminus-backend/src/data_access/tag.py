from .db_access import *

def get_tags_db():
	cursor = init_connection("SELECT * FROM TER_TAG")

	list_tags = []
	for tag in cursor:
		list_tags.append({"id_tag" : tag["id_tag"],
						 "name_tag" : tag["name_tag"],
						  "color_tag": tag["color_tag"]})

	return list_tags

def get_tag_by_id_db(id):
	query_string = "SELECT * FROM TER_TAG WHERE id_tag = {}".format(id)
	cursor = init_connection(query_string)

	list_tags_names = []
	for tag in cursor:
		list_tags_names.append(tag['name_tag'])

	return list_tags_names

def get_tag_by_name_db(name):
    query_string = "SELECT * FROM TER_TAG WHERE trim(upper(name_tag)) = trim(upper({}));".format(name)
    cursor = init_connection(query_string)
    list_tags_names = []
    for tag in cursor:
        list_tags_names.append(tag['id_tag'])

    if(len(list_tags_names) !=0):
        return list_tags_names
    else:
        return -1
