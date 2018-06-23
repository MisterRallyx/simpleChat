import psycopg2

########## SOME CONSTANTES  ##########

# Database table constantes
MESSAGE_TABLE = "messages"
USER_TABLE = "users"


""" CONNEXION FUNCTION """

### Function who return a connection and cursor objects pointed on Database
## parameters :
##   -- database => database name
##   -- user => system user name who own the db
##   -- password => database's password
def cursor_on_db(database, user, password):
    try :
        conn = psycopg2.connect(dbname=database, user=user, password=password)
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
        errorCode = -1
        try:
            # SQL request
            SQL = "INSERT INTO {} (pseudo, mdp) VALUES (%s,%s);".format(USER_TABLE)
            # exuction of sql request
            cur.execute(SQL, (user, password))
            # consol message
            print("Successfully add user {}".format(user))
            return (True,errorCode)
        except psycopg2.Error as e:
            print("Cannot add user.")
            # case of username already taken
            if e.pgcode=='23505':
                print("User already exist")
                errorCode = 1
            # unknow error
            else:
                errorCode = 0
            return (False, errorCode)

### Function who add a message in database
## parameters :
##   -- message : text of message to add
##   -- user : user who sent the message
##   -- canal : Canal where the message is supposed to be send
##   -- cur => cursor on db
## return value :
##  -- True => message succesfully added
##  -- False => message not added
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


""" READ FUNCTION """

# Test fonction
if __name__=="__main__":
    #connection to db
    conn,cur = cursor_on_db("chat-python", "alexis", "tPgx9cyJJy")
    #try to add an user
    add_user("rally", "123", cur)
    #try to add a message
    add_message("test", "rally", "principal", cur)
    #commit change in db
    conn.commit()
