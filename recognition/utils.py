import base64
import cv2
from mysql.connector import MySQLConnection
import ast
from logger import logger
from datetime import datetime
import boto3
import pytesseract
import numpy as np
import imutils
import os
import re

DJANGO_ENV = os.environ.get('DJANGO_ENV')
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def get_task(connection):
    task = None
    try:
        cussor = connection.cursor()
        result = []
        cussor.execute("Select * from task where status = 0 order by updated_at ASC ")
        columns = tuple([d[0] for d in cussor.description])
        for row in cussor:
            result.append(dict(zip(columns, row)))
        if result:
            task = result[0]
        cussor.close()
    except MySQLConnection:
        logger.error("MySQL Connection error")
        pass
    return task


def get_bounding_boxex(template, connection):
    bounding_boxes = []

    if template:
        try:
            cussor = connection.cursor()
            template_id = template['id']
            query = f"Select * from bounding_box where template_id = {template_id}"
            cussor.execute(query)
            columns = tuple([d[0] for d in cussor.description])
            for row in cussor:
                bounding_boxes.append(dict(zip(columns, row)))
            cussor.close()
        except MySQLConnection:
            logger.error("MySQL Connection error")
            pass
    return bounding_boxes


def get_template(task, connection):
    template = None
    if task:
        try:
            cussor = connection.cursor()
            template_id = task['template_id']
            result = []
            if template_id:
                query = f"Select * from template where id = {template_id}"
                cussor.execute(query)
                columns = tuple([d[0] for d in cussor.description])
                for row in cussor:
                    result.append(dict(zip(columns, row)))

                if result:
                    template = result[0]
                cussor.close()
            else:
                update_task(task['id'], 3)
                logger.error(f"Task {task['id']} failed due to not having template")

        except MySQLConnection:
            logger.error("MySQL Connection error")
            pass
    return template


def get_coordinates(task, connection):
    metadatas = []
    coordinates_list = []
    template = get_template(task, connection)
    if template is not None:
        bounding_boxes = get_bounding_boxex(template, connection)
        if bounding_boxes is not None:
            for bounding_box in bounding_boxes:
                if bounding_box['metadata']:
                    metadatas.append((bounding_box['metadata'], bounding_box['id'], bounding_box['recognize_type']))
            else:
                update_task(task['id'], 3, connection)
                logger.error(f"Task {task['id']} failed due to not having bounding boxes ")
            for metadata in metadatas:
                res = ast.literal_eval(metadata[0])
                coordinates = []
                for _ in res:
                    x = _['x']
                    y = _['y']
                    coordinates.append((x, y))
                coordinates_list.append((coordinates, metadata[1], metadata[2]))
        else:
            update_task(task['id'], 3)
            logger.error(f"Task {task['id']} failed due to not having bounding boxes ")
    else:
        update_task(task['id'], 3)
        logger.error(f"Task {task['id']} failed due to not found required template")
    return coordinates_list


def update_task(task_id, _type, connection):
    try:
        cussor = connection.cursor()
        query = f"Update task set status = {_type} where id = {task_id}"
        cussor.execute(query)
        connection.commit()
        cussor.close()
    except MySQLConnection:
        logger.error("MySQL Connection error")
        pass


def save_result(text, image_id, bounding_box, task_id, connection):
    now = datetime.now()

    try:
        cussor = connection.cursor()
        query = f"INSERT INTO result(result, created_at, updated_at, image_id, bounding_box_id) VALUES ('{text}','{now}', '{now}', {image_id},{bounding_box})"
        cussor.execute(query)
        connection.commit()
        cussor.close()
        update_task(task_id, 2, connection)
    except MySQLConnection:
        logger.error("MySQL Connection error")
        update_task(task_id, 3, connection)
        logger.error(f"Task {task_id} failed due to cannot save results")
        pass


def get_image(task_id, connection):
    images = []
    try:
        cussor = connection.cursor()
        query = f"Select * from image where task_id = {task_id}"
        cussor.execute(query)
        columns = tuple([d[0] for d in cussor.description])
        for row in cussor:
            images.append(dict(zip(columns, row)))
        cussor.close()
    except MySQLConnection:
        logger.error("MySQL Connection error")
        pass
    if not images:
        update_task(task_id, 3)
        logger.error(f"Task {task_id} failed due to not having images")
    return images


def check_email(email):
    if re.search(regex, email):
        return True
    else:
        return False


def recognize_digits(image):
    text = pytesseract.image_to_string(image, config='digits')
    return text


def recognize_eng(image):
    text = pytesseract.image_to_string(image, lang='eng')
    return text


def recognize_vie(image):
    text = pytesseract.image_to_string(image, lang='vie')
    return text


def recognize_checkbox(image):
    text = checkbox_detect(image)
    return text


def recognize_email(image):
    text = pytesseract.image_to_string(image, lang='eng')
    valid = check_email(text)
    if valid:
        return text
    else:
        return None


def file_downloader(file_name, file_type, image_type):
    is_production = DJANGO_ENV == 'production'
    if is_production:
        if image_type:
            return download_s3(os.path.join(file_type, file_name))
        else:
            return download_s3(os.path.join(file_type, 'thumbnails', file_name))
    else:
        if image_type:
            return download_local(os.path.join(file_type, file_name))
        else:
            return download_local(os.path.join(file_type, 'thumbnails', file_name))


def download_local(path):
    abs_path = os.path.join('/home/ngochainguyen/Documents/Test/', path)
    with open(abs_path, 'rb+') as file:
        return base64.b64encode(file.read())


def download_s3(path):
    s3 = boto3.client(service_name='s3', aws_access_key_id=settings.AWS_ACCESS_KEY,
                      aws_secret_access_key=settings.AWS_ACCESS_TOKEN)
    bucket_name = settings.AWS_BUCKET_NAME
    tmp_file = os.path.join('/tmp', f"{str(datetime.datetime.now())}.png")
    s3.download_file(bucket_name, path, tmp_file)
    with open(tmp_file, 'rb+') as file:
        return base64.b64encode(file.read())


def checkbox_detect(image):
    '''
    Ths function take image path or image as an input
    and detects checkbox in it


    1. Convert it into Grayscale
    2. Blur the Image
    3. Detect Edges using Canny edge detector
    4. Detect all the contours
    5. Identify the shape using area, threshold, aspect ratio,
    contours closed/open
    6. Draw boundaries on shapes found
    '''
    try:
        # 1. Convert it into Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 2. Blur the Image
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 3. Detect Edges using Canny edge detector the lower and upper threshold
        # boundaries are calculated using median and sigma
        sigma = 0.33
        v = np.median(blurred)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blurred, lower, upper)

        # 4. Detect all the contours and grab the values using imutilsgrab_contours
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        checkbox_contours = []

        areas_pt = []
        # Loop over each and every contours for filtering the shape

        for c in cnts:
            # 5. Identify the shape using area, threshold, aspect ratio, contours closed/open
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.035 * peri, True)
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            area = cv2.contourArea(c)
            areas_pt.append((len(approx), area, aspect_ratio))
            if 10.0 < area < 250.0 and (0.82 <= aspect_ratio <= 1.2):
                # 6. Draw boundaries on shapes found
                checkbox_contours.append(c)

        if checkbox_contours:
            return 1
        else:
            return 0
    except Exception:
        pass
