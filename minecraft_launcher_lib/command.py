from minecraft_launcher_lib.helper import parseRuleList, getNatives
import json
import os

def get_libraries(data,path):
    libstr = ""
    for i in data["libraries"]:
        if not parseRuleList(i,"rules",{}):
            continue
        currentPath = os.path.join(path,"libraries")
        libPath, name, version = i["name"].split(":")
        for l in libPath.split("."):
            currentPath = os.path.join(currentPath,l)
        currentPath = os.path.join(currentPath,name,version)
        native = getNatives(i)
        if native == "":
            jarFilename = name + "-" + version + ".jar"
        else:
            jarFilename = name + "-" + version + "-" + native + ".jar"
        #if jarFilename == "jinput-platform-2.0.5-natives-linux.jar":
        #    continue
        currentPath = os.path.join(currentPath,jarFilename)
        if not os.path.isfile(currentPath):
            print(currentPath)
        libstr = libstr + currentPath + ":"
    libstr = libstr + os.path.join(path,"versions",data["id"],data["id"] + ".jar")
    return libstr

def replace_arguments(argstr,versionData,path,options):
    #Replace all arguments with the needed value
    argstr = argstr.replace("${auth_player_name}",options.get("username","{username}"))
    argstr = argstr.replace("${version_name}",versionData["id"])
    argstr = argstr.replace("${game_directory}",options.get("gameDirectory",path))
    argstr = argstr.replace("${assets_root}",os.path.join(path,"assets"))
    argstr = argstr.replace("${assets_index_name}",versionData["assets"])
    argstr = argstr.replace("${auth_uuid}",options.get("uuid","{uuid}"))
    argstr = argstr.replace("${auth_access_token}",options.get("token","{token}"))
    argstr = argstr.replace("${user_type}","mojang")
    argstr = argstr.replace("${version_type}",versionData["type"])
    return argstr

def get_arguments_string(versionData,path,options):
    arglist = []
    for v in versionData["minecraftArguments"].split(" "):
        v = replace_arguments(v,versionData,path,options)
        arglist.append(v)
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

def get_command(version,path,options):
    with open(os.path.join(path,"versions",version,version + ".json")) as f:
        data = json.load(f)
    command = ["java"]
    command.append("-Xms512M")
    command.append("-Xmx512M")
    command.append("-Djava.library.path=" + os.path.join(path,"versions",data["id"],"natives"))
    command.append("-cp")
    command.append(get_libraries(data,path))
    command.append(data["mainClass"])
    if "minecraftArguments" in data:
        #For older versions
        command = command + get_arguments_string(data,path,options)
    else:
        command = command + get_arguments(data["arguments"]["game"],data,path,options)
    return command
