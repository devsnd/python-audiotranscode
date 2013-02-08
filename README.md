audiotranscode
==============

python module to transcode between audio formats using the CLI frontends of the codecs already installed on your system

-  faac
-  lame
-  ffmpeg
-  oggvorbis
-  flac

Using audiotranscode is as easy as py:

    import audiotranscode
    at = audiotranscode.AudioTranscode()
    at.transcode('path/to/some.mp3','output/path.ogg')

As of now audiotranscode can transcode between any of the following formats:

 - mp3
 - ogg
 - aac

And can additionally decode those formats:

 - flac
