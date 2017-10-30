import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '9eca7af565a64946adc7626c44935eb5'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = "show me some action movies"

    response = json.loads(request.getresponse().read())

    print (response['result']['fulfillment']['speech'])


if __name__ == '__main__':
    main()