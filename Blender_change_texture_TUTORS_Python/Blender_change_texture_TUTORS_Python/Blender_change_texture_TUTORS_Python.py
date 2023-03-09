from asyncio.windows_events import NULL
import bpy
import os
import glob
import re

different_name = False

#function to remove packed images
def remove_packed_images():
    # Get the list of packed images in the current Blender file
    packed_images = [img for img in bpy.data.images if img.packed_file is not None]

    # Remove each packed image from the Blender file
    for img in packed_images:
        bpy.data.images.remove(img)

# Get the path of the current Blender file
filepath = bpy.data.filepath

# Remove the filename from the path to get the directory path
dirpath = os.path.dirname(filepath)
# Set the base directory where the textures are stored
base_dir = dirpath

# Loop through each directory in the base directory
for subdir in os.listdir(base_dir):
    remove_packed_images()
    # Construct the full path of the current directory
    current_dir = os.path.join(base_dir, subdir)
    
    # Look for the texture file named "Texture01"
    texture_file = glob.glob(os.path.join(current_dir, "Texture01.*"))
    
    
    # If a texture file is found, load it into Blender
    if texture_file:
        img = bpy.data.images.load(texture_file[0])
        
        #check if there is object with the name
        if "obj0.002" not in bpy.data.objects:
            obj_name = "Jersey_Red.001"
            
        else:
            # Set the name of the object whose texture we want to change
            obj_name = "obj0.002"
        
        
        # Get the object by name
        obj = bpy.data.objects[obj_name]

        # Get the material of the object
        mat = obj.material_slots[0].material
        
        # Set the texture of the material
        mat.node_tree.nodes["Image Texture"].image = img

        # Pack the texture image into the Blender file
        img.pack()

        ###

        subdir_list = re.split("-|_", subdir)
        player_name = subdir_list[4]
        player_name = player_name.lower().capitalize()
        player_number = subdir_list[3]
        rarity = subdir_list[2]
        rarity = rarity.lower().capitalize()
        series = subdir_list[0].upper() + " "+ subdir_list[1].upper()
        


        obj2_name = "Text.003"

        # Get the object by name
        obj2 = bpy.data.objects[obj2_name]

        # Change the text of the object
        obj2.data.body = f"#{player_number} {player_name} - {rarity} Edition\n{series}\nAnniversary Series"

        # Save the blend file with a new name
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(current_dir, "{}.blend".format(subdir)), check_existing=False)