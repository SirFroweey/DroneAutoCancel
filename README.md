# Drone IO Auto-Cancel
> A Github webhook implementation to address Drone IO's missing "auto-cancelation of previous builds" feature.

## How it works
On `push` and on `pull_request` events are sent to the flask web-hook app and is authenticated using a SECRET env var named `WEBHOOK_VERIFY_TOKEN`. This token is then compared with the SECRET setup on your Github web-hook settings page for your repository as shown below:
![alt text](https://i.imgur.com/kbhtFhK.png "URL and secret setup and response type")

The flask app then compares the sha1 `ref` sent by either of those aforementioned `events` with the latest (last) Drone IO builds `hash`, if the hash do not match, that Drone build is then canceled (or stopped) via the Drone API. The Drone API agent is authenticated via a few env vars, listed below, so please assign these env vars on the machine running your web-hook.

## ENV VARS Setup
- `WEBHOOK_VERIFY_TOKEN`: A string, should be kept a secret; used to authenticate your app with Github's web-hook mechanism. This needs to match the `secret` value entered on your repo's webhook settings page.
- `DRONE_SERVER`: should be set as `https://drone.britecorepro.com`
- `DRONE_TOKEN`: your personal access token displayed on your profile page on our drone server (listed above).
- `DRONE_REPO_OWNER_USERNAME`: your github username, i.e.: `SirFroweey` is mine. Should be set to `IntuitiveWebSolutions` if we decide to host this app on our DevOps infrastructure.
- `DRONE_REPO_NAME`: your repository name, i.e.: 'BriteCore' or in this case `DroneAutoCancel`.

## Setting up local dev environment
- Setup your local machines environmental variables as shown above.
- Clone this repository on your machine.
- `cd` into your repository directory.
- Run `pip install -r requirements.txt` or even better, setup a virtualenv and activate it then install the requirements.
- Download `ngrok` and move it into your `Applications/` folder.
- Create a symlink, as shown here: 

```
# cd into your local bin directory
cd /usr/local/bin

# create symlink
ln -s /Applications/ngrok ngrok
```

- Run `python hook.py` on your terminal of choice
- Execute `ngrok http 5000`
- Setup your repo's Github webhook as shown below and point it to your `ngrok` `https` URL that we generated earlier (via the `ngrok http 5000` command):

![alt text](https://i.imgur.com/kbhtFhK.png "URL and secret setup and response type")

![alt text](https://i.imgur.com/HBogfyB.png "Event types")

- The Github `event` event should report back as successful with a green `200` status code, as shown below:
![alt text](https://i.imgur.com/TU7bilO.png "Successful ping")


## Local docker setup
> To be completed... (Coming soon)
