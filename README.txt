Introduction
============

unimr.red5.protectedvod implements a video-on-demand (vod) or
audio-on-demand solution for secure flash streaming with `Red5
server`_. It provides a way to protect your media files from being
directly downloaded from Plone or from being "leeched" by other
sites. For this purpose the streaming URL is secured by altering the
requested URL with a signature. When the video/audio file is requested,
the path of the file is individually signed by Plone for each request
and the streaming is delegated to Red5. Red5 checks afterwards the
signature of the incoming request for validity by a shared secret
(only known by Plone and Red5!). If the signature is valid Red5
delivers the stream. The signature is unique, context specific and its
duration of validity is limited. Plone's security context is therefore
completely preserved in Red5. Nobody can copy-and-paste that URL
anywhere he want and load the video.

.. _`Red5 server`: http://osflash.org/red5


Installation
============

Product
-------

Add unimr.red5.protectedvod to your buildout as normal. See 
http://plone.org/documentation/tutorial/buildout. Don't forget to 
load the configure.zcml file!

Then install the product via Plone's Add-on products control panel.


FileSystemStorage
-----------------

Both Plone and Red5 require a shared file system with read/write
access. Follow the installation instructions of iw.fss_ and remember
that only site storage strategies *site1* and *site2* are supported by
unimr.red5.protectedVOD. Red5 needs the file extension of the
media content to work.

.. _iw.fss: http://pypi.python.org/pypi/iw.fss

Configuration
-------------

In portal_properties/red5_protectedvod_properties you have to
configure the Red5 server URL, TTL (time to live) in sec of your
signature and the shared secret for generating the signature.

   :red5_server_url: rtmp://<red5_hostname>/protectedVOD
   :ttl:             60
   :secret:          <top_secret>


Example Archetype
=================

The included Archetype *Red5Stream* integrates the GPL version of
flowplayer_ with Plone 3.x. It can play video files (FLV, H.246, MP4)
as well as audio files (MP3). Clients with "view" permission can only
view the content by the streaming technique of Red5 but cannot
directly download the content. Per default only clients with owner or
manager role have the "Download Red5Stream" permission to download the
content from Plone.

.. _flowplayer: http://www.flowplayer.org


Kupu integration 
----------------

To make it easier to present Red5Streams within a content item of Plone,
this product installs a new Kupu paragraph style. You can use them
like this:

   1. Insert the image you want to use as a splash image. You
      should insert this "inline" (rather than left/right floating),
      preferably in its own paragraph. Alternatively, you can also
      enter a text as placeholder.

   2. Select on the image (or placeholder text), and make it link
      to the .flv or .mp3 file you want to play.
       
   3. Select the *red5-stream* style from the styles drop-down.


Signature & streaming URL
=========================

The dynamically signed streaming URL takes the following format:

    **rtmp://<red5_hostname>/protectedVOD/<baseUrl>/<signature>/<expires>/<streamName>**

The parts of this URL are as follows:

    * *baseURL* is determined based on the relative path of the
      video/audio content in the FileSystemStorage.

    * *signature* is calculated as follows:
      ``hmac.new(shared_secret + baseUrl + streamName + client ip + expires).hexdigest()``
      where shared_secret is specified in Plone's configuration and
      should match the value on the red5 server.

    * *expires* is a timestamp given as a hex string. This is the number
      of seconds since January 1, 1970, 00:00:00 in hexadecimal
      notation plus the the ttl configured in Plone portal_properties.

    * *streamName* is the name of the video file, for example,
      Extremists.flv, flowplayer.flv, or rocknroll.mp4.


Red5 application
================

This package includes the corresponding Red5 application
*protectedVOD* as WAR-archive (also a tgz-Archive of the java sources;
s. README.txt in ``red5-wabapp`` directory of this product for further
information). Don't forget to change/synchronize the shared secret in
both Plone's and Red5's configuration!


Requisites
==========

  * Support for symbolic links for the used file system
  * FileSystemStorage (iw.fss_)
  * Red5 server (v0.8.x)
  

Credits
=======
  
  - Andreas Gabriel <gabriel _at_ hrz.uni-marburg.de>
  - David Nax       <naxd _at_ hrz.uni-marburg.de> 


TODO
====

  * clustering implementation
  * collective.flowplayer integration
