from utils.image_utils import image_to_base64, load_image
import re
import os


MAP_PROMPT_EN = """
The map image is shown below:
"""

def make_map_prompt(map_descriptions, map_images, map_path, is_resize=False):
    messages = []
    map_images = []
    map_descriptions = []
    loaded_map_images = []
    map_description = MAP_PROMPT_EN
    
    messages.append(
    {
        'type': 'text',
        'text': map_description
    })
    

    if os.path.exists(map_path):
        map_image = load_image(map_path)
        if map_image:
            map_descriptions.append("")
            loaded_map_images.append(map_image)
            map_images.append(map_path)

    for i, map_image in enumerate(loaded_map_images):

        messages.append({
            'type': 'image_url',
            'image_url': {
                'url': image_to_base64(map_image),
            }
        })

    return messages

