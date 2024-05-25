from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db///MagicLink.db", echo=True, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

def setupDatabase():
    with Session() as session:
        #session.execute(text("drop table if exists notes;"))
        #session.execute(text("drop table if exists user;"))
        session.execute(text(
            """
            create table if not exists user (
            id integer primary key
            , email varchar not null unique
            , created_date datetime default current_timestamp
            , user_token text
            , session_token text
            );
            """
        ))
        session.execute(text(
            """
            create table if not exists notes (
            id integer primary key
            , note text
            , created_date datetime default current_timestamp
            , user_id integer
            , foreign key (user_id) references user(id) on delete cascade
            );
            """
            # ON DELETE CASCADE: Ensures that if a user is deleted, all associated notes are also deleted.
        ))
        session.commit()

def initialiseData():
    return     

########################################################################
# User
########################################################################
def getUser(email):
    with Session() as session:
        sql = """
            select * from user where email = :email
            """
        user = session.execute(text(sql), {'email': email}).mappings().fetchone()
        if user:
            return user
        else:
            return None

def createUser(email):
    with Session() as session:
        try:
            sql = """
                insert into user (email) values (:email)
                """
            session.execute(text(sql), {'email': email})
            session.commit()
            user = getUser(email)
        except:
            session.rollback()
            raise   
    return user

def expireUserToken(email):
    with Session() as session:
        sql = """
            update user 
            set user_token = null 
            where email = :email
            """
        result = session.execute(text(sql), {'email': email})
        session.commit()
        if result.rowcount > 0:
            print("User token expired successfully.")
        else:
            print("Something went wrong")
        return

def setUserToken(email, user_token):
    with Session() as session:
        try:
            sql = """
                update user 
                set user_token = :user_token
                where email = :email
                """
            session.execute(text(sql), {
                'email': email,
                'user_token': user_token,
            })
            session.commit()
        except:
            session.rollback()
            raise            
    return

def setSessionToken(email, session_token):
    with Session() as session:
        try:
            sql = """
                update user 
                set session_token = :session_token
                where email = :email
                """
            session.execute(text(sql), {
                'email': email,
                'session_token': session_token,
            })
            session.commit()
        except:
            session.rollback()
            raise            
    return

########################################################################
# Note
########################################################################
def getNotes(current_user):
    with Session() as session:
        sql = """
            select * from notes where user_id = :user_id
            """
        result = session.execute(text(sql), {'user_id': current_user.id}).mappings().fetchall()
        if result:
            return result
        else:
            return None

def addNote(note, current_user):
    with Session() as session:
        try:
            sql = """
                insert into notes (note, user_id)
                values (:note, :user_id)
                returning *
                """
            result = session.execute(text(sql), {'note': note, 'user_id': current_user.id}).mappings().fetchone()
            session.commit()
            return result
        except:
            session.rollback()
            raise            
