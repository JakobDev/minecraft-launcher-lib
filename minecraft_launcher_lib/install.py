from minecraft_launcher_lib.helper import parseRuleList, getNatives
import requests
import shutil
import json
import os

def empty(arg):
    pass

def download_file(url,path,callback):
    if os.path.isfile(path):
        return
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    callback.get("setStatus",empty)("Download " + os.path.basename(path))
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

def install_libraries(data,path,callback):
    callback.get("setMax",empty)(len(data["libraries"]))
    for count, i in enumerate(data["libraries"]):
        if not parseRuleList(i,"rules",{}):
            continue
        currentPath = os.path.join(path,"libraries")
        libPath, name, version = i["name"].split(":")
        for l in libPath.split("."):
            currentPath = os.path.join(currentPath,l)
        currentPath = os.path.join(currentPath,name,version)
        native = getNatives(i)
        if native != "":
            jarFilenameNative = name + "-" + version + "-" + native + ".jar"
        jarFilename = name + "-" + version + ".jar"
        download_file(i["downloads"]["artifact"]["url"],os.path.join(currentPath,jarFilename),callback)
        if native != "":
            download_file(i["downloads"]["classifiers"][native]["url"],os.path.join(currentPath,jarFilenameNative),callback)
        callback.get("setProgress",empty)(count)

def install_assets(data,path,callback):
    #Download all assets
    download_file(data["assetIndex"]["url"],os.path.join(path,"assets","indexes",data["assets"] + ".json"),callback)
    with open(os.path.join(path,"assets","indexes",data["assets"] + ".json")) as f:
        assets_data = json.load(f)
    #The assets gas a hash. e.g. c4dbabc820f04ba685694c63359429b22e3a62b5
    #With this hash, it can be download from https://resources.download.minecraft.net/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    #And saved at assets/objects/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    callback.get("setMax",empty)(len(assets_data["objects"]))
    count = 0
    for key,value in assets_data["objects"].items():
        download_file("https://resources.download.minecraft.net/" + value["hash"][:2] + "/" + value["hash"],os.path.join(path,"assets","objects",value["hash"][:2],value["hash"]),callback)
        count += 1
        callback.get("setProgress",empty)(count)

def do_version_install(data,path,callback):
    #Download and read versions.json
    download_file(data["url"],os.path.join(path,"versions",data["id"],data["id"] + ".json"),callback)
    with open(os.path.join(path,"versions",data["id"],data["id"] + ".json")) as f:
        versiondata = json.load(f)
    install_libraries(versiondata,path,callback)
    install_assets(versiondata,path,callback)
    #Download minecraft.jar
    download_file(versiondata["downloads"]["client"]["url"],os.path.join(path,"versions",data["id"],data["id"] + ".jar"),callback)

def install_minecraft_version(versionid,path,callback=None):
    if callback == None:
        callback = {}
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    for i in version_list["versions"]:
        if i["id"] == versionid:
            do_version_install(i,path,callback)
            return
