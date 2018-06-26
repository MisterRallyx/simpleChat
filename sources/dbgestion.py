#! ../env/bin/python3
# coding: utf-8

import psycopg2

########## SOME CONSTANTES  ##########

# Database table constantes
MESSAGE_TABLE = "messages"
MESSAGE_ID = "id"
MESSAGE_TXT = "txt"
MESSAGE_SENDER = "expediteur"
MESSAGE_REMOVE = "suppr"
MESSAGE_DATE = "msg_date"
MESSAGE_CHANNEL = "canal"
#
USER_TABLE = "users"
DELETE_MARK = "suppr"
USER_USER = "pseudo"
USER_ADMIN = "admin"
USER_PASSWORD = "mdp"


""" CONNEXION FUNCTION """

### Function who return a connection and cursor objects pointed on Database
## parameters :
##   -- database => database name
##   -- user => system user name who own the db
##   -- password => database's password
def cursor_on_db(database, user, password):
    try :
        conn = psycopg2.connect(dbname=database, user=user, password=password)
        conn.autocommit = True # dont need to manual commit
        cur = conn.cursor()
        print("Connection etablished.")
        return conn,cur
    except Exception as e :
        print("Cannot connect to database.")
        print(e)
        return None


""" WRITE FUNCTION """

### Function who add an user to database
## parameters :
##   -- User => user name
##   -- password => user password
##   -- cur => cursor pointed on database
## return a tuple of values values :
##   -- First is a bool, True if user added, false overwise
##   -- an integrer : -1 if ok, 0 if not ok with unknow error, 1 if user already exist on db
def add_user(user, password, cur):
    if user!='' and user!=None:
        errorCode = 0
        added_user = False
        try:
            # test if user is already in DB
            if is_user_exist(user, cur):
                print("User already exist")
                errorCode = 1
            else:
                # SQL request
                SQL = "INSERT INTO {} (pseudo, mdp) VALUES (%s,%s);".format(USER_TABLE)
                # exuction of sql request
                cur.execute(SQL, (user, password))
                # consol message
                print("Successfully add user {}".format(user))
                errorCode = -1
                added_user = True
        except psycopg2.Error as e:
            print("Cannot add user.")
            # case of username already taken
            if e.pgcode=='23505':
                print("User already exist")
                errorCode = 1
            # unknow error
            else:
                errorCode = 0
    return (added_user, errorCode)

### Function who add a message in database
## parameters :
##   -- message : text of message to add
##   -- user : user who sent the message
##   -- canal : Canal where the message is supposed to be send
##   -- cur => cursor on db
## return value :
##   -- True => message succesfully added
##   -- False => message not added
def add_message(message, user, canal, cur):
    if message!='' and message!=None:
        try:
            SQL = "INSERT INTO {} (txt, expediteur, canal) VALUES (%s,%s,%s);".format(MESSAGE_TABLE)
            cur.execute(SQL,(message, user, canal))
            print("Message added to database.")
            return True
        except Exception as e:
            print("Cannot add message.")
            print(e)
            return False


### Function who mark a message as deleted using his id
## parameters :
##   -- msg_id => the id of the message ou want to mark as remove
##   -- cur => cursor on database
## return value :
##   -- True => message succesfully marked
##   -- False => message not marked
def delete_msg(msg_id, cur):
    if msg_id >= 0 :
        try :
            SQL = "UPDATE {} SET {} = true WHERE id = %s;".format(MESSAGE_TABLE, DELETE_MARK)
            cur.execute(SQL,str(msg_id))
            print("Message #{} deleted".format(msg_id))
            return True
        except Exception as e :
            print("Error, cannot delete message {}.".format(msg_id))
            print(e)
            return False
    print("Message ID must be > 0 for deleting a message.")
    return False


### Function who modifie admin privilege
## parameters :
##   -- bool => value to set
##   -- user => set on this user
##   -- cur => cursor on database
## return value :
##   -- True => user succesfully modified
##   -- False => user not modified
def set_admin_privilege(bool, user, cur):
    try :
        SQL = "UPDATE {} SET {} = %s WHERE {} = %s;".format(USER_TABLE, USER_ADMIN, USER_USER)
        cur.execute(SQL, (bool, user))
    except Exception as e :
        print("Error occured, cannot set admin privilege.")
        print(e)


""" READ FUNCTION """
# # TODO: user_login()

### Function who return if user exist
## parameters :
##   -- user => interested user
##   -- cur => cursor on database
## return value :
##   -- True => user is in DB
##   -- False => user is not in DB
def is_user_exist(user, cur):
    try :
        SQL = "SELECT {} FROM {} WHERE {} = \'{}\' ;".format(USER_USER, USER_TABLE, USER_USER, user)
        cur.execute(SQL)
        res = cur.fetchall()
        if res == []:
            print("User {} doesn't exist in database.".format(user))
            return False
        return True
    except Exception as e:
        print("An error occured during the research of user {}".format(user))
        print(e)
        return False

### Function who return if user is admin
## parameters :
##   -- user => interested user
##   -- cur => cursor on database
## return value :
##   -- True => user is an admin
##   -- False => user is not an admin
def is_user_admin(user, cur):
    try:
        SQL = "SELECT {},{} FROM {} WHERE {} = \'{}\';".format(USER_USER, USER_ADMIN, USER_TABLE, USER_USER, user)
        cur.execute(SQL)
        res = cur.fetchall()
        if res == []:
            print("User {} can't be an admin, he is not on database.")
            return False
        return res[0][1]
    except Exception as e :
        print("An error occured in is_user_admin.")
        print(e)
        return False

### Function who a message by is identifier id
## parameters :
##   -- id => id of the message
##   -- cur => cursor on database
## return value :
##   -- (SENDER, TEXTE, DATE, CHANNEL) => the SENDER of the message and the TEXTE of message.
def get_message(id, cur):
    try :
        if id < 0:
            print("Cannot have a negative ID for a message.")
            return None
        SQL = "SELECT {},{},{},{},{} FROM {} WHERE {} = %s;".format(MESSAGE_ID, MESSAGE_TXT,MESSAGE_SENDER,MESSAGE_DATE,MESSAGE_CHANNEL, MESSAGE_TABLE, MESSAGE_ID)
        cur.execute(SQL, str(id))
        res = cur.fetchall()
        return (res[0][2], res[0][1], res[0][3], res[0][4])
    except Exception as e:
        print("Cannot get message.")
        print(e)
        return (None,None)

### Function who return if a message was remove
## parameters :
##   -- id => id of the message
##   -- cur => cursor on database
## return value :
##   -- True if message deleted, false overwise
def is_msg_deleted(msg_id, cur):
    # invalid parameters
    if msg_id<0 or cur==None:
        print("Wrong argument in is_message_deleted().")
        return False
    # SQL request
    try :
        SQL = "SELECT {} FROM {} WHERE {} = %s;".format(MESSAGE_REMOVE, MESSAGE_TABLE, MESSAGE_ID)
        cur.execute(SQL, str(msg_id))
        res = cur.fetchall()
        return res[0][0]
    except Exception as e:
        print("Fatal error in is_message_deleted().")
        print(e)
        return False


def is_good_password(user, password, cur):
    if cur==None:
        print("Wrong parameters in is_good_login.")
        return False
    try :
        # get password of user in parameter
        SQL = 'SELECT {} FROM {} WHERE {} = \'{}\';'.format(USER_PASSWORD, USER_TABLE, USER_USER, user)
        cur.execute(SQL)
        res = cur.fetchall()
        # no result = user doesn't exist
        if res==[]:
            print("User {} doesn't exist. Cannot login.".format(user))
            return False
        # if password match
        elif res[0][0]==password:
            print("Good login for user {}.".format(user))
            return True
        print("Wrong login for user {}.".format(user))
        return False
    except Exception as e:
        print("Fatal error in is_good_login().")
        print(e)
        return False


# Test fonction
if __name__=="__main__":
    res = True
    #connection to db
    conn,cur = cursor_on_db("chat-python", "alexis", "tPgx9cyJJy")
    #try to add an user
    add_user = add_user("rally", "123", cur)
    res = add_user[0] and res
    #try to add a message
    res = add_message("test", "rally", "principal", cur) and res
    #try is user exist
    res = not (is_user_exist("alexis", cur)) and res
    res = is_user_exist("rally", cur) and res
    # Test is_user_admin and set_admin_privilege()
    res = not(is_user_admin("rally", cur)) and res
    set_admin_privilege(True, "rally", cur)
    res = is_user_admin("rally", cur) and res
    set_admin_privilege(False, "rally", cur)
    res = not(is_user_admin("rally", cur)) and res
    # Test get_message()
     # Cannot test date
    msg = get_message(1, cur)
    res = msg[0]==('rally') and res
    res = msg[1]==('test') and res
    res = msg[3]==('principal') and res
    # Test delete_msg()
    res = not(is_msg_deleted(1, cur)) and res
    delete_msg(1, cur)
    res = is_msg_deleted(1, cur) and res
    # Test is_good_password
    res = is_good_password('rally', '123', cur) and res
    res = not(is_good_password('rally', '12', cur)) and res # wrong password
    res = not(is_good_password('rall', '123', cur)) and res # wrong user

    # test result
    print("\n##### Résulat du test : #####")
    if res :
        print("OK.")
    else :
        print("Failed.")
