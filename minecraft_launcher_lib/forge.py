from .install import download_file, install_minecraft_version, install_libraries
from .helper import get_library_path, get_jar_mainclass
from xml.dom import minidom
import subprocess
import platform
import requests
import tempfile
import zipfile
import random
import json
import os

def extract_file( handler, zip_path, extract_path):
    try:
        os.makedirs(os.path.dirname(extract_path))
    except:
        pass
    with handler.open(zip_path,"r") as f:
        with open(extract_path,"wb") as w:
            w.write(f.read())

def get_data_library_path(libname,path):
    #Remove the []
    libname = libname[1:-1]
    libpath = os.path.join(path,"libraries")
    base_path, libname, version, extra = libname.split(":")
    for i in base_path.split("."):
        libpath = os.path.join(libpath,i)
    try:
        extra,fileend = extra.split("@")
    except:
        fileend = "jar"
    libpath = os.path.join(libpath,libname,version,libname + "-" + version + "-" + extra + "." + fileend)
    return libpath

def forge_processors(data,path,lzma_path):
    argument_vars = {"{MINECRAFT_JAR}":os.path.join(path,"versions",data["minecraft"],data["minecraft"] + ".jar")}
    for key,value in data["data"].items():
        if value["client"].startswith("[") and value["client"].endswith("]"):
            argument_vars["{" + key + "}"] =  get_data_library_path(value["client"],path)
        else:
            argument_vars["{" + key + "}"] = value["client"]
    argument_vars["{BINPATCH}"] = lzma_path
    if platform.system() == "Windows":
        classpath_seperator = ";"
    else:
        classpath_seperator = ":"
    for i in data["processors"]:
        #Get the classpath
        classpath = ""
        for c in i["classpath"]:
            classpath = classpath + get_library_path(c,path) + classpath_seperator
        classpath = classpath + get_library_path(i["jar"],path)
        mainclass = get_jar_mainclass(get_library_path(i["jar"],path))
        command = ["java","-cp",classpath,mainclass]
        for c in i["args"]:
            var = argument_vars.get(c,c)
            if var.startswith("[") and var.endswith("]"):
                command.append(get_library_path(var[1:-1],path))
            else:
                command.append(var)
        subprocess.call(command)

def install_forge_version(versionid,path,callback=None):
    if callback == None:
        callback = {}
    FORGE_DOWNLOAD_URL = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
    temp_file_path = os.path.join(tempfile.gettempdir(),"forge-" + str(random.randrange(1,100000)) + ".tmp")
    download_file(FORGE_DOWNLOAD_URL.format(version=versionid),temp_file_path,callback)
    zf = zipfile.ZipFile(temp_file_path,"r")
    #Read the install_profile.json
    with zf.open("install_profile.json","r") as f:
        version_content = f.read()
    version_data = json.loads(version_content)
    forge_version_id = version_data["version"]
    #Make sure, the base version is installed
    install_minecraft_version(version_data["minecraft"],path,callback=callback)
    #Install all needed libs from install_profile.json
    install_libraries(version_data,path,callback)
    #Extract the version.json
    version_json_path = os.path.join(path,"versions",forge_version_id,forge_version_id + ".json")
    extract_file(zf,"version.json",version_json_path)
    #Extract forge libs from the installer
    forge_lib_path = os.path.join(path,"libraries","net","minecraftforge","forge",versionid)
    extract_file(zf,"maven/net/minecraftforge/forge/{version}/forge-{version}.jar".format(version=versionid),os.path.join(forge_lib_path,"forge-" + versionid + ".jar"))
    extract_file(zf,"maven/net/minecraftforge/forge/{version}/forge-{version}-universal.jar".format(version=versionid),os.path.join(forge_lib_path,"forge-" + versionid + "-universal.jar"))
    #Extract the client.lzma
    lzma_path = os.path.join(tempfile.gettempdir(),"lzma-" + str(random.randrange(1,100000)) + ".tmp")
    extract_file(zf,"data/client.lzma",lzma_path)
    zf.close()
    os.remove(temp_file_path)
    #Install the rst with the vanilla function
    install_minecraft_version(forge_version_id,path,callback=callback)
    #Run the processors
    forge_processors(version_data,path,lzma_path)
    os.remove(lzma_path)

def run_forge_installer(version):
    FORGE_DOWNLOAD_URL = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
    temp_file_path = os.path.join(tempfile.gettempdir(),"forge-" + str(random.randrange(1,100000)) + ".tmp")
    download_file(FORGE_DOWNLOAD_URL.format(version=version),temp_file_path,{})
    subprocess.call(["java","-jar",temp_file_path])
    os.remove(temp_file_path)

def list_forge_versions():
    MAVEN_METADATA_URL = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/maven-metadata.xml"
    r = requests.get(MAVEN_METADATA_URL).text
    xml_data = minidom.parseString(r)
    version_list = []
    for i in xml_data.getElementsByTagName("version"):
        version_list.append(i.childNodes[0].wholeText)
    return version_list

def find_forge_version(vanilla_version):
    version_list = list_forge_versions()
    version_list.reverse()
    for i in version_list:
        version_split= i.split("-")
        if version_split[0] == vanilla_version:
            return i
    return None
