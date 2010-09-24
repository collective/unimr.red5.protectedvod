#  Red5Stream http://www.uni-marburg.de/hrz
#  Protected streaming via plone & red5
#  Copyright (c) 2009 Andreas Gabriel <gabriel@hrz.uni-marburg.de>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


from logging import getLogger
from zope.interface import implements

from ZODB.POSException import ConflictError

from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.content.file import ATFile
from Products.ATContentTypes.content.file import ATFileSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import registerATCT

try:
    from iw.fss.FileSystemStorage import FileSystemStorage
    HAS_FSS = True
except ImportError:
    HAS_FSS = False

from unimr.red5.protectedvod.interface import IRed5Stream
from unimr.red5.protectedvod.permissions import DownloadRed5Stream
from unimr.red5.protectedvod.config import PROJECTNAME

Red5StreamSchema = ATFileSchema.copy()

file_field = Red5StreamSchema['file']
file_field.read_permission = DownloadRed5Stream

if HAS_FSS:
    file_field.storage = FileSystemStorage()
    file_field.registerLayer('storage', file_field.storage)

finalizeATCTSchema(Red5StreamSchema)


class Red5Stream(ATFile):

    implements(IRed5Stream)
    portal_type    = 'Red5Stream'
    archetype_name = 'Red5Stream'
    inlineMimetypes= tuple()

    schema = Red5StreamSchema

    security       = ClassSecurityInfo()


    security.declareProtected(DownloadRed5Stream, 'index_html')
    security.declareProtected(DownloadRed5Stream, 'download')

    security.declarePrivate('getIndexValue')
    def getIndexValue(self, mimetype='text/plain'):
        """ an accessor method used for indexing the field's value
            XXX: the implementation is mostly based on archetype's
            `FileField.getIndexable` and rather naive as all data gets
            loaded into memory if a suitable transform was found.
            this should probably use `plone.transforms` in the future """
        field = self.getPrimaryField()
        source = field.getContentType(self)
        transforms = getToolByName(self, 'portal_transforms')
        if transforms._findPath(source, mimetype) is None:
            return ''
        value = str(field.get(self))
        filename = field.getFilename(self)
        try:
            return str(transforms.convertTo(mimetype, value,
                mimetype=source, filename=filename))
        except (ConflictError, KeyboardInterrupt):
            raise
        except:
            getLogger(__name__).exception('exception while trying to convert '
               'blob contents to "text/plain" for %r', self)





registerATCT(Red5Stream, PROJECTNAME)
    
