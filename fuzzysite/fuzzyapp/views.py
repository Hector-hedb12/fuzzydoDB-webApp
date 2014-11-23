from django.shortcuts import render
from fuzzyapp.pokemonModel import Pokemon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from fuzzyapp.managequery import Querym


def index(request):
  db_list = ['pokemon'] # Deberia ser el resultado de una consulta a BD
  context = {'db_list': db_list}
  
  return render(request, 'fuzzyapp/index.html', context)

def about(request):

  context = {}
  
  return render(request, 'fuzzyapp/about.html', context)

def db_information(request, db_name):
  # Se deberia consultar a postgres, por ejemplo, a una tabla con 
  # las BDs disponibles y si no esta: raise Http404
  
  page = request.GET.get('page')
  query = request.GET.get('query')
  
  
  
  if db_name == 'pokemon':
    att_name = Pokemon.att_name
    att_list = Pokemon.att_list
    att_type = Pokemon.att_type
    
    table_names = Pokemon.table_names
    
    listsn0 = Pokemon.listsn0
    idn0 = Pokemon.idn0
    att_esp = Pokemon.att_esp
    
    
    querystr = Querym().getq(query, att_name, att_type, att_esp)
    object_list = list( Pokemon.objects.allq(querystr) )
  else: raise Http404
  
  paginator = Paginator(object_list, 15)
  
  
  try: 
    object_sublist = paginator.page(page)
  except PageNotAnInteger:
    object_sublist = paginator.page(1)
    page = 1
  except EmptyPage:
    object_sublist = paginator.page(paginator.num_pages)
    page = paginator.num_pages
  
  
  
 
  
  context = {'db_name'     : db_name, 
             'object_sublist':object_sublist,
             'att_list': zip(att_list, att_type),
             'starting_list':zip([2,3,5], table_names, listsn0),
             'page':page,
             'query':query,
             'querystr':querystr
             }
  
  return render(request, 'fuzzyapp/db_query.html', context)


def db_info(request, db_name):
  # Se deberia consultar a postgres, por ejemplo, a una tabla con 
  # las BDs disponibles y si no esta: raise Http404
  
  page = request.GET.get('page')
  query = request.GET.get('query')
  
  
  
  if db_name == 'pokemon':
    att_name = Pokemon.att_name
    att_list = Pokemon.att_list
    att_type = Pokemon.att_type
    
    table_names = Pokemon.table_names
    
    listsn0 = Pokemon.listsn0
    idn0 = Pokemon.idn0
    att_esp = Pokemon.att_esp
    
    
    querystr = Querym().getq(query, att_name, att_type, att_esp)
    
  else: raise Http404
  
  
  context = {'db_name'     : db_name, 
             'att_list': zip(att_list, att_type),
             'starting_list':zip([2,3,5], table_names, listsn0)
             }
  
  return render(request, 'fuzzyapp/db_info.html', context)

