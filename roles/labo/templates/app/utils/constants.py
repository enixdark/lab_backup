class Constant:

    class Command:
        CP = 'cp -r %s %s' 
        MONGODUMP = 'mongodump'
        RSYNC = 'rrsync.sh %s %s %s %s' #'rsync -vazCog --chown=%s:%s --exclude=".*" %s %s'
        LVM = None

    class Mode:
        CP = 'cp'
        MONGO = 'mongo'
        LVM = 'lvm'
        S3 = 's3'
