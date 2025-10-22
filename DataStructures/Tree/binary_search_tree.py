import datetime
from DataStructures.Tree import bst_node as node
from DataStructures.List import single_linked_list as sl
from DataStructures.List import array_list as lt

def new_map():
    return {"root":None}

def put(my_bst, key, value):
    
    my_bst["root"]=insert_node(my_bst["root"], key, value)
    
    return my_bst


def insert_node(root, key, value):
    if root is None:
        return node.new_node(key, value)

    if key == node.get_key(root):
        root["value"] = value

    elif key < node.get_key(root):
        root["left"] = insert_node(root["left"], key, value)

    else:
        root["right"] = insert_node(root["right"], key, value)
        
    left_size = root["left"]["size"] if root["left"] else 0
    right_size = root["right"]["size"] if root["right"] else 0
    root["size"] = 1 + left_size + right_size

    return root

def get(my_bst, key):
    res=get_node(my_bst["root"], key)
    if res is None:
        return None
    else:
        return res["value"]


def get_node(root, key):
    if root is None:
        return None
    
    if key == node.get_key(root):
        return root

    elif key < node.get_key(root):
        return get_node(root["left"], key)

    else:
        return get_node(root["right"], key)

def size(my_bst):
    if my_bst["root"] is None:
        return 0
    else :
        return my_bst["root"]["size"]
    
def remove(my_bst, key):
    my_bst["root"] = remove_node(my_bst["root"], key)
    return my_bst

def remove_node(root, key):
    if root is None:
        return None
    if key < root["key"]:
        root["left"] = remove_node(root["left"], key)
    elif key > root["key"]:
        root["right"] = remove_node(root["right"], key)
    else:
        if root["left"] is None:
            return root["right"]
        if root["right"] is None:
            return root["left"]
        temp = get_min_node(root["right"])
        root["key"], root["value"] = temp["key"], temp["value"]
        root["right"] = delete_min_tree(root["right"])
    return root

    
def contains(my_bst,key):
    res=get(my_bst,key)
    if res is None:
        return False
    return True

def is_empty(my_bst):
    if my_bst["root"] is None:
        return True
    return False

def key_set(my_bst):
    """
    Retorna una lista con todas las llaves del árbol binario de búsqueda.
    """
    lista = sl.new_list()             
    root = my_bst["root"]             
    key_set_tree(root, lista)         
    return lista                      


def key_set_tree(node, lista):
    """
    Recorre el árbol en orden (in-order) y agrega las llaves a la lista.
    """
    if node is not None:
        key_set_tree(node["left"], lista)        
        sl.add_last(lista, node["key"])         
        key_set_tree(node["right"], lista)     
        
def value_set(my_bst):
    values = sl.new_list()
    value_set_tree(my_bst["root"], values)
    return values

def value_set_tree(node, values):
    if node is not None:
        value_set_tree(node["left"], values)
        sl.add_last(values, node["value"])
        value_set_tree(node["right"], values)
        
def get_min(my_bst):
    if my_bst["root"] is None:
        return None
    return get_min_node(my_bst["root"])

def get_min_node(root):
    if root is None:
        return None
    if root["left"] is None:
        return root["key"]
    return get_min_node(root["left"])

def get_max(my_bst):
    if my_bst["root"] is None:
        return None
    return get_max_node(my_bst["root"])

def get_max_node(root):
    if root is None:
        return None
    if root["right"] is None:
        return root["key"]
    return get_max_node(root["right"])



def delete_min(my_bst):
    my_bst["root"] = delete_min_tree(my_bst["root"])
    return my_bst

def delete_min_tree(root):
    if root is None:
        return None
    if root["left"] is None:
        return root["right"]
    root["left"] = delete_min_tree(root["left"])
    return root

def delete_max(my_bst):
    my_bst["root"] = delete_max_tree(my_bst["root"])
    return my_bst

def delete_max_tree(root):
    if root is None:
        return None
    if root["right"] is None:
        return root["left"]
    root["right"] = delete_max_tree(root["right"])
    return root

def height(my_bst):
    return height_tree(my_bst["root"])

def height_tree(root):
    if root is None:
        return 0
    return 1 + max(height_tree(root["left"]), height_tree(root["right"]))

def keys(my_bst, key_initial, key_final):
    list_keys = sl.new_list()
    if my_bst["root"] is not None:
        keys_range(my_bst["root"], key_initial, key_final, list_keys)
    return list_keys

def keys_range(root, key_initial, key_final, list_key):
    if root is None:
        return
    if key_initial < root["key"]:
        keys_range(root["left"], key_initial, key_final, list_key)
    if key_initial <= root["key"] <= key_final:
        sl.add_last(list_key, root["key"])
    if key_final > root["key"]:
        keys_range(root["right"], key_initial, key_final, list_key)

def values(my_bst, key_initial, key_final):
    list_values = sl.new_list()
    values_range(my_bst["root"], key_initial, key_final, list_values)
    return list_values


def values_range(root, key_initial, key_final, list_values):
    if root is None:
        return list_values

    node_key = root["key"]

    if isinstance(node_key, datetime.datetime):
        node_key = node_key.date()
    if isinstance(key_initial, datetime.datetime):
        key_initial = key_initial.date()
    if isinstance(key_final, datetime.datetime):
        key_final = key_final.date()

    if key_initial < node_key:
        values_range(root["left"], key_initial, key_final, list_values)

    if key_initial <= node_key <= key_final:
        sl.add_last(list_values, root["value"])
        print(f"DBG_RANGE: key {node_key} in range [{key_initial}, {key_final}]")  # ✅

    if key_final > node_key:
        values_range(root["right"], key_initial, key_final, list_values)

    return list_values
