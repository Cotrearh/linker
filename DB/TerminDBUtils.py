import re
from PyQt4.QtSql import QSqlQuery

from DB.data_base import get_remote_connection, get_local_connection
from DB.queries import get_definition_query, update_definition_query, count_word_in_db_query, get_definition_query_OC, \
    update_definition_query_OC
from utils.StringUtils import stem_str


def checkTerminExists(uuid, oc):
    remote_sql = QSqlQuery(get_remote_connection())
    if oc:
        remote_sql.prepare(get_definition_query_OC)
    else:
        remote_sql.prepare(get_definition_query)
    remote_sql.bindValue(":uuid", uuid.__str__())
    if remote_sql.exec_():
        if remote_sql.next():
            return True
        else:
            return False
    else:
        return False


def getDefinition(uuid, oc):
    remote_sql = QSqlQuery(get_remote_connection())
    if oc:
        remote_sql.prepare(get_definition_query_OC)
    else:
        remote_sql.prepare(get_definition_query)
    remote_sql.bindValue(":uuid", uuid.__str__())
    if remote_sql.exec_():
        if remote_sql.next():
            definition = remote_sql.value(0).__str__()
            definition = definition.replace('&nbsp;', ' ')
            definition = definition.replace(' </A>', '</A> ')
            fs = re.findall(r'<[Aa][^>]*> ', definition)
            for f in fs:
                new_f = f.strip()
                definition = definition.replace(f, new_f)
            return definition
        else:
            return None
    else:
        return None


def updateDefinition(uuid, definition, oc):
    remote_sql = QSqlQuery(get_remote_connection())
    if oc:
        remote_sql.prepare(update_definition_query_OC)
    else:
        remote_sql.prepare(update_definition_query)
    remote_sql.bindValue(":uuid", uuid.__str__())
    remote_sql.bindValue(":definition", definition.__str__())
    if remote_sql.exec_():
        return True
    else:
        return False


# status: 1 - найдено однозначное соответствие для ссылки, 2 - найдено несколько соответствий для ссылки
def prepareLinkFromWordInDB(word, html, exclude_uuid):
    try:
        html = html.split("<!--StartFragment-->")[1].split("<!--EndFragment-->")[0]
    except:
        html = word
    str = stem_str(word)
    remote_sql = QSqlQuery(get_local_connection())
    remote_sql.prepare(count_word_in_db_query)
    # remote_sql.prepare(search_word_in_db_query)
    remote_sql.bindValue(":word", str)
    remote_sql.bindValue(":exclude_uuid", exclude_uuid)
    if remote_sql.exec_():
        if remote_sql.next():
            num = remote_sql.value(0)
            if num == 0:
                return None
            elif num == 1:
                return {
                    'link': "<a href='termin##" + remote_sql.value(1) + "##status##1##word##" + word + "##inithtml##" +
                            html + "' style='color:green'>" + html + "</a>"
                }
            elif num > 1:
                return {
                    'link': "<a href='termin##" + str + "##status##2##word##" + word + "##inithtml##" + html +
                            "' style='color:red'>" + html + "</a>"
                }
        else:
            return None
    else:
        return None
