#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
#
# Copyright (C) 2005-2006 David Guerizec <david@guerizec.net>
#
# Last modified: 2006 Jun 02, 00:08:36 by david
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA


import os.path

from SSHproxy import config
from SSHproxy import keys

class PluginLogUsers(object):
    tr_table = {}
    _tr_table = {
            '\r\n':         '\n',
            '\r':           '\n',
            '\n':           '\n',
            '<':            '<INF>',
            '>':            '<SUP>',
        }
    def __init__(self):
        conf = config.SSHproxyConfig()
        if not hasattr(conf, 'logusers_dir'):
            conf.logusers_dir = '/tmp/sshproxy_logusers'
            conf._write()
        if not os.path.isdir(conf.logusers_dir):
            os.mkdir(conf.logusers_dir)
        
        self.path = conf.logusers_dir

        for key in dir(keys):
            if key[0] == '_' or not isinstance(getattr(keys, key), str):
                continue
            self.tr_table[getattr(keys, key)] = '<%s>' % key

        for key, value in self._tr_table.items():
            self.tr_table[key] = value

    def logusers(self, console, chan, sitedata, char):
        user = sitedata.userdata.username
        path = os.path.join(self.path, user)
        if not os.path.isdir(path):
            os.mkdir(path)

        logfile = os.path.join(path, sitedata.sitename)
        log = open(logfile, 'a')
        log.write(self.translate(char))
        log.close()

    def translate(self, char):
        return self.tr_table.get(char, char)
        if self.tr_table.has_key(char):
            return self.tr_table[char]
        return char
        

