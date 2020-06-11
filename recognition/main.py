from datetime import timedelta
import os
import cv2
from utils import *
import base64
import numpy as np
from PIL import Image, ImageEnhance
from connection import get_connection
from timeloop import Timeloop
from logger import logger

t1 = Timeloop()


@t1.job(interval=timedelta(seconds=1))
def recognition():
    logger.info("Recognition is running")

    connection = get_connection()
    if connection:
        task = get_task(connection)
        if task:
            task_id = task['id']
            # update_task(task_id, 1)
            coordinates_list = get_coordinates(task, connection)
            images_list = get_image(task_id, connection)
            images = []
            if images_list:
                for _ in images_list:
                    data = file_downloader(_['name'], 'images', 1)
                    im_bytes = base64.b64decode(data)
                    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
                    image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
                    images.append((image, _['id']))

            if images:
                for image in images:
                    for coordinates in coordinates_list:
                        text = None
                        _ = coordinates[0]
                        temp = image[0]
                        image_roi = temp[_[0][1]:_[1][1],
                                    _[0][0]:_[1][0]]
                        if coordinates[2] == 5:
                            text = recognize_checkbox(image_roi)
                            bounding_box_id = coordinates[1]
                            save_result(text, image[1], bounding_box_id, task_id, connection)

                        filename = "{}.png".format(os.getpid())
                        cv2.imwrite(filename, image_roi)
                        image_roi = Image.open(filename)
                        img = image_roi.crop((3, 0, image_roi.size[0], image_roi.size[1]))
                        resized = img.resize(
                            (img.size[0] * 16, img.size[1] * 16), Image.ANTIALIAS
                        )
                        r1, g1, b1 = (200, 200, 100)
                        r2, g2, b2 = (255, 255, 255)
                        data = np.array(resized.convert('RGBA'))
                        red, green, blue, alpha = data.T
                        yellow_areas = (red > r1) & (green > g1) & (blue > b1)
                        data[..., :-1][yellow_areas.T] = (r2, g2, b2)
                        contrast = ImageEnhance.Contrast(Image.fromarray(data))
                        img = contrast.enhance(3)
                        os.remove(filename)
                        if coordinates[2] == 0:
                            text = recognize_eng(img)
                        elif coordinates[2] == 1:
                            text = recognize_vie(img)
                        elif coordinates[2] == 4:
                            text = recognize_digits(img)
                        elif coordinates[2] == 6:
                            text = recognize_email(img)
                        bounding_box_id = coordinates[1]
                        save_result(text, image[1], bounding_box_id, task_id, connection)
                        print(text)
        connection.close()


if __name__ == "__main__":
    try:
        t1.start(block=True)
    except Exception :
        pass
