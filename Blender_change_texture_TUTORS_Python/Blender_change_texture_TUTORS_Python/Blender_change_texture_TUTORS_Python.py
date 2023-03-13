from ast import Return
import bpy
import os
import glob
import re

#
#change that window name where you usually change that new texture name must be: Image Texture
#


#can change series years no need to find it middle of code.
Years = "22 - 23"



#function to remove packed images
def remove_packed_images(series_number):
    # Get the list of packed images in the current Blender file
    packed_images = [img for img in bpy.data.images if img.packed_file is not None]
    if series_number != 1:
        # Remove each packed image that contains "BaseColor" in its name
        for img in packed_images:
            if "BaseColor" in img.name:
                bpy.data.images.remove(img)
    else:
        # Remove each packed image from the Blender file
        for img in packed_images:
            bpy.data.images.remove(img)

#def make function to but space middle of string
def make_space_middle(string):
    mid = len(string) // 2
    first_part = string[:mid]
    second_part = string[mid:]
    return first_part.lower().capitalize() + " " + second_part.lower().capitalize()
    

#function to check from subfolder name first part what series we blendering 
def check_series(first_part_of_sub):
    if first_part_of_sub.upper() == "RETRO":
        return 1
    elif first_part_of_sub.upper() == "HIFK2":
        return 2
    elif first_part_of_sub.upper() == "HIFK3":
        return 3
    


#function to arrenges subfolder name to correct order
def arrenge_subfolder(subF ,series_number):
    remake_list = []
    
    if series_number == 1:
        
        remake_list.append(subF[3])
        remake_list.append(subF[4])
        remake_list.append(subF[2])
        remake_list.append(subF[1])
        remake_list.append(subF[0])
        
        return remake_list
        
    elif series_number == 2:
        remake_list.append(subF[1])
        remake_list.append(subF[2])
        remake_list.append(subF[4])
        remake_list.append(subF[3])
        remake_list.append(Years)
        return remake_list
        
    elif series_number == 3:
        series_number = 3
        #numero, nimi, rarity, sarja, merkki
        #number, name, rarity, series, brand
        remake_list.append(subF[1])
        remake_list.append(subF[2])
        remake_list.append(subF[4])
        remake_list.append(make_space_middle(subF[3]))
        remake_list.append(Years)
        
        
        return remake_list
    
    
    

# Get the path of the current Blender file
filepath = bpy.data.filepath

# Remove the filename from the path to get the directory path
dirpath = os.path.dirname(filepath)
# Set the base directory where the textures are stored
base_dir = dirpath

# Loop through each directory in the base directory
for subdir in os.listdir(base_dir):

    #make subdir_list variable to split the name of the folder
    subdir_list = re.split("-|_| ", subdir)

    #check if series number
    series_number = check_series(subdir_list[0])

    #arrenge subfolder name to correct order
    subdir_list = arrenge_subfolder(subdir_list, series_number)
    
    
    # Construct the full path of the current directory
    current_dir = os.path.join(base_dir, subdir)
    
    #check if series is anniversary
    if series_number == 1:
        # Look for the texture file named "Texture01"
        texture_file = glob.glob(os.path.join(current_dir, "Texture01.*"))
    else:
        # look for the texture file named "*_BaseColor
        texture_file = glob.glob(os.path.join(current_dir, "*_BaseColor.*"))
    
    
    #if texture file is found, start make new blender file
    if texture_file:
        
        # Remove the packed images from the Blender file
        remove_packed_images(series_number)
        
        # If a texture file is found, load it into Blender
        img = bpy.data.images.load(texture_file[0])
        
        #check if series is anniversary
        if series_number == 1:
            obj_name = "obj0.002"
        elif series_number == 2:
            obj_name = "Jersey_Red.001"
        else:
            obj_name = "Jersey"
            
        
        
        
        # Get the object by name
        obj = bpy.data.objects[obj_name]

        # Get the material of the object
        mat = obj.material_slots[0].material
        
        # Set the texture of the material
        mat.node_tree.nodes["Image Texture"].image = img

        # Pack the texture image into the Blender file
        img.pack()
        
        ###

        #set subdir to variables
        player_name = subdir_list[1]
        player_name = player_name.lower().capitalize()
        player_number = subdir_list[0]
        rarity = subdir_list[2]
        rarity = rarity.lower().capitalize()
        series = subdir_list[3].upper() + " "+ subdir_list[4].upper()
        

        if series_number !=2:
            obj2_name = "Text.003"
        else:
            obj2_name = "Text.005"

        # Get the object by name
        obj2 = bpy.data.objects[obj2_name]

        #check if series is anniversary
        if series_number == 1:
            # Change the text of the object
            obj2.data.body = f"#{player_number} {player_name} - {rarity} Edition\n{series}\nAnniversary Series"
        elif series_number == 2:
            obj2.data.body = f"#{player_number} {player_name} - {rarity} Edition\n\n          {series}"
        else:
            # Change the text of the object
            obj2.data.body = f"#{player_number} {player_name} - {rarity} Edition\n{series}" 

        # Save the blend file with a new name
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(current_dir, "{}.blend".format(subdir)), check_existing=False)