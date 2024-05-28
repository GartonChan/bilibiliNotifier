"""
Reference: 
    - https://www.cnblogs.com/lsdb/p/9835894.html
"""
from src.config import DatabaseURL

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime

def getTimestampsForToday():
    from datetime import time
    # Get the current date
    today = datetime.today().date()
    # Generate the beginning of today (00:00:00)
    start_of_today = datetime.combine(today, time.min)
    # Generate the end of today (23:59:59.999999)
    end_of_today = datetime.combine(today, time.max)
    return start_of_today, end_of_today

def getTimestapmsForNDaysAgo(N):
    theDate = datetime.today().date() - timedelta(N)
    startOfTheDate = datetime.combine(theDate, time.min)
    # Generate the end of today (23:59:59.999999)
    endOfTheDate = datetime.combine(theDate, time.max)
    return startOfTheDate, endOfTheDate

def timestampToDate(timestamp):
    dateobj = datetime.fromtimestamp(timestamp)
    # print("[timestampToDate]: ", dateobj.strftime("%Y-%m-%d %H:%M:%S"))
    return dateobj.strftime("%Y-%m-%d %H:%M:%S")

# Engine
engine = create_engine(DatabaseURL)  # sqlite://<nohostname>/<path>
conn = engine.connect()

# Model
Base = declarative_base()
class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(String(20))
    bvid = Column(String(20))
    created = Column(String(20))
    title = Column(String(128))
    pic = Column(String(128))
    length = Column(String(10))
    play = Column(Integer)
    
    def __repr__(self):
        return "<Post(mid='%s', bvid='%s', created='%s', title='%s, pic=%s')>" % (
                   self.mid, self.bvid, timestampToDate(int(self.created)), self.title, self.pic)

# create table if not exist
Base.metadata.create_all(engine, checkfirst=True)

# session
session = Session(engine)

# DB-related interfaces
def displayAll():
    print("---------- Query All ----------")
    for post in session.query(Post):
        print(post)
        # print(type(post) == Post)  # True

def displayNewest():
    print("---------- Query Newest ----------")
    post = session.query(Post).order_by(Post.created.desc()).first()
    print(post)
    # print(type(post) == Post)  # True

def addPost(post):
    if type(post) == Post:
        session.add(post)
        session.commit()
    else:
        print("parameter post is not a Post Type Class")

def queryNewestPostBymid(mid):
    res = session.query(Post).order_by(Post.created.desc()).filter_by(mid=mid).first()
    return res

def displayAllNewlyPost(mids: list):
    for mid in mids:
        res = queryNewestPostBymid(mid)
        print(res)

def checkUpdate(mid, newlypost, updateQueue):
    res = queryNewestPostBymid(mid)
    if (res.created < newlypost.created):
        # push to queue
        updateQueue.append(newlypost)
        # store in db
        addPost(newlypost)
    return updateQueue

def isTheSamePost(post1: Post, post2: Post):
    return (post1.mid == post2.mid 
            and post1.created == post2.created)

def isPostExisted(post: Post):
    query_post = session.query(Post).filter_by(mid=post.mid, created=post.created).first()
    if query_post:
        return True
    else:
        return False

def addUpdatePosts(postList: list):
    for each in postList:
        if type(each) == Post:
            session.add(each)
            print("Update: ", each)
    session.commit()
    return 0  # todo: should be the number of success adding

def main():
    # displayAll()
    # print(len(session.query(Post).all()))
    displayNewest()

if __name__ == "__main__":
    main()
    # rmPostsNDaysAgo(2)
