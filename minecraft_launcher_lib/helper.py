import platform
import zipfile
import hashlib
import json
import os

def parseSingeRule(rule,options):
    #Parse a rule from the versions.json
    if rule["action"] == "allow":
        returnvalue = False
    elif rule["action"] == "disallow":
        returnvalue = True
    if "os" in rule:
        for key, value in rule["os"].items():
            if key == "name":
                if value == "windows" and platform.system() != 'Windows':
                    return returnvalue
                elif value == "osx" and platform.system() != 'Darwin':
                    return returnvalue
                elif value == "linux" and platform.system() != 'Linux':
                    return returnvalue
            elif key == "arch":
                if value == "x86" and platform.architecture()[0] != "32bit":
                    return returnvalue
    if "features" in rule:
        for key, value in rule["features"].items():
            if key == "has_custom_resolution" and not options.get("customResolution",False):
                return returnvalue
            elif key == "is_demo_user" and not options.get("demo",False):
                return returnvalue
    return not returnvalue

def parseRuleList(data,ruleString,options):
    #Parse a rule list
    if not ruleString in data:
        return True
    for i in data[ruleString]:
        if not parseSingeRule(i,options):
            return False
    return True


def inherit_json(original_data,path):
    #See https://github.com/tomsik68/mclauncher-api/wiki/Version-Inheritance-&-Forge
    inherit_version = original_data["inheritsFrom"]
    with open(os.path.join(path,"versions",inherit_version,inherit_version + ".json")) as f:
        new_data = json.load(f)
    for key, value in original_data.items():
        if isinstance(value,list) and isinstance(new_data.get(key,None),list):
            new_data[key] = value + new_data[key]
        elif isinstance(value,dict) and isinstance(new_data.get(key,None),dict):
            for a, b in value.items():
                if isinstance(b,list):
                    new_data[key][a] = new_data[key][a] + b
        else:
            new_data[key] = value
    return new_data

#Returns the path from a libname
def get_library_path(name,path):
    libpath = os.path.join(path,"libraries")
    base_path, libname, version = name.split(":")
    for i in base_path.split("."):
        libpath = os.path.join(libpath,i)
    try:
        version,fileend = version.split("@")
    except:
        fileend = "jar"
    libpath = os.path.join(libpath,libname,version,libname + "-" + version + "." + fileend)
    return libpath

#Returns the mainclass of a given jar
def get_jar_mainclass(path):
    zf = zipfile.ZipFile(path)
    #Parse the MANIFEST.MF
    with zf.open("META-INF/MANIFEST.MF") as f:
        lines = f.read().decode("utf-8").splitlines()
    zf.close()
    content = {}
    for i in lines:
        try:
            key, value = i.split(":")
            content[key] = value[1:]
        except:
            pass
    return content["Main-Class"]

#Returns the sha1 hash of the given file
def get_sha1_hash(path):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()
