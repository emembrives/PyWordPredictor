# -*- coding: utf-8 -*-
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


class Quadruplet(SQLObject):
    w0 = ForeignKey("Word")
    w1 = ForeignKey("Word")
    w2 = ForeignKey("Word")
    w3 = ForeignKey("Word")
    occurences = IntCol()

class Word(SQLObject):
    data = StringCol()
    occurences = IntCol()

class Database(object):
    # Create a connection to the database (SQLite)
    def __init__(self,path=None):
        if path!=None:
            db_filename = os.path.abspath(path)
        else:
            db_filename = "/:memory:"
        connection_string = 'sqlite:' + db_filename

        #if os.path.exists(db_filename):
        #    os.unlink(db_filename)

        self.connection = connectionForURI(connection_string)
        sqlhub.processConnection = self.connection

    def clear(self):
        Word.dropTable()
        Quadruplet.dropTable()
        Word.createTable()
        Quadruplet.createTable()

        
