audiotranscode
==============

[![Build Status](https://travis-ci.org/devsnd/python-audiotranscode.svg?branch=master)](https://travis-ci.org/devsnd/python-audiotranscode)

python module to transcode between audio formats using the CLI frontends of the codecs already installed on your system, e.g lame, vorbis-tools etc

supported python versions:
 - 2.6
 - 2.7
 - 3.2
 - 3.3
 - pypy


supported formats
-----------------

As of now audiotranscode can transcode between any of the following formats:

_filetype_ _(program used)_

 - mp3 (lame, ffmpeg)
 - ogg (vorbis oggenc/oggdec, ffmpeg)
 - aac/m4a (faac, faad)
 - flac (flac)
 - wav

command line usage
------------------

    audiotranscoder [-b BITRATE] <infile> <outfile>

```bitrate``` is specified in kbits/s.
```<input>``` is the path to the file that needs to be transcoded.
```<output>``` is the output path. The file extension of the output determines the output format

    audiotranscoder --codecs

shows all installed codecs


programatical usage
-------------------

Using audiotranscode is as easy as py:

    import audiotranscode
    at = audiotranscode.AudioTranscode()
    at.transcode('path/to/some.mp3','output/path.ogg')
    
you can also set the bitrate of the output stream, like so:

    at.transcode('path/to/some.aac','output/path.mp3',bitrate=128)
    
You can also get the encoded data on the fly for live transcoding:

    for data in at.transcode_stream('path/to/some.flac','mp3'):
        # do something with chuck of data
        # e.g. sendDataToClient(data)
        
If you need to know which formats can be transcoded:

    at = audiotranscode = AudioTranscode()
    at.available_encoder_formats() #returns list like ['mp3','ogg', ...]
    at.available_decoder_formats() #returns list like ['mp3','ogg', ...]
        
limitations
-----------

As of now, i have only tested 16bit, 44100Hz, 2 channel audio, since it is the most used, other formats might or might not work.

But feel free fork this repo and to add stuff!
