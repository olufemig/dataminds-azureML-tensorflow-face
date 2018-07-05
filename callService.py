import argparse
import sys
import cv2
import time
import json
import pickle
import requests


def main(args):
    parser = argparse.ArgumentParser(description='Call the face recognition service')
    parser.add_argument('-u', '--url', default='http://localhost/score', type=str, help='Service URL')
    parser.add_argument('-p', '--path', default='test_image.jpg', type=str, help='Path to test image')
    parser.add_argument('-k','--key',type=str,help='service key',default=None)
    #key is only needed when deploying to AKS cluster. Local service does not require key. Default = None.
    args = parser.parse_args()
    path = args.path
    key = args.key
    url = args.url
    img_raw = cv2.imread(path)
    img_pkl = pickle.dumps(img_raw) #img_pkl is of type bytes
    img_utf8 = bytes(img_pkl,'utf-8')
    #call the webservice here (see also the removeThis sample project in workbench)

    headers = {'Content-Type': 'application/json'}
    if key is not None and key is not []:
    #key is only needed when deploying to AKS cluster. Local service does not require key. Default = None.
        headers['Authorization'] = 'Bearer ' + key
    #data = '{"input_df": [{"image base64 string": "' + img_pkl + '"}]}'
    data = img_pkl
    print(data[0:2])

    startTime = time.time()
    res = requests.post(url,headers=headers,data=data)
    try:
        resDict = json.loads(res.json())
        apiDuration   = int(float(resDict['executionTimeMs']))
        localDuration = int(float(1000.0*(time.time() - startTime)))
        print(resDict)
    except:
        print("ERROR: webservice returned message " + res.text)
    


if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()