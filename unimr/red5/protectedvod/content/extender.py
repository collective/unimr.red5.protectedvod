from zope.component import adapts
from zope.interface import implements

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from plone.app.blob.field import BlobField

from Products.CMFPlone import PloneMessageFactory as _
from Products.validation import V_REQUIRED

from Products.Archetypes.atapi import FileWidget
from Products.Archetypes.atapi import AnnotationStorage

from unimr.red5.protectedvod.interface import IRed5Stream
from unimr.red5.protectedvod.permissions import DownloadRed5Stream

class ExtensionBlobField(ExtensionField, BlobField):
    """ derivative of blobfield for extending schemas """

    def set(self, instance, value, **kwargs):
        super(ExtensionBlobField, self).set(instance, value, **kwargs)
        self.fixAutoId(instance)


class Red5StreamExtender(object):
    adapts(IRed5Stream)
    implements(ISchemaExtender)

    fields = [
        ExtensionBlobField('file',
            required = True,
            primary = True,
            searchable = True,
            default = '',
            read_permission = DownloadRed5Stream,               
            index_method = 'getIndexValue',
            languageIndependent = True,
            storage = AnnotationStorage(migrate=True),
            validators = (('isNonEmptyFile', V_REQUIRED),
                          ('checkFileMaxSize', V_REQUIRED)),
            widget = FileWidget(label = _(u'label_file', default=u'File'),
                                description=_(u''),
                                show_content_type = False,))

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
