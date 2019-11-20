import platform

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

def getNatives(data):
    if "natives" in data:
        if platform.system() == 'Windows':
            if "windows" in data["natives"]:
                return data["natives"]["windows"]
            else:
                return ""
        elif platform.system() == 'Darwin':
            if "osx" in data["natives"]:
                return data["natives"]["osx"]
            else:
                return ""           
        else:
            if "linux" in data["natives"]:
                return data["natives"]["linux"]
            else:
                return "" 
    else:
        return ""

