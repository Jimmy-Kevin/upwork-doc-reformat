from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToJson
import requests
import time
import json

# YOU CAN MODIFY THE PARAMETERS BELOW TO CHANGE HOW THE SCRIPTS BEHAVES

# The URL to our proto buffer GTFS data.
# You can change this to any other URL, as long as that URL returns
# a protocol buffer file format GTFS data.
gtfs_url = 'https://realtime.prod.dash.obaweb.org/agency/71/vehiclePositions'

# File path and file name of the output file.
# For example, this could be: '../some_other_folder/output.json'
filepath = './dash_live.json' 


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

while True:
    # Fetch GTFS data from the URL and parse it into a FeedMessage object.
    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        print("[LOG] Requesting")
        response = requests.get(gtfs_url, timeout=4)  # you can change the response Timeout (in seconds)
        feed.ParseFromString(response.content)

        # Convert GTFS data to JSON file format.
        json_obj = MessageToJson(feed)
        new_obj = convert_tree_case(json.loads(json_obj))
        del new_obj["header"]

        #Write GTFS data to a file.
        with open(filepath, 'w') as f:
            print("[LOG] Writing GTFS data")
            f.write(json.dumps(new_obj, indent=2))
    except requests.exceptions.Timeout:
        print("[LOG] Timeout exception")
        time.sleep(15)

    except requests.RequestException:
        print("[LOG] Ambiguous exception that occurred while handling your request")

    except BaseException as error:
        print('[LOG] An exception occurred: {}'.format(error))

    time.sleep(5)


