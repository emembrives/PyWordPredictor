# PyWordPredictor - XML-RPC word prediction server
# Copyright (C) 2010 - Etienne Membrives
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

    # probability is given by beta as computed by LDA,
    #  expressed as log of the real p(w|t=k)
    probability=FloatCol()
    word=ForeignKey("Word")
    topic=ForeignKey("Topic")

class Topic(SQLObject):
    # A topic
    topicid=IntCol()
