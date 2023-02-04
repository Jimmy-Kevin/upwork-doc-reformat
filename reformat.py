# Python3 program to convert string
# from camel case to snake case

def change_case(str):
    res = [str[0].lower()]
    for c in str[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            res.append('_')
            res.append(c.lower())
        else:
            res.append(c)
    newstr = ''.join(res)
    #if newstr!=str:
        #print("%s ==> %s" % (str, newstr))
    return newstr
    
# Driver code
#str = "GeeksForGeeks"
#print(change_case(str))

def convert_tree_case(tree):
    if type(tree) == type({}):
        #print("convert dict")
        result = {}
        for k in tree.keys():
            newk = change_case(k)
            result[newk] = convert_tree_case(tree[k])
        return result
    if type(tree) == type([]):
        #print("convert list")
        result = []
        for value in tree:
             result.append(convert_tree_case(value))
        return result
    #print("raw value no need covert")
    return tree
    
import json

a = json.loads(open("./dash_live.json", "r").read())
b = convert_tree_case(a)
del b["header"]

print(json.dumps(b, indent=2))
