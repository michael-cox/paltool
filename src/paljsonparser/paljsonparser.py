#!/usr/bin/python3

import json_stream
# players json
# properties.worldSaveData.value.CharacterSaveParameterMap.

class PalCharacterData:
    def __init__(self, datastream):
        self.root_objs = {}
        for obj in datastream["properties"]["worldSaveData"]["value"]["CharacterSaveParameterMap"]["value"]:
            self.__load_object(obj)

    def __load_object(self, obj):

        # read obj[key] 
        player_uid = ''
        instance_id = ''
        for param,struct in obj["key"].items():
            if param == 'PlayerUId':
                player_uid = struct["value"]
            elif param == 'InstanceId':
                instance_id = struct["value"]

        # get parent object in our map structure
        parent_obj = None
        if player_uid in self.root_objs:
            parent_obj = self.root_objs[player_uid]
        else:
            parent_obj = PalObject(player_uid)
            self.root_objs[player_uid] = parent_obj

        # read obj[value]
        
        current_obj = None
        save_params = {}
        for key,struct_value in obj["value"]["RawData"]["value"]["object"]["SaveParameter"]["value"].items():
            if key == "Gender":
                save_params[key] = struct_value["value"]["value"]
            elif key == "PassiveSkillList":
                save_params[key] = [value for value in struct_value["value"]["values"]]
            else:
                save_params[key] = struct_value["value"]

        if "IsPlayer" in save_params and save_params["IsPlayer"]:
            current_obj = parent_obj
            current_obj.instance_id = instance_id
        else:
            current_obj = PalObject(instance_id)
            parent_obj.children.append(current_obj)

        current_obj.save_params = save_params

class PalObject:
    def __init__(self, uuid):
        self.uuid = uuid
        self.instance_id = None
        self.save_params = []
        self.children = []


def load_level(level_file):
    data = json_stream.load(level_file)
    character_data = PalCharacterData(data)
    return character_data

def main():
    with open("/home/miccox3/devel/pal_savegame_test/solo_world/Level.sav.json", "r") as f:
        character_data = load_level(f)
    return character_data
