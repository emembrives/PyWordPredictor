from sqlobject import *
import re, datetime
import sys, os


# Create a connection to the database (SQLite)
db_filename = os.path.abspath('data.db')
connection_string = 'sqlite:' + db_filename

#if os.path.exists(db_filename):
#    os.unlink(db_filename)

connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

class Quadruplet(SQLObject):
    w1 = ForeignKey("Word")
    w2 = ForeignKey("Word")
    w3 = ForeignKey("Word")
    w4 = ForeignKey("Word")
    occurences = IntCol()

class Triplet(SQLObject):
    w1 = ForeignKey("Word")
    w2 = ForeignKey("Word")
    w3 = ForeignKey("Word")
    occurences = IntCol()

class Duplet(SQLObject):
    w1 = ForeignKey("Word")
    w2 = ForeignKey("Word")
    occurences = IntCol()

class Word(SQLObject):
    data = StringCol()
    occurences = IntCol()
    wordtopic=MultipleJoin("WordTopic")

class WordTopic(SQLObject):
    # Relation between a word and a topic

    # probability is given by beta as computed
    # by LDA
    probability=FloatCol()
    topic=ForeignKey("Topic")

class Topic(SQLObject):
    # A topic
    topicid=IntCol()
