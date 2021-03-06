import base64
import os
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from utils.folder_file_manager import save_file
from settings import VISION_CREDENTIAL_PATH, CUR_DIR, LOCAL


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = VISION_CREDENTIAL_PATH
DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


class GoogleVisionAPI:
    """Construct and use the Google Vision API service."""

    def __init__(self):

        self.credentials = GoogleCredentials.get_application_default()

        self.service = discovery.build('vision', 'v1', credentials=self.credentials, discoveryServiceUrl=DISCOVERY_URL)

    def detect_text(self, img_path, file_name, dir_name=None):
        """ Uses the Vision API to detect text in the given file. """

        request_list = []
        feature_type = 'DOCUMENT_TEXT_DETECTION'

        with open(img_path, 'rb') as img_file:
            content_json_obj = {'content': base64.b64encode(img_file.read()).decode('UTF-8')}

            feature_json_obj = [{'type': feature_type}]

            request_list.append(
                {'image': content_json_obj,
                 'features': feature_json_obj}
            )

        request = self.service.images().annotate(
            body={'requests': request_list})

        try:
            response = request.execute()

            ret_json = response['responses'][0]
            if LOCAL:
                json_file_path = os.path.join(CUR_DIR, 'test_json', f"temp_{dir_name}_{file_name}.json")
                save_file(filename=json_file_path, content=json.dumps(ret_json), method="w")

            return ret_json

        except Exception as e2:
            print("Key error: %s" % e2)


if __name__ == '__main__':

    vision = GoogleVisionAPI()

    """Call the Vision API on a file and index the results."""
    texts = vision.detect_text(img_path="", file_name=""),
    print(texts)
