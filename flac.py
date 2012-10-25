#!/usr/bin/python3
#
# audiotranscode
#
# a cross-library (live) audio transcoding module
#
# Copyright (c) 2012 Tom Wallroth
#
# Sources on github:
# http://github.com/devsnd/audiotranscode
#
# licensed under GNU GPL version 3 (or later)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#

import subprocess
import os
import audiotranscode

devnull = open(os.devnull,'w')

formats = ['flac']

class LAME:
    def __init__(self):
        if not self.available():
            raise audiotranscode.TranscoderNotFound('flac')
        
    def encode(self, pcmDataPipe, newformat, bitrate=None):
        command = ['flac', '-c']
        enc = subprocess.Popen( audiotranscode.customizeCommand(command),
                                stdin=pcmDataPipe,
                                stdout=subprocess.PIPE,
                                stderr=devnull)
        return enc.stdout
        
    def decode(self, filePath):
        command = ['flac', '-F','-d', '-c', 'INFILE']
        dec = subprocess.Popen( audiotranscode.customizeCommand(command,infile=filePath),
                                stderr=devnull,
                                stdout=subprocess.PIPE)
        return dec.stdout

    def available():
        try:
            subprocess.Popen(['ffmpeg'],stdout=devnull, stderr=devnull)
            return True
        except OSError:
            return False