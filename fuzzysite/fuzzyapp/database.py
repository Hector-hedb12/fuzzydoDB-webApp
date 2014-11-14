# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# El cliente de base de datos esta hecho en Java, y se usa en Python a traves   #
# de la libreria Py4j. Este modulo provee una interfaz mas pythonic sobre       #
# ese cliente.                                                                  #
# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

import re
from django.conf import settings

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
#                     API para consultar la base de datos                       #
# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def fuzzyStatement(statement):
  """
  Ejecuta directamente la consulta statement en la base de datos,
  sin prestarle tomar en cuenta el resultado.
  """
  return settings.FUZZYDB.execute(statement)

def fuzzyQuery(query, columns={}):
  res = settings.FUZZYDB.execute(query).result
  while res.next():
    # Build row
    yield { cname: res.getString(cname) for cname in columns }
