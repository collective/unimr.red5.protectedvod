## Script (Python) "at_download"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Download a file keeping the original uploaded filename
##

# fix for Archetype's field download, which does not check the
# read permission

from AccessControl import Unauthorized

if traverse_subpath:
    field = context.getWrappedField(traverse_subpath[0])
else:
    field = context.getPrimaryField()

if field.checkPermission('r',context):
   return field.download(context)

raise Unauthorized
