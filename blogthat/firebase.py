from firebase_admin import credentials, initialize_app, storage
import environ
import json
env = environ.Env()
environ.Env.read_env()

cred = None
# Init firebase with your credentials
try:
        cred = credentials.Certificate("blogthat/firebase_keys.json")
except:
        google_credentials = env('GOOGLE_APPLICATION_CREDENTIALS')
        google_credentials = json.loads(google_credentials)
        cred = credentials.Certificate(google_credentials)


initialize_app(cred, {'storageBucket': 'bloggingpool.appspot.com'})

def upload_to_firebase(filename):
        # Put your local file path
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_filename(filename)
        # Opt : if you want to make public access from the URL
        blob.make_public()
        print("your file url: ", blob.public_url)
        return blob.public_url



