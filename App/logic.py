"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones
 *
 * Dario Correal
 """

import os
import csv
import datetime
from DataStructures.Tree import binary_search_tree as bst

# TODO Realice la importación del Árbol Binario Ordenado
# TODO Realice la importación de ArrayList (al) como estructura de datos auxiliar para sus requerimientos
# TODO Realice la importación de LinearProbing (lp) como estructura de datos auxiliar para sus requerimientos
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp


data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'



def new_logic():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'crimes': None,
                'dateIndex': None
                }

    analyzer['crimes'] = al.new_list()
    # TODO completar la creación del mapa ordenado
    analyzer['dateIndex'] = bst.new_map()
    
    return analyzer

# Funciones para realizar la carga

def load_data(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for crime in input_file:
        add_crime(analyzer, crime)
    return analyzer



# Funciones para agregar informacion al analizador


def add_crime(analyzer, crime):
    """
    funcion que agrega un crimen al catalogo
    """
    al.add_last(analyzer['crimes'], crime)
    update_date_index(analyzer['dateIndex'], crime)
    return analyzer


def update_date_index(map, crime):
    occurreddate = crime['OCCURRED_ON_DATE']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S').date()
    entry = bst.get(map, crimedate)

    if entry is None:
        datentry = new_data_entry(crime)
    else:
        datentry = entry

    add_date_index(datentry, crime)
    bst.put(map, crimedate, datentry)

    return map


def add_date_index(datentry, crime):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstcrimes']
    al.add_last(lst, crime)

    offenseIndex = datentry['offenseIndex']
    offentry = lp.get(offenseIndex, crime['OFFENSE_CODE_GROUP'])

    if offentry is None:
        # Cas où le type de crime n’existe pas encore
        new_offense = new_offense_entry(crime['OFFENSE_CODE_GROUP'], crime)
        al.add_last(new_offense['lstoffenses'], crime)
        lp.put(offenseIndex, crime['OFFENSE_CODE_GROUP'], new_offense)
    else:
        # Cas où le type de crime existe déjà
        al.add_last(offentry['lstoffenses'], crime)

    return datentry



def new_data_entry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstcrimes': None}
    entry['offenseIndex'] = lp.new_map(num_elements=30,
                                        load_factor=0.5)
    entry['lstcrimes'] = al.new_list()
    return entry


def new_offense_entry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = al.new_list()
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def crimes_size(analyzer):
    """
    Número de crimenes
    """
    return al.size(analyzer['crimes'])


def index_height(analyzer):
    """
    Altura del arbol
    """
    # TODO Completar la función de consulta de altura del árbol
    return bst.height(analyzer['dateIndex'])


def index_size(analyzer):
    """
    Numero de elementos en el indice
    """
    # TODO Completar la función de consulta de tamaño del árbol
    return bst.size(analyzer['dateIndex'])


def min_key(analyzer):
    """
    Llave mas pequena
    """
    # TODO Completar la función de consulta de la llave mínima
    return bst.get_min(analyzer['dateIndex'])


def max_key(analyzer):
    """
    Llave mas grande
    """
    # TODO Completar la función de consulta de la llave máxima
    return bst.get_max(analyzer['dateIndex'])


def get_crimes_by_range(analyzer, initialDate, finalDate):
    if isinstance(initialDate, str):
        initialDate = datetime.datetime.strptime(initialDate, "%Y-%m-%d").date()
    if isinstance(finalDate, str):
        finalDate = datetime.datetime.strptime(finalDate, "%Y-%m-%d").date()

    lst = bst.values(analyzer['dateIndex'], initialDate, finalDate)

    if lst is None or 'first' not in lst:
        return 0

    total = 0
    node = lst["first"]
    while node is not None:
        entry = node["info"]
        if entry and "lstcrimes" in entry:
            total += al.size(entry["lstcrimes"])
        node = node["next"]


    return total





def get_crimes_by_range_code(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    crimedate = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
    entry = bst.get(analyzer['dateIndex'], crimedate)

    if entry is not None:
        offenseIndex = entry['offenseIndex']
        offentry = lp.get(offenseIndex, offensecode)
        if offentry is not None:
            return al.size(offentry['lstoffenses'])
    return 0
