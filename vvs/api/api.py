from flask import Blueprint, request
from vvs.libs import folders_setup, image_capture, image_compare

import os


# need to config this
BASE_DIR = 'base'
DIFFERENCES_DIR = 'differences'
TARGETS_DIR = 'targets'
DEFAULT_RESOLUTION = (1024, 768)

SCREENSHOTS_CROSS_TEST_NAME = 'cross_browser'
SCREENSHOTS_CROSS_DIR = 'screenshots_cross'

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
    # simple validation 
    body = request.get_json()
    url = body.get('url')
    base = body.get('browsers').get('base')
    targets = body.get('browsers').get('targets')
    if not url or not base or not targets or len(targets) == 0:
        return {'message': 'Missing required params <url, base, targets> '} , 400

    # create folders
    screenshots_folder = folders_setup.create_folders(SCREENSHOTS_CROSS_DIR)

    # capture images
    # capture base image

    test_results = {'base':{'browser':base, 'file':''}, 'targets' : []}

    base_folder = os.path.join(screenshots_folder, BASE_DIR)
    base_file = image_capture.capture_screens(url=url, 
                                            browser=base, 
                                            file_identificator = 'base', 
                                            directory_path = base_folder, 
                                            test_name = SCREENSHOTS_CROSS_TEST_NAME,
                                            resolution = DEFAULT_RESOLUTION)
    test_results['base']['file'] = base_file
    
    # capture target images
    target_folder = os.path.join(screenshots_folder, TARGETS_DIR)
    for target_browser in targets:
        target_file = image_capture.capture_screens(url=url, 
                                                browser=target_browser, 
                                                file_identificator = target_browser, 
                                                directory_path = target_folder, 
                                                test_name = SCREENSHOTS_CROSS_TEST_NAME,
                                                resolution = DEFAULT_RESOLUTION)
        test_results['targets'].append({'target_browser': target_browser, 'file':target_file, 'result':'', 'notes':''})

    differences_folder = os.path.join(screenshots_folder, DIFFERENCES_DIR)
    for target_result in test_results['targets']:
        difference_file = image_compare.analyze(base = test_results['base']['file'], 
                                                target = target_result['file'], 
                                                differences_dir = differences_folder,
                                                resolution = DEFAULT_RESOLUTION)
        if difference_file is None:
            target_result['result'] =  'Success' 
            target_result['notes'] = 'There are no visual differences.'
        else:
            target_result['result'] = 'Failure'
            target_result['notes'] = 'Visual differences detected.' 
            target_result['file'] =  difference_file
            
    return {'message': test_results }


# @api.route('/crosssite', methods=['POST'])
# def crossbrowser():
#     """
#     Expected json style:
#     {
#         "browser":"chrome",
#         "urls":{
#             "base":"https://www.google.com",
#             "targets":["https://www.google.com?q=hola"]
#         }
#     }
#     """ 
#     # simplet validation by
#     body = request.get_json()
#     browser = body.get('browser')
#     base = body.get('urls').get('base')
#     targets = body.get('urls').get('targets')
#     if not browser or not base or not targets or len(targets) == 0:
#         return {'message': 'Missing required params <browser, base, targets> '} , 400

#     # capture images
#     image_capture = ImageCapture(url, CrossBrowserModel(base, targets))
#     cb = image_capture.capture_screens()
#     if cb is None:
#         return {'message': 'Something went wrong '} ,500

#     results = []
#     for target in cb.targets:
#         print(cb.differences_folder)
#         difference_file = ImageCompare(cb.base['file'], target['file'], cb.differences_folder)
#         if difference_file is None:
#             results.append({'target_browser': target['browser'], 
#                             'result': 'success', 
#                             'notes':'There are no visual differences.'})
#         else:
#             results.append({'target_browser': target['browser'], 
#                             'result': 'failure', 
#                             'notes':'Visual differences detected.', 
#                             'file': difference_file})
            
#     return {'message': {'base_browser': base, 'results': results}}
