from zope.interface import Interface
from zope.formlib import form
from Products.Five.formlib import formbase
from unimr.red5.protectedvod.content.migrator import migrateRed5Streams
from Products.statusmessages.interfaces import IStatusMessage


class IMigrateBlobsSchema(Interface):
    pass


class MigrateBlobs(formbase.PageForm):
    form_fields = form.FormFields(IMigrateBlobsSchema)
    label = u'Blobs Migration'
    description = u''

    @form.action('Migrate Red5Stream')
    def actionMigrate(self, action, data):
        output = migrateRed5Streams(self.context)
        IStatusMessage(self.request).addStatusMessage(output, type='info')
        return self.request.response.redirect(self.context.absolute_url())

    @form.action('Cancel')
    def actionCancel(self, action, data):
        return self.request.response.redirect(self.context.absolute_url())
