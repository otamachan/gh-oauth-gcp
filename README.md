# gh-oauth-gcp

https://otamachan.github.io/gh-oauth-gcp/

This is a sample web page application using GitHub OAuth.
A web page only application cannot use GitHub OAuth because its endpoint does not support CORS. https://github.com/isaacs/github/issues/330 .
In this sample application, I use Cloud Functions to enable GitHub OAuth login with CORS support.

# HowTo

## Initial setup

```
# create a project
gcloud projects create gh-oauth-gcp
# set a project
gcloud config set project gh-oauth-gcp
# enable billing
sensible-browser https://console.cloud.google.com/
# enable services
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com
# set a region
gcloud config set functions/region asia-northeast1
# create a secret
gcloud secrets create secrets --replication-policy="automatic"
# set a secret
echo -n '{"client_id":"xxx","client_secret":"yyyy"}' | gcloud secrets versions add secrets --data-file=-
# apply permission
gcloud secrets add-iam-policy-binding secrets --role roles/secretmanager.secretAccessor --member serviceAccount:gh-oauth-gcp@appspot.gserviceaccount.com
```

## Deploy
```bash
# deploy a function
gcloud functions deploy login --entry-point login --runtime python38 --trigger-http --allow-unauthenticated --memory 128MB --timeout 5
```
