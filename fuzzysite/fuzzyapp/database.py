# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# El cliente de base de datos esta hecho en Java, y se usa en Python a traves   #
# de la libreria Py4j. Este modulo provee una interfaz mas pythonic sobre       #
# ese cliente.                                                                  #
# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

import re
from django.conf import settings

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
#                   Clases para representar tipos difusos                       #
# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

class FuzzyValue(object):
  """ 
  Representa un valor difuso.
  Hace referencia a la existencia del concepto 'FuzzyValue'
  """
  pass

class FuzzyExtension(FuzzyValue):
  """
  Tipo difuso por extension.
  * Sus campos:  values -- lista de tuplas de la forma (posibilidad, valor)
  """
  
  def __init__(self, values):
    self.values = values
  
  def __str__(self):
    return str(list(self.values))
  
  def __unicode__(self):
    str_vals = map(lambda (p, v): "{:.2f}/{}".format(p, v), filter(lambda (p, v): p > 0, self.values))
    str_vals = ', '.join(str_vals)
    
    return "{{f {} }}".format(str_vals)

class FuzzyTrapezoid(FuzzyValue):
  """
  Tipo difuso en forma de trapecio. Puede ser degenerado.
  
  * Sus campos son:
                    values -- lista de tuplas de la forma (posibilidad, valor)
                    x1, x2, x3, x4 -- puntos del trapecio. Pueden ser None.
                    
    Si x1 y x2 son None, es un trapecio degenerado
    Si x3 y x4 son None, es un trapecio degenerado
    
    No puede ocurrir que todos los valores sean None. Si hay valores None,
    es porque el trapecio es exactamente uno de los dos casos de trapecio
    degenerado.
    """  
  def __init__(self, values):
    self.values = values
    self.x1 = values[0][1]
    self.x2 = values[1][1]
    self.x3 = values[2][1]
    self.x4 = values[3][1]
    
  def __str__(self):
    return str(list(self.values))
  
  def __unicode__(self):
    return str(list(self.values))

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
  """
  Ejecuta la consulta query en la base de datos y devuelve un generador
  cuyos elementos son diccionarios que representan las filas del
  resultado.
  Para construir estos diccionarios se utiliza la definicion que se
  pasa via el parametro columns.
  
  El formato de columns es el siguiente:
    {
    ...
    "<nombre_de_columna>": {
    "type": "<tipo de conversion>",
    "subtype_converter": <funcion de conversion para subtipo>
              (este ultimo solo es valido cuando se trata de un tipo difuso)
              }
    ...
    }

    Los valores validos para <tipo de conversion> son los siguientes:
    * integer
    * string
    * boolean
    * fuzzy
    * default (hace toString() de la columna devuelta por el driver JDBC)

    Ejemplo de uso del API:

    Dado el tipo difuso: CREATE FUZZY DOMAIN fuzzyint AS POSSIBILITY DISTRIBUTION ON INTEGER
    Y la tabla:          CREATE TABLE personas (nombre text, apellido text, edad fuzzyint, sueldo int)
    
    Entonces se puede consultar de la siguiente forma:
    result_columns = {
        "nombre":   {"type": "string", },
        "apellido": {"type": "string", },
        "edad":     {"type": "fuzzy", "subtype_converter": int},
        "sueldo":   {"type": "integer", }
    }
    
    result = list(fuzzyQuery("SELECT * FROM personas", columns=result_columns))
    """
  res = settings.FUZZYDB.execute(query).result
  while res.next():
    # Build row
    yield { cname: fetch_column(res, cname, **params) for cname, params in columns.items() }
    
def fetch_column(result_set, cname, type, **kwargs):
  """
  Recibe un ResultSet (de Java JDBC), un nombre de columna, un tipo
  de conversion; y procede a extraerla, convertirla y devolverla como
  un tipo de Python.
  """
  conversion = c_conversions.get(type, 
                                 lambda x, y, **kwargs: x.getObject(y).toString() )
  return conversion(result_set, cname, **kwargs)

# Diccionario que guarda las conversiones disponibles
c_conversions = {
  "integer" : lambda x, y, **kwargs: x.getInt(y),
  "string"  : lambda x, y, **kwargs: x.getString(y),
  "boolean" : lambda x, y, **kwargs: x.getBoolean(y),
  "fuzzy"   : lambda x, y, **kwargs: convert_fuzzy(x.getObject(y).toString(), **kwargs), # NOQA
  "array"   : lambda x, y, **kwargs: convert_array(x.getArray(y), **kwargs),
  "default" : lambda x, y, **kwargs: x.getObject(y).toString(),
}

def convert_array(array_obj, subtype_converter):
  res = array_obj.getResultSet()
  result = []
  while res.next():
    result.append(subtype_converter(res.getObject(2)))
  
  return result

def convert_fuzzy(string, subtype_converter):
  """
  Toma un string proveniente de la representacion default de PostgreSQL
  para un valor difuso, y lo convierte en una instancia de FuzzyValue
  apropiada, convirtiendo el subtipo del dominio difuso mediante la
  funcion subtype_converter.

  El formato que envia PostgreSQL es el siguiente, en formato mas o menos
  backus-naur:
  DIFUSO -> ( { POSIBILIDAD+ }, { VALOR+ } , TIPO )
  POSIBILIDAD -> "<literal numero flotante>"
  VALOR -> "<representacion en string del tipo subyacente>"
  TIPO -> t | f  (si es trapecio o extension)
  """
  
  # Eliminar los parentesis
  string = string[1:-1]
  match = re.match("\"\{(.*)\}\",\"\{(.*)\}\",(t|f)", string)

  odd, value, type = match.groups()
  type = True if type == "t" else False

  odd = map(float, odd.rsplit(","))
  value = map(
    lambda x: subtype_converter(x) if x != "NULL" else None,
    value.rsplit(",")
  )

  if type:
    return FuzzyExtension(zip(odd, value))
  else:
    return FuzzyTrapezoid(zip(odd, value))