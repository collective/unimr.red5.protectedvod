from plone.app.blob.migrations import migrate
from plone.app.blob.migrations import ATFileToBlobMigrator
from plone.app.blob.migrations import getMigrationWalker

class Red5StreamFSSToBlobMigrator(ATFileToBlobMigrator):
    src_portal_type = 'Red5Stream'
    src_meta_type = 'Red5Stream'
    dst_portal_type = 'Red5Stream'
    dst_meta_type = 'Red5Stream'

    
def getRed5StreamsMigrationWalker(self):
    return getMigrationWalker(self, migrator=Red5StreamFSSToBlobMigrator)

def migrateRed5Streams(context):
    return migrate(context, walker=getRed5StreamsMigrationWalker)
