from django.db import models
from fuzzyapp.database import fuzzyQuery

# ### ### ### ### ### ### ### ### ### ### ### ### ###
#  Obtiene objetos Pokemon desde la base de datos   #
# ### ### ### ### ### ### ### ### ### ### ### ### ###
class PokemonQuerySet():
  
  def __init__(self):
    self.conditions = []
    self.order_columns = []
  
    """
    Agrega una condicion para filtrar los pokemones en la base de datos
    Cada argumento que se le pase representa una condicion.
    
    Condiciones soportadas:

    * <columna>__startswithany = <valores>: busca aquellos elementos cuya
        columna <columna> comience por algun string en <valores>
    * <columna>__exact = <valor>: aquellos elementos cuya columna <columna>
        sea exactamente igual a <valor>
    """
  def filter(self, **kwargs):
    for key, value in kwargs.items():
      # Va a explotar si pasan algo como a__b__c
      # Esto no es Django, a lo sumo soportamos algo como
      # <columna>__<operador>.
      
      column, operator = key.rsplit("__")
      
      if operator == "startswithany":
        condition_format = "(" + column + " LIKE '{value}%')"
        conditions = map( lambda x: condition_format.format(value=x),
                          value )
        
        self.conditions.append("(" + " OR ".join(conditions) + ")")
      
      elif operator == "exact":
        self.conditions.append("({column} = '{value}')".format( column=column,
                                                                value=value
                                                                )
                              )
      else:
        raise NotImplementedError( "Can't filter using operator {op}".format(op=operator) )
      
    return self
  
  """
  Filtra por aquellos pokemones que se relacionen con una unidad
  con id en 'ids'.
  """
  #def id_unidad_in(self, ids):
    #condition_format = "(ua.id_unidad = {value})"
    #conditions = map( lambda x: condition_format.format(value=x),
                      #ids
                    #)
    #self.conditions.append("(" + " OR ".join(conditions) + ")")
  
  """ Recibe una secuencia de columnas sobre las cuales ordenar el resultado """
  def order_by(self, column, direction='DESC'):
    self.order_columns += ((column, direction), )
    return self
  
  """ Construye la sentencia SQL necesaria para buscar todos los elementos """
  def _get_sql_query(self):
    sql = ( "SELECT * FROM pokemon")
    # Agregar condiciones WHERE, si las hay
    if len(self.conditions) > 0:
      sql += " WHERE "
      sql += " AND ".join(self.conditions)
    
    # Agregar ORDER BY, si hace falta
    if len(self.order_columns) > 0:
      sql += " ORDER BY "
      sql += ','.join(map(lambda (col, dir): col + " " + dir, self.order_columns))
    
    query_columns = ["codigo", "nombre","tipo_1","tipo_2", "gh_1", "gh_2",
                     "poder_human_readable", "region", "ratio_human_readable",
                     "color", "color_percibido_human_readable"]
    
    return sql, query_columns

    """
    Devuelve un generador que ejecuta la consulta del QuerySet y
    genera las instancias de Materia correspondientes al resultado.
    """
  def __iter__(self):
    sql, query_columns = self._get_sql_query()
    #result = []
    for row in fuzzyQuery(sql, query_columns):
      pokemon = Pokemon( codigo          = row["codigo"],
                         nombre          = row["nombre"],
                         tipo_1          = row["tipo_1"],
                         tipo_2          = row["tipo_2"],
                         gh_1            = row["gh_1"],
                         gh_2            = row["gh_2"],
                         poder           = row["poder_human_readable"],
                         region          = row["region"],
                         ratio           = row["ratio_human_readable"],
                         color           = row["color"],
                         color_percibido = row["color_percibido_human_readable"]
                        )
      #pokemon._update_on_save = True
      #print result
      #result.append(pokemon)
      yield pokemon
    #return result

# ### ### ### ### ### ### ### ### ### ### ### ### ###
#                                                   #
# ### ### ### ### ### ### ### ### ### ### ### ### ###
class PokemonManager():
    """ Devuelve un QuerySet que hace match con todos los pokemones """
    def all(self):
        return PokemonQuerySet()
    
    """ Devuelve un QuerySet con todos los pokemones, filtrando segun kwargs"""
    def get(self, **kwargs):
        return PokemonQuerySet().filter(**kwargs)

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
#                                                                                                                       #
#    COLUMNA          |                            DESCRIPCION                             |  TIPO                      #
#    -------------------------------------------------------------------------------------------------------------      #
#  * codigo:          |  numero del pokemon desde el punto de vista de la pokedex nacional | varchar pk                 #
#  * nombre:          |  nombre del pokemon                                                | varchar                    #
#  * tipo_1:          |  tipo primario del pokemon                                         | tipos_pokemon              # 
#  * tipo_2:          |  tipo secundario del pokemon                                       | tipos_pokemon              #
#  * gh_1:            |  grupo en el que el pokemon puede tener crias                      | grupos_huevo_pokemon       #
#  * gh_2:            |  grupo en el que el pokemon puede tener crias                      | grupos_huevo_pokemon       #
#  * poder:           |  poder estimado que puede tener un pokemon                         | poderes_base_pokemon       #
#  * region:          |  generacion en la cual aparecio por primera vez el pokemon         | varchar                    #
#  * ratio:           |  que tan facil/dificil es el pokemon de capturar                   | ratios_de_captura_pokemon  #
#  * color:           |  color primario por el que esta clasificado el pokemon             | colores_pokemon            #
#  * color_percibido: |  colores del pokemon                                               | multicolores_pokemon       #
#                                                                                                                       #
# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

class Pokemon(object):
  
  objects = PokemonManager()
  
  def __init__(self, codigo, nombre, tipo_1, tipo_2, 
               gh_1, gh_2, poder, region, ratio, 
               color, color_percibido):
    self.codigo          = codigo
    self.nombre          = nombre
    self.tipo_1          = tipo_1
    self.tipo_2          = tipo_2
    self.gh_1            = gh_1
    self.gh_2            = gh_2
    self.poder           = poder
    self.region          = region
    self.ratio           = ratio
    self.color           = color
    self.color_percibido = color_percibido
    
    self._update_on_save = False
  
  def save(self):
    if self._update_on_save:
      raise NotImplementedError( "Update: No implemented Yet" )
    else:
      self._update_on_save = True
      raise NotImplementedError( "Insert: No implemented Yet" )
  
  def __str__(self):
    return '{nombre=' + self.nombre + '}'
