echo -n "Copying private files ..."
scp settings_local.py webme@184.106.152.183:/web/bfun/releases/current/bfun/
scp private_remote.sh webme@184.106.152.183:/web/bfun/releases/current/bfun/
echo "Dumping and sending data"
python manage.py dumpdata > data/data.bfun.json
scp -r data/*.json webme@184.106.152.183:/web/bfun/releases/current/bfun/data
scp -r media_rsc/uploads webme@184.106.152.183:/web/bfun/releases/current/bfun/media_rsc/
