from flask import Blueprint, request
from vvs.services.image_capture import ImageCapture
from vvs.services.image_compare import analyze as ImageCompare
from vvs.model.crossbrowser import CrossBrowserModel

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
    # simplet validation by
    body = request.get_json()
    url = body.get('url')
    base = body.get('browsers').get('base')
    targets = body.get('browsers').get('targets')
    if not url or not base or not targets or len(targets) == 0:
        return {'message': 'Missing required params <url, base, targets> '} , 400

    # capture images
    image_capture = ImageCapture(url, CrossBrowserModel(base, targets))
    cb = image_capture.capture_screens()
    if cb is None:
        return {'message': 'Something went wrong '} ,500

    results = []
    for target in cb.targets:
        print(cb.differences_folder)
        difference_file = ImageCompare(cb.base['file'], target['file'], cb.differences_folder)
        if difference_file is None:
            results.append({'result': 'success', 'notes':'There are no visual differences.'})
        else:
            results.append({'result': 'failure', 
                            'notes':'Visual differences detected.', 
                            'file': difference_file})
            
    return {'message': results}
