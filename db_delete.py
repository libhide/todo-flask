import os
import shutil

try:
  os.remove(os.path.join(os.getcwd(),'app.db'))
  shutil.rmtree('/db_repository')
except Exception as e:
  print '================================================================'
  print 'Looks like you have already removed the database.' 