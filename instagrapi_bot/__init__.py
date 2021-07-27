from typing import Tuple
from instagrapi import Client
import tempfile
from PIL import Image

accepted_aspect_ratio = {
    '1:1' : {'width': 1080, 'height': 1080},
    '4:5' : {'width': 1080, 'height': 1350}
}

class InstagrapiBot:
    def __init__(self, client: Client):
        assert isinstance(client, Client), "Invalid client"
        self._client = client

    def resize_and_upload(self, caption: str, image_path: str, aspect_ratio: str = '1:1', bg_color : Tuple[float,float,float] = (255,255,255)):
        """
        Resize photo to fit aspect ratio

        Parameters
        ----------
        caption: str
            Media caption
        image_path: str
            path to image
        aspect_ratio: str, optional
            resize aspect ratio (default 1:1)
        bg_color: Tuple[float,float,float], optional
            background color (default white (255,255,255))
        """
        assert aspect_ratio in accepted_aspect_ratio, 'Wrong aspect ratio! Must be one of {}'.format(list(accepted_aspect_ratio.keys()))
        
        destination = tempfile.mktemp(".jpeg")
        final_img = Image.new('RGB', (accepted_aspect_ratio[aspect_ratio]['width'], accepted_aspect_ratio[aspect_ratio]['height']), bg_color)

        with Image.open(image_path) as im:
            image_width, image_height = im.size
            width_difference = final_img.width - image_width
            height_difference = final_img.height - image_height

            if width_difference < height_difference:
                width_in_ratio = final_img.width
                reduction_percent = (final_img.width / float(image_width))
                height_in_ratio = int((float(image_height) * float(reduction_percent)))
            else:
                height_in_ratio = final_img.height
                reduction_percent = (final_img.height / float(image_height))
                width_in_ratio = int((float(image_width) * float(reduction_percent)))
            
            resized_im = im.resize((width_in_ratio, height_in_ratio))
        
        final_img.paste(resized_im, (int((final_img.width - resized_im.width) / 2), int((final_img.height - resized_im.height) / 2)))
        final_img.save(destination)

        self._client.photo_upload(path=destination,caption=caption)
