only_classified_postfix = " AND uuid IN (SELECT termin_uuid FROM tb_ontology_rubrics_termins) "

#   Запросы списка терминов на вкладке РАсстановка ссылок
#   :search_str - поисковый образ, :linked - показывать уже перелинкованные термины
show_termins_in_list_query = "SELECT name, uuid, linked FROM termins WHERE name LIKE :search_str AND linked " \
                             "IN (:linked,0) AND was_deleted = 0 LIMIT :limit OFFSET :offset"
show_termins_in_list_count_query = "SELECT count(*) FROM termins WHERE name LIKE :search_str AND linked " \
                                   "IN (:linked,0) AND was_deleted = 0"

#   Запросы для класса обновления данных с сервера
count_termins_on_server_query = "SELECT count(*) FROM tb_dict_termins WHERE uuid IS NOT NULL"
count_termins_on_server_query_OC = "SELECT count(*) FROM tb_dict_termins WHERE uuid IS NOT NULL" + \
                                   only_classified_postfix
count_termins_local_query = "SELECT count(*) FROM termins"
select_termins_from_server_query = "SELECT uuid, name, homo FROM tb_dict_termins WHERE uuid IS NOT NULL ORDER BY " \
                                   "name, uuid LIMIT :limit OFFSET :offset"
select_termins_from_server_query_OC = "SELECT uuid, name, homo FROM tb_dict_termins WHERE uuid IS NOT NULL " + \
                                      only_classified_postfix + " ORDER BY " \
                                    "NAME, UUID LIMIT :LIMIT OFFSET :OFFSET"
select_termin_by_uuid_query = "SELECT name, was_deleted FROM termins WHERE uuid = :uuid"
update_termin_from_server_query = "UPDATE termins SET name = :name, linked = 0, was_deleted = 0," \
                                  " name_stemmed = :name_stemmed WHERE uuid = :uuid"


def add_termins_from_server_query(list):
    return "INSERT INTO termins(uuid, name, omonym_num, linked, name_stemmed) VALUES " + list


select_all_local_termins_query = "SELECT uuid, name FROM termins"
check_uuid_on_server_query = "SELECT uuid FROM tb_dict_termins WHERE uuid = :uuid"
check_uuid_on_server_query_OC = "SELECT uuid FROM tb_dict_termins WHERE uuid = :uuid" + only_classified_postfix
# delete_local_termin_by_uuid = "DELETE FROM termins WHERE uuid = :uuid"
delete_local_termin_by_uuid = "UPDATE termins SET was_deleted = 1 WHERE uuid = :uuid"
clear_all_termins_query = "DELETE FROM termins"


def delete_local_termins_by_uuid_list(list):
    return "UPDATE termins SET was_deleted = 1 WHERE uuid IN (" + list + ")"


def final_delete_local_termins_by_uuid_list(list):
    return "DELETE FROM termins WHERE uuid IN (" + list + ")"


broken_link_insert_query = "INSERT INTO broken_links(uuid, name) VALUES (:uuid, :name)"


def mark_as_deleted_query(list):
    return "UPDATE termins SET was_deleted = 1 WHERE uuid IN (" + list + ")"


#   выражение, удаляющее термин из списка битых ссылок, если термин был повторно загружен в фонд
check_deleted_restored_query = "DELETE FROM broken_links WHERE uuid IN (SELECT uuid FROM termins)"


def check_link_exist_by_uuid_query(uuid):
    return "SELECT name FROM tb_dict_termins WHERE definition LIKE '%<A href=\"termin;" + uuid + "\"%' LIMIT 1"


def check_link_exist_by_uuid_query_OC(uuid):
    return "SELECT name FROM tb_dict_termins WHERE definition LIKE '%<A href=\"termin;" + uuid + "\"%' " + \
           only_classified_postfix + " LIMIT 1"


#   Вкладка Битые ссылки
show_brokenlinks_in_list_query = "SELECT name, uuid FROM termins WHERE name LIKE :search_str AND was_deleted = 1 " \
                                 "LIMIT :limit OFFSET :offset"
show_brokenlinks_in_list_count_query = "SELECT count(*) FROM termins WHERE name LIKE :search_str AND was_deleted = 1"

# Работа с термином
get_definition_query = "SELECT definition FROM tb_dict_termins WHERE uuid = :uuid"
update_definition_query = "UPDATE tb_dict_termins SET definition = :definition WHERE uuid = :uuid"
get_definition_query_OC = "SELECT definition FROM tb_dict_termins WHERE uuid = :uuid" + only_classified_postfix
update_definition_query_OC = "UPDATE tb_dict_termins SET definition = :definition WHERE uuid = :uuid" + \
                             only_classified_postfix
search_word_in_db_query = "SELECT name, uuid FROM termins WHERE name_stemmed = :word"
# TODO возможно стоит сделать, чтобы не допускались ссылки не только на себя по УИД-ам, но и на омонимы?
count_word_in_db_query = "SELECT count(*), uuid FROM termins WHERE name_stemmed = :word AND uuid != :exclude_uuid"
search_word_in_db_query2 = "SELECT name, regexp_matches(name, :word) FROM tb_dict_termins"
get_name_and_short_def_query = "SELECT name, substr(definition, 0, 300) FROM tb_dict_termins WHERE uuid = :uuid"
search_word_in_db_query2_OC = "SELECT name, regexp_matches(name, :word) FROM tb_dict_termins" + only_classified_postfix
get_name_and_short_def_query_OC = "SELECT name, substr(definition, 0, 300) FROM tb_dict_termins WHERE uuid = :uuid" + \
                                  only_classified_postfix

# запросы окна выбора ссылок
show_termins_in_link_selector_query = "SELECT name, uuid FROM termins WHERE name_stemmed LIKE :search_str " \
                                      "AND was_deleted = 0 LIMIT :limit OFFSET :offset"

# запросы на сохранение термина в БД после расстановки ссылок
update_local_termin_query = "UPDATE termins SET linked = :linked WHERE uuid = :uuid"
update_remote_termin_query = "UPDATE tb_dict_termins SET definition = :definition WHERE uuid = :uuid"
update_remote_termin_query_OC = "UPDATE tb_dict_termins SET definition = :definition WHERE uuid = :uuid" + \
                                only_classified_postfix


# запросы для класса обработки битых ссылок
def find_all_termins_contains_link_to_uuid(uuid):
    return "SELECT uuid, definition FROM tb_dict_termins WHERE definition LIKE '%<A href=\"termin;" + uuid + "\"%'"


def find_all_termins_contains_link_to_uuid_OC(uuid):
    return "SELECT uuid, definition FROM tb_dict_termins WHERE definition LIKE '%<A href=\"termin;" + uuid + "\"%'" + \
           only_classified_postfix


full_delete_local_termin_by_uuid = "DELETE FROM termins WHERE uuid = :uuid"

select_all_broken_query = "SELECT uuid FROM termins WHERE was_deleted = 1"


def replace_uuid_in_links_query(uuid, new_uuid):
    return "UPDATE tb_dict_termins SET definition = REPLACE(definition, 'href=\"termin;" + uuid + \
           "\"', 'href=\"termin;" + new_uuid + "\"') WHERE definition LIKE '%<A href=\"termin;" + uuid + "\"%'"


def replace_uuid_in_links_query_OC(uuid, new_uuid):
    return "UPDATE tb_dict_termins SET definition = REPLACE(definition, 'href=\"termin;" + uuid + \
           "\"', 'href=\"termin;" + new_uuid + "\"') WHERE definition LIKE '%<A href=\"termin;" + uuid + "\"%'" + \
           only_classified_postfix
