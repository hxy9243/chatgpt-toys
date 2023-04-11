from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from flaskapp.config import db


class Document(db.Model):
    __tablename__ = 'documents'
    docid = db.Column('id', db.String(16), primary_key=True)
    doctype = db.Column('type', db.String(16), default='text')
    hash = db.Column('hash', db.String(64))
    body = db.Column('body', db.Text)
    ntokens = db.Column('ntokens', db.Integer)

    conversations = relationship(
        'Conversation',
        cascade="all, delete-orphan",
        back_populates='doc',
    )

    def __repr__(self):
        return f'<Document {self.docid}>'

    def data(self):
        return {
            'id': self.docid,
            'body': self.body,
            'type': self.doctype,
        }


class Conversation(db.Model):
    __tablename__ = 'conversations'
    convid = db.Column('id', db.String(16), primary_key=True)
    docid = db.Column('docid', db.String(16),
                      ForeignKey(Document.docid),
                      nullable=False,
                      )
    user = db.Column('user', db.String(16))

    doc = relationship(
        'Document', back_populates='conversations',
    )
    messages = relationship(
        'Message',
        cascade='all, delete-orphan',
        back_populates='conversation'
    )

    def __repr__(self):
        return f'<Conversation {self.convid}>'

    def data(self):
        return {
            'id': self.convid,
            'docid': self.docid,
            'user': self.user,
        }


class Message(db.Model):
    __tablename__ = 'messages'
    msgid = db.Column('id', db.String(16), primary_key=True)
    convid = db.Column('convid', db.ForeignKey('conversations.id'),
                       nullable=False)
    index = db.Column('index', db.Integer)
    msg = db.Column('message', db.Text)
    msgtype = db.Column('type', db.String(32))
    context = db.Column('context', db.Text)
    ntokens = db.Column('ntokens', db.Integer)
    time = db.Column('time', db.DateTime)

    conversation = relationship(
        'Conversation', back_populates='messages',
    )

    def __repr__(self):
        return f'<Message {self.convid}>'

    def data(self):
        return {
            'convid': self.convid,
            'id': self.msgid,
            'index': self.index,
            'msg': self.msg,
            'msgtype': self.msgtype,
            'context': self.context,
            'ntokens': self.ntokens,
            'time': self.time.isoformat(),
        }