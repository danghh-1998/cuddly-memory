from PIL import Image, ImageEnhance
from time import sleep

from recognition.utils import *
from recognition.logger import logger
from recognition.connection import get_connection
from recognition.aws_recognition import aws_recognition


def recognition():
    connection = get_connection()
    if connection:
        task = get_task(connection=connection)
        if task:
            task_id = task['id']
            logger.info(f"Found task {task_id}")
            update_task(task_id=task_id, _type=1, connection=connection)
            coordinates_list, template_image_shape = get_coordinates(task=task, connection=connection)
            images_list = get_image(task_id=task_id, connection=connection)
            images = []
            if images_list:
                for _ in images_list:
                    data = file_downloader(_['image'], 'images', 1)
                    image = cv2.imdecode(np.frombuffer(data, np.uint8), 1)
                    images.append((image, _['id']))

            if images:
                for image in images:
                    for coordinates in coordinates_list:
                        _ = coordinates[0]
                        temp = image[0]
                        image_roi = temp[int(_[0][1]):int(_[1][1]), int(_[0][0]):int(_[1][0])]
                        if coordinates[2] == 3:
                            text = recognize_checkbox(image_roi)
                            bounding_box_id = coordinates[1]
                            save_result(text, image[1], bounding_box_id, task_id, connection)
                        else:
                            filename = "/tmp/{}.png".format(os.getpid())
                            cv2.imwrite(filename, image_roi)
                            text = aws_recognition(filename)
                            bounding_box_id = coordinates[1]
                            save_result(text, image[1], bounding_box_id, task_id, connection)
            task = get_task_by_id(connection=connection, id_=task_id)
            if task['status'] != 3:
                update_task(task_id, 2, connection)
        logger.info('No task found, sleeping...')
        sleep(1)
        connection.close()


if __name__ == "__main__":
    while True:
        logger.info('Start recognition')
        recognition()
