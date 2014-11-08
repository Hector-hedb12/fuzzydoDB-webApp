from django.shortcuts import render
from fuzzyapp.pokemonModel import Pokemon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

def index(request):
  db_list = ['pokemon'] # Deberia ser el resultado de una consulta a BD
  context = {'db_list': db_list}
  return render(request, 'fuzzyapp/index.html', context)

def db_information(request, db_name):
  # Se deberia consultar a postgres, por ejemplo, a una tabla con 
  # las BDs disponibles y si no esta: raise Http404
  if db_name == 'pokemon':
    object_list = list( Pokemon.objects.all() )
  else: raise Http404
  
  paginator = Paginator(object_list, 20)
  page = request.GET.get('page')
  
  try: 
    object_sublist = paginator.page(page)
  except PageNotAnInteger:
    object_sublist = paginator.page(1)
  except EmptyPage:
    object_sublist = paginator.page(paginator.num_pages)
    
  return render(request, 'fuzzyapp/db_information.html', {'db_name'     : db_name, 
                                                          'object_sublist':object_sublist})