from datetime import datetime
from .arrow import *
import json
import re

def conv_to_str(value):
    if isinstance(value, datetime):
        return get(value).format("MMMM D, YYYY")
    else:
        return str(value)


def isfloat(value):
    if value is None:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def first(lst):
    return next((x for x in lst if x), None)


def dget(d, dkey, default=None):
    """Dictionary get: gets the field from nested key

    Args:
        d (dict, list): Dictionary/list to retrieve field from
        dkey (str): Nested key to retrive field from dictionary/list separated 
            by periods. Example: key1.3.key2, this will be the equivalent of 
            d['key1'][3]['key2'].
        default (optional): Default object to return if value not found. 
            Defaults to None.

    Returns:
        Any: field to return from dict or default if not found.
    """
    keys = dkey.split('.')
    obj = d

    for key in keys:
        if not obj:
            return default
        if key.isdigit():
            index = int(key)
            if isinstance(obj, list) and index < len(obj):
                obj = obj[index]
            else:
                return default
        else:
            if isinstance(obj, dict) and key in obj:
                obj = obj[key]
            else:
                return default
    return obj

def getSuggestions(search) :
    """
    
    
    Returns:
        All suggestions containing the couple (label,description) for each item in the array
    """
    suggestions = []
    
    for result in search :
        label = dget(result, "label")
        desc = dget(result, "description")
        suggestions.append((label,desc))
        
    return suggestions


def confirmMatches(search, txt) :
    isResultMatch = []
    for result in search :
        match = dget(result,"match")
        txtMatch = dget(match, "text")
        
        if txtMatch.lower() == txt.lower():
            isResultMatch.append(True)
        else :
            isResultMatch.append(False)
            
    return isResultMatch

# Param : fichier json
# Return : convertit le fichier json en dictionnaire python
def parseJson(jsonFileName):
    jsonFile = open(jsonFileName,"r")
    jsonStr = jsonFile.read()
    return json.loads(jsonStr)

# Param fileName : fichier du dataset à charger
# Return dataset : dictionnaire contenant les queries
def loadDataset(fileName):
    dataset = dict()
    if fileName == "dataset/annotated_wd_data_train.txt":
        file = open(fileName,'r',encoding="utf8")
        i = 0
        for line in file:
            dataset[i] = re.split(r'[\n\t]+', line)
            i += 1
    elif fileName == "dataset/qald-7-test-en-wikidata-withoutanswers.json":
        file = parseJson(fileName)
        j = 0
        for key,item in file.items():
            if key == "questions":
                for i in item:
                    dataset[j] = i["question"][0]["string"]
                    j += 1
    else:
        print("fileName not implemented")
        return None
    return dataset
        