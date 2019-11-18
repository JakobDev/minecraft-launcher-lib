from minecraft_launcher_lib.helper import parseRuleList, getNatives
import requests
import shutil
import json
import os

def download_file(url,path):
    if os.path.isfile(path):
        return
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    print("Download " + url + " as " + path)
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

def install_libraries(data,path):
    for i in data["libraries"]:
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
        download_file(i["downloads"]["artifact"]["url"],os.path.join(currentPath,jarFilename))
        if native != "":
            download_file(i["downloads"]["classifiers"][native]["url"],os.path.join(currentPath,jarFilenameNative))

def install_assets(data,path):
    #Download all assets
    download_file(data["assetIndex"]["url"],os.path.join(path,"assets","indexes",data["id"] + ".json"))
    with open(os.path.join(path,"assets","indexes",data["id"] + ".json")) as f:
        assets_data = json.load(f)
    #The assets gas a hash. e.g. c4dbabc820f04ba685694c63359429b22e3a62b5
    #With this hash, it can be download from https://resources.download.minecraft.net/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    #And saved at assets/objects/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    for key,value in assets_data["objects"].items():
        download_file("https://resources.download.minecraft.net/" + value["hash"][:2] + "/" + value["hash"],os.path.join(path,"assets","objects",value["hash"][:2],value["hash"]))

def do_version_install(data,path):
    #Download and read versions.json
    download_file(data["url"],os.path.join(path,"versions",data["id"],data["id"] + ".json"))
    with open(os.path.join(path,"versions",data["id"],data["id"] + ".json")) as f:
        versiondata = json.load(f)
    install_libraries(versiondata,path)
    install_assets(versiondata,path)
    #Download minecraft.jar
    download_file(versiondata["downloads"]["client"]["url"],os.path.join(path,"versions",data["id"],data["id"] + ".jar"))

def install_version(versionid,path):
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    for i in version_list["versions"]:
        if i["id"] == versionid:
            do_version_install(i,path)
            return
