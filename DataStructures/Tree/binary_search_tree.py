from DataStructures.Tree import bst_node as node

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