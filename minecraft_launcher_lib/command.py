from .helper import parseRuleList, inherit_json
from .utils import get_library_version
from .natives import get_natives
import platform
import json
import copy
import os

def get_libraries(data,path):
    if platform.system() == "Windows":
        classpath_seperator = ";"
    else:
        classpath_seperator = ":"
    libstr = ""
    for i in data["libraries"]:
        if not parseRuleList(i,"rules",{}):
            continue
        currentPath = os.path.join(path,"libraries")
        libPath, name, version = i["name"].split(":")
        for l in libPath.split("."):
            currentPath = os.path.join(currentPath,l)
        currentPath = os.path.join(currentPath,name,version)
        native = get_natives(i)
        if native == "":
            jarFilename = name + "-" + version + ".jar"
        else:
            jarFilename = name + "-" + version + "-" + native + ".jar"
        currentPath = os.path.join(currentPath,jarFilename)
        libstr = libstr + currentPath + classpath_seperator
    if "jar" in data:
        libstr = libstr + os.path.join(path,"versions",data["jar"],data["jar"] + ".jar")
    else:
        libstr = libstr + os.path.join(path,"versions",data["id"],data["id"] + ".jar")
    return libstr

def replace_arguments(argstr,versionData,path,options):
    #Replace all arguments with the needed value
    argstr = argstr.replace("${natives_directory}",options["nativesDirectory"])
    argstr = argstr.replace("${launcher_name}",options.get("launcherName","minecraft-launcher-lib"))
    argstr = argstr.replace("${launcher_version}",options.get("launcherVersion",get_library_version()))
    argstr = argstr.replace("${classpath}",options["classpath"])
    argstr = argstr.replace("${auth_player_name}",options.get("username","{username}"))
    argstr = argstr.replace("${version_name}",versionData["id"])
    argstr = argstr.replace("${game_directory}",options.get("gameDirectory",path))
    argstr = argstr.replace("${assets_root}",os.path.join(path,"assets"))
    argstr = argstr.replace("${assets_index_name}",versionData.get("assets",versionData["id"]))
    argstr = argstr.replace("${auth_uuid}",options.get("uuid","{uuid}"))
    argstr = argstr.replace("${auth_access_token}",options.get("token","{token}"))
    argstr = argstr.replace("${user_type}","mojang")
    argstr = argstr.replace("${version_type}",versionData["type"])
    argstr = argstr.replace("${user_properties}","{}")
    argstr = argstr.replace("${resolution_width}",options.get("resolutionWidth","854"))
    argstr = argstr.replace("${resolution_height}",options.get("resolutionHeight","480"))
    argstr = argstr.replace("${game_assets}",os.path.join(path,"assets","virtual","legacy"))
    argstr = argstr.replace("${auth_session}",options.get("token","{token}"))
    return argstr

def get_arguments_string(versionData,path,options):
    arglist = []
    for v in versionData["minecraftArguments"].split(" "):
        v = replace_arguments(v,versionData,path,options)
        arglist.append(v)
    #Custom resolution is not in the list
    if options.get("customResolution",False):
        arglist.append("--width")
        arglist.append(options.get("resolutionWidth","854"))
        arglist.append("--height")
        arglist.append(options.get("resolutionHeight","480"))
    if options.get("demo",False):
        arglist.append("--demo")
    return arglist

def get_arguments(data,versionData,path,options):
    arglist = []
    for i in data:
        #Rules might has 2 different names in different versions.json
        if not parseRuleList(i,"compatibilityRules",options):
            continue
        if not parseRuleList(i,"rules",options):
            continue
        #i could be the argument
        if isinstance(i,str):
            arglist.append(replace_arguments(i,versionData,path,options))
        else:
            #Sometimes  i["value"] is the argument
            if isinstance(i["value"],str):
                arglist.append(replace_arguments(i["value"],versionData,path,options))
            #Sometimes i["value"] is a list of arguments
            else:
                for v in i["value"]:
                    v = replace_arguments(v,versionData,path,options)
                    arglist.append(v)
    return arglist

def get_minecraft_command(version,path,options):
    options = copy.copy(options)
    with open(os.path.join(path,"versions",version,version + ".json")) as f:
        data = json.load(f)
    if "inheritsFrom" in data:
        data = inherit_json(data,path)
    options["nativesDirectory"] = options.get("nativesDirectory",os.path.join(path,"versions",data["id"],"natives"))
    options["classpath"] = get_libraries(data,path)
    command = [options.get("executablePath","java")]
    if "jvmArguments" in options:
        command = command + options["jvmArguments"]
    #Newer Versions have jvmArguments in version.json
    if isinstance(data.get("arguments",None),dict):
        if "jvm" in data["arguments"]:
            command = command + get_arguments(data["arguments"]["jvm"],data,path,options)
        else:
            command.append("-Djava.library.path=" + options["nativesDirectory"])
            command.append("-cp")
            command.append(options["classpath"])
    else:
        command.append("-Djava.library.path=" + options["nativesDirectory"])
        command.append("-cp")
        command.append(options["classpath"])
    #The argument for the logger file
    if options.get("enableLoggingConfig",False):
        if "logging" in data:
            logger_file = os.path.join(path,"assets","log_configs",data["logging"]["client"]["file"]["id"])
            command.append(data["logging"]["client"]["argument"].replace("${path}",logger_file))
    command.append(data["mainClass"])
    if "minecraftArguments" in data:
        #For older versions
        command = command + get_arguments_string(data,path,options)
    else:
        command = command + get_arguments(data["arguments"]["game"],data,path,options)
    if "server" in options:
        command.append("--server")
        command.append(options["server"])
        if "port" in options:
            command.append("--port")
            command.append(options["port"])
    return command
