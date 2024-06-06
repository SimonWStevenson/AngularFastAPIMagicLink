from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db///MagicLink.db", echo=True, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

def setupDatabase():
    with Session() as session:
        #session.execute(text("drop table if exists sessions;"))
        #session.execute(text("drop table if exists notes;"))
        #session.execute(text("drop table if exists user;"))
        session.execute(text(
            """
            create table if not exists user (
            id integer primary key
            , email varchar not null unique
            , created_date datetime default current_timestamp
            , user_token text
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

        session.execute(text(
            """
            create table if not exists sessions (
            id integer primary key
            , created_date datetime default current_timestamp
            , user_id integer
            , browser text
            , browser_version text
            , os text
            , os_version text
            , device text
            , device_brand text
            , device_model text
            , is_mobile integer
            , is_tablet integer
            , is_pc integer
            , is_bot integer
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
            session.rollback()
            raise
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

def setSessionToken(user_id, device_info):
    with Session() as session:
        try:
            sql = """
                insert into sessions (user_id, browser, browser_version, os, os_version, device, device_brand, device_model, is_mobile, is_tablet, is_pc, is_bot)
                values (:user_id, :browser, :browser_version, :os, :os_version, :device, :device_brand, :device_model, :is_mobile, :is_tablet, :is_pc, :is_bot)
                returning *
                """
            result = session.execute(text(sql), {
                'user_id': user_id,
                'browser': device_info['browser'],
                'browser_version': device_info['browser_version'],
                'os': device_info['os'],
                'os_version': device_info['os_version'],
                'device': device_info['device'],
                'device_brand': device_info['device_brand'],
                'device_model': device_info['device_model'],
                'is_mobile': device_info['is_mobile'],
                'is_tablet': device_info['is_tablet'],
                'is_pc': device_info['is_pc'],
                'is_bot': device_info['is_bot'],
            }).mappings().fetchone()
            session.commit()
            return result
        except:
            session.rollback()
            raise            

def getSessionToken(email, session_id):
    with Session() as session:
        sql = """
            select s.* from user u
            inner join sessions s on u.id = s.user_id
            where 
                u.email = :email 
                and s.id = :session_id
            """
        result = session.execute(text(sql), {'email': email, 'session_id': session_id}).mappings().fetchone()
        if result:
            return result
        else:
            return None

def getSessions(user_id, session_id):
    with Session() as session:
        sql = """
            select 
                u.email
                , s.*
                , case when s.id = :session_id then 1 else 0 end as is_this_session
            from user u
            inner join sessions s on u.id = s.user_id and u.id = :user_id
            """
        result = session.execute(text(sql), {'user_id': user_id, 'session_id': session_id}).mappings().fetchall()
        if result:
            return result
        else:
            return None

def deleteSession(user_id, session_id):
    with Session() as session:
        try:
            sql = """
                delete from sessions where user_id = :user_id and id = :session_id
                returning *
                """
            result = session.execute(text(sql), {
                'user_id': user_id,
                'session_id': session_id,
            }).mappings().fetchone()
            session.commit()
            return result
        except:
            session.rollback()
            raise

########################################################################
# Note
########################################################################
def getNotes(current_user):
    with Session() as session:
        sql = """
            select * from notes where user_id = :user_id
            """
        result = session.execute(text(sql), {'user_id': current_user.user_id}).mappings().fetchall()
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
            result = session.execute(text(sql), {'note': note, 'user_id': current_user.user_id}).mappings().fetchone()
            session.commit()
            return result
        except:
            session.rollback()
            raise            
