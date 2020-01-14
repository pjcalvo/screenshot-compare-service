from flask import Blueprint, request
from vvs.libs import folders_setup, image_capture, image_compare
from vvs.libs.storage import GoogleClient

import os
from datetime import datetime


# need to config this
BASE_DIR = 'base'
DIFFERENCES_DIR = 'differences'
TARGETS_DIR = 'targets'
DEFAULT_RESOLUTION = (1024, 768)

SCREENSHOTS_CROSS_TEST_NAME = 'cross_browser'
SCREENSHOTS_CROSS_DIR = 'screenshots_cross'

SCREENSHOTS_SITE_TEST_NAME = 'cross_site'
SCREENSHOTS_SITE_DIR = 'screenshots_site'

api = Blueprint('api', 'api', url_prefix='/api')

@api.route('/crossbrowser', methods=['POST'])
def crossbrowser():
    """
    Expected json style:
    {
        "url":"https://www.google.com",
        "browsers":{
            "base":"chrome",
            "targets":["firefox","safari"]
        }
    }
    """
    try:
        # simple validation
        body = request.get_json()
        url = body.get('url')
        base = body.get('browsers').get('base')
        targets = body.get('browsers').get('targets')
        if not url or not base or not targets or len(targets) == 0:
            return {'message': 'Missing required params <url, base, targets> '}, 400
    except Exception as ex:
        print(ex)
        return {'message': 'Missing required params <browser, base, targets> '}, 400

    try:
        # create a temporary folder
        temp_folder = folders_setup.create_temp_folder()
        # capture image
        # capture base image
        test_results = {'base': {'browser': base, 'file': ''}, 'targets': []}

        base_file = image_capture.capture_screens(
            url=url,
            browser=base,
            file_identificator='base',
            directory_path=temp_folder,
            test_name=SCREENSHOTS_CROSS_TEST_NAME,
            resolution=DEFAULT_RESOLUTION)
        test_results['base']['file'] = base_file

        # capture target images
        for target_browser in targets:
            result = image_capture.capture_screens(
                url=url,
                browser=target_browser,
                file_identificator=target_browser,
                directory_path=temp_folder,
                test_name=SCREENSHOTS_CROSS_TEST_NAME,
                resolution=DEFAULT_RESOLUTION)
            if result:
                test_results['targets'].append(
                    {'target_browser': target_browser, 'file': result, 'result': '', 'notes': ''})

        for target_result in test_results['targets']:
            difference_file = image_compare.analyze(
                                                    base=test_results['base']['file'],
                                                    target=target_result['file'],
                                                    source_dir=temp_folder,
                                                    differences_dir=temp_folder,
                                                    resolution=DEFAULT_RESOLUTION)
            if difference_file is None:
                target_result['result'] = 'Success'
                target_result['notes'] = 'There are no visual differences.'
            else:
                target_result['result'] = 'Failure'
                target_result['notes'] = 'Visual differences detected.'
                target_result['file'] = difference_file

        # upload to google
        gc = GoogleClient()
        timestamp = str(datetime.now())

        # upload base
        result = gc.upload_file(
            os.path.join(temp_folder, test_results['base']['file']),
            f'{timestamp}/base/{test_results["base"]["file"]}')
        test_results["base"]["file"] = result

        # upload results
        for target_result in test_results['targets']:
            print(target_result['file'])
            result = gc.upload_file(
                os.path.join(temp_folder, target_result['file']),
                f'{timestamp}/diff/{target_result["file"]}')
            target_result['file'] = result

        # remove temp folder
        folders_setup.delete_temp_folder(temp_folder)
        
        return {'message': test_results}
    

    except NotADirectoryError as ex:
        print(ex)
        return {'message': 'Something went wrong file processing the request'}, 500


@api.route('/crosssite', methods=['POST'])
def crosssite():
    """
    Expected json style:
    {
        "browser":"chrome",
        "urls":{
            "base":"https://www.google.com",
            "targets":["https://www.google.com?q=hola"]
        }
    }
    """
    try:
        # simple validation by
        body = request.get_json()
        browser = body.get('browser')
        base = body.get('urls').get('base')
        targets = body.get('urls').get('targets')
        if not browser or not base or not targets or len(targets) == 0:
            return {'message': 'Missing required params <browser, base, targets> '}, 400
    except Exception as ex:
        print(ex)
        return {'message': 'Missing required params <browser, base, targets> '}, 400

    try:
        temp_folder = folders_setup.create_temp_folder()
        # capture images
        # capture base image
        test_results = {'base': {'url': base, 'file': ''}, 'targets': []}

        base_file = image_capture.capture_screens(
            url=base,
            browser=browser,
            file_identificator='base',
            directory_path=temp_folder,
            test_name=SCREENSHOTS_SITE_TEST_NAME,
            resolution=DEFAULT_RESOLUTION)
        test_results['base']['file'] = base_file

        # capture target images
        count = 0
        for target_url in targets:
            target_file = image_capture.capture_screens(
                url=target_url,
                browser=browser,
                file_identificator=f'{count}',
                directory_path=temp_folder,
                test_name=SCREENSHOTS_SITE_TEST_NAME,
                resolution=DEFAULT_RESOLUTION)
            count += 1
            test_results['targets'].append(
                {'target_url': target_url, 'file': target_file, 'result': '', 'notes': ''})

        for target_result in test_results['targets']:
            difference_file = image_compare.analyze(base=test_results['base']['file'],
                                                    target=target_result['file'],
                                                    differences_dir=temp_folder,
                                                    source_dir=temp_folder,
                                                    resolution=DEFAULT_RESOLUTION)
            if difference_file is None:
                target_result['result'] = 'Success'
                target_result['notes'] = 'There are no visual differences.'
            else:
                target_result['result'] = 'Failure'
                target_result['notes'] = 'Visual differences detected.'
                target_result['file'] = difference_file
        
        # upload to google
        gc = GoogleClient()
        timestamp = str(datetime.now())

        # upload base
        result = gc.upload_file(
            os.path.join(temp_folder, test_results['base']['file']),
            f'{timestamp}/base/{test_results["base"]["file"]}')
        test_results["base"]["file"] = result

        # upload results
        for target_result in test_results['targets']:
            print(target_result['file'])
            result = gc.upload_file(
                os.path.join(temp_folder, target_result['file']),
                f'{timestamp}/diff/{target_result["file"]}')
            target_result['file'] = result

        # remove temp folder
        folders_setup.delete_temp_folder(temp_folder)

        return {'message': test_results}

    except Exception as ex:
        print(ex)
        return {'message': 'Something went wrong file processing the request'}, 500
