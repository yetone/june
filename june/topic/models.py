"""
Topic:
    topic must be in a node

    impact:
        for sorting topic

        1. when user reply a topic, impact increase:
            + (n1 + day_del * n2) * log(user.reputation)

        2. when user up vote a topic, impact increase:
            + n3 * log(user.reputation)

        3. when user down vote a topic, impact decrease:
            - n4 * log(user.reputation)

"""

import time
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Text
from july.database import db


def get_current_impact():
    return int(time.time())


class Topic(db.Model):
    id = Column(Integer, primary_key=True)
    node_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(200))
    content = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                      onupdate=datetime.utcnow)
    status = Column(String(40))
    hits = Column(Integer, default=1)

    up_count = Column(Integer, default=0)
    down_count = Column(Integer, default=0)

    #:TODO delete ups, downs
    #ups = Column(Text)  # e.g.  1,2,3,4
    #downs = Column(Text)

    reply_count = Column(Integer, default=0)
    last_reply_by = Column(Integer, default=0)
    last_reply_time = Column(DateTime, default=datetime.utcnow, index=True)

    impact = Column(Integer, default=get_current_impact, index=True)


class Reply(db.Model):
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    content = Column(String(2000))
    created = Column(DateTime, default=datetime.utcnow)

    accepted = Column(String(1), default='n')  # accepted by topic owner


class Vote(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    topic_id = Column(Integer, nullable=False, index=True)
    type = Column(String(10))


class TopicLog(db.Model):
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
