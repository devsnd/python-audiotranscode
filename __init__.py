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
import re
import os
import logging as log
import tempfile

log.e = log.error
log.w = log.warning
log.i = log.info
log.d = log.debug

TRANSCODE_BUFFER = 1024*200
STREAM_BUFFER = 1024*150 # must be smaller than TRANSCODE_BUFFER!
DEFAULT_BITRATE_OGG = 160
DEFAULT_BITRATE_MP3 = 192
devnull = open(os.devnull,'w')

Encoders = {
    #encoders take input and write output from stdin and stout
    'ogg' : ['oggenc', '-b','BITRATE_OGG','-'],
    'mp3' : ['lame','-b','BITRATE_MP3','-','-'],
    #'aac': ['faac','-o','-','-'], #doesn't work yet
}

Decoders = {
    #filepath must be appendable!
    'mp3'   : ['mpg123', '-w', '-'],
    'ogg'   : ['oggdec', '-o', '-'],
    'flac'  : ['flac', '-F','-d', '-c'],
    'aac'   : ['faad', '-w'],        #untested
    
    #'fallback' : ['mplayer','-vc','null','-vo','null','-ao' 'pcm:waveheader:fast:file=-'],
}


def getEncoders():
    return list(Encoders.keys())
    
def getDecoders():
    return list(Decoders.keys())


def __init__():
    unavailEnc = []
    for k,v in Encoders.items():
        if not programAvailable(v[0]):
            unavailEnc.append((k,v[0]))
        else:
            log.i("Encoder '{}' for format '{}' was found.".format(v[0],k))
    for enc in unavailEnc:
        Encoders.pop(enc[0])
        log.i("Encoder '{}' not found. Will not be able to encode {} streams".format(enc[1], enc[0]))
    
    unavailDec = []
    for k,v in Decoders.items():
        if not programAvailable(v[0]):
            unavailDec.append((k,v[0]))
        else:
            log.i("Decoder '{}' for format '{}' was found.".format(v[0],k))
    for dec in unavailDec:
        Decoders.pop(dec[0])
        log.i("Decoder '{}' not found. Will not be able to encode {} streams".format(dec[1],dec[0]))
    
def programAvailable(name):
    try:
        subprocess.Popen([name],stdout=devnull, stderr=devnull)
        return True
    except OSError:
        return False

def decode(filepath):
    try:
        return subprocess.Popen(Decoders[filetype(filepath)]+[filepath], stdout=subprocess.PIPE, stderr=devnull)
    except OSError:
        log.w("Cannot decode {}, no decoder available, trying fallback decoder!".format(filepath))
        try:
            return subprocess.Popen(Decoders[filetype(filepath)]+[filepath], stdout=subprocess.PIPE)#, stderr=devnull)
        except OSError:
            log.w("Fallback failed, cannot decode {}!".format(filepath))
            raise

def encode(newformat, fromdecoder):
    try:
        enc = Encoders[newformat]
        if 'BITRATE_OGG' in enc:
            enc[enc.index('BITRATE_OGG')] = str(DEFAULT_BITRATE_OGG)
        if 'BITRATE_MP3' in enc:
            enc[enc.index('BITRATE_MP3')] = str(DEFAULT_BITRATE_MP3)
        return subprocess.Popen(enc, stdin=fromdecoder.stdout, stdout=subprocess.PIPE)#, stderr=devnull)
    except OSError:
        log.w("Cannot encode to {}, no encoder available!")
        raise
   
def transcode(filepath, newformat):
    log.e("""Transcoding file {}
{} ---[{}]---> {}""".format(filepath,filetype(filepath),Encoders[newformat][0],newformat))
    try:
        fromdecoder = decode(filepath)
        encoder = encode(newformat, fromdecoder)
        while True:
            data = encoder.stdout.read(TRANSCODE_BUFFER)
            if not data:
                break               
            yield data
                    
    except OSError:
        log.w("Transcode of file '{}' to format '{}' failed!".format(filepath,newformat))
        
def getTranscoded(filepath, newformat, usetmpfile=False):
    needsTranscoding = True
    if usetmpfile:
        tmpfilepath = cache.createCacheFile(filepath,newformat)
        if cache.exists(filepath,newformat):
            yield open(tmpfilepath,'rb').read()
        else:
            tmpfilew = open(tmpfilepath,'wb')
            tmpfiler = open(tmpfilepath,'rb')
            for data in transcode(filepath,newformat):
                tmpfilew.write(data)
                #return as soon as enough data available
                if tmpfilew.tell()>tmpfiler.tell()+STREAM_BUFFER:
                    yield tmpfiler.read(STREAM_BUFFER) 
            yield tmpfiler.read() #return rest of file (encoding done)

    else:
        for data in transcode(filepath,newformat):
            yield data

def customizeCommand(command, bitrate=192, infile=None):
    if 'BITRATE' in command:
        command[command.index('BITRATE')] = bitrate
    if 'INFILE' in command:
        command[command.index('INFILE')] = infile
    return command
        