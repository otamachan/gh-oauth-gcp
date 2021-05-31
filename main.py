import json
import random
import string
import urllib.parse
import urllib.request
from flask import redirect
from google.cloud import secretmanager

host = "github.com"
allow_origin = "https://otamachan.github.io"
scope = "user:email"
secret_name = "secrets"
project_id = "gh-oauth-gcp"
request = {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
client = secretmanager.SecretManagerServiceClient()
response = client.access_secret_version(request)
secret = json.loads(response.payload.data.decode("UTF-8"))


def login(request):
    if request.method == 'OPTIONS':
        headers = {
            "Access-Control-Allow-Origin": allow_origin,
            "Access-Control-Allow-Methods": "GET",
        }
        return ('', 204, headers)
    if request.args and "code" in request.args:
        params = {
            "code": request.args["code"],
            "client_id": secret["client_id"],
            "client_secret": secret["client_secret"],
        }
        if "state" in request.args:
            params["state"] = request.args["state"]
        req = urllib.request.Request(f"https://{host}/login/oauth/access_token?{urllib.parse.urlencode(params)}", method="POST")
        with urllib.request.urlopen(req) as res:
            body = res.read().decode("utf-8")
        headers = {
            "Access-Control-Allow-Origin": allow_origin,
        }
        return (json.dumps({k: v[0] for k, v in urllib.parse.parse_qs(body).items()}), 200, headers)
    params = {
        "client_id": secret["client_id"],
        "scope": scope,
        "state": "".join([random.choice(string.ascii_letters + string.digits) for i in range(12)]),
    }
    return redirect(f"https://{host}/login/oauth/authorize?{urllib.parse.urlencode(params)}")
