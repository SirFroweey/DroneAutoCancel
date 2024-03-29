# Drone IO Auto-Cancel
> A Github webhook implementation to address Drone IO's missing "auto-cancelation of previous builds" feature.

## Contact
- David Almendarez (`@david`)

## How it works
On `push` and on `pull_request` events are sent to the flask web-hook app and is authenticated using a SECRET env var named `WEBHOOK_VERIFY_TOKEN`. This token is then compared with the SECRET setup on your Github web-hook settings page for your repository as shown below:
![alt text](https://i.imgur.com/kbhtFhK.png "URL and secret setup and response type")

The flask app then compares the sha1 `after` (hash) sent by either of those aforementioned `events` with the latest (last) Drone IO builds `hash`, if the hash do not match, that Drone build is then canceled (or stopped) via the Drone API. The Drone API is authenticated via a few env vars, listed below, so please assign these env vars on the machine running your web-hook.

## ENV VARS Setup
- `WEBHOOK_VERIFY_TOKEN`: A string, should be kept a secret; used to authenticate your app with Github's web-hook mechanism. This needs to match the `secret` value entered on your repo's webhook settings page.
- `DRONE_SERVER`: should be set as `https://drone.britecorepro.com`
- `DRONE_TOKEN`: your personal access token displayed on your profile page on our drone server (listed above).
- `DRONE_REPO_OWNER_USERNAME`: your github username, i.e.: `SirFroweey` is mine. Should be set to `IntuitiveWebSolutions` if we decide to host this app on our DevOps infrastructure.
- `DRONE_REPO_NAME`: your repository name, i.e.: 'BriteCore' or in this case `DroneAutoCancel`.
- `ONLY_PROCESS_PR_EVENTS`: Boolean, should our hook only process `pull_request` event types? Defaults to `False`.

## Setting up local dev environment (Manual)
- Setup your local machines environmental variables as shown above.
- Clone this repository onto your machine.
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

- Pushing to your repository where you setup your web-hook (presumably your `BriteCore` fork), should report back with a successful `200` response as shown below:

![alt text](https://i.imgur.com/BvcCk1s.png "Successful push")


## Setting up local dev environment (Docker)
> Experimental for now, ask @david for access to private repo.

1. Install Docker
2. `docker login`
3. Run `docker-compose up`
4. Navigate to `127.0.0.1:5000/webhook` on your web browser and ensure you get a 405 page, this signals a successful startup.
5. Download `ngrok` and move it into your `Applications/` folder.
6. Create a symlink, as shown here: 

```
# cd into your local bin directory
cd /usr/local/bin

# create symlink
ln -s /Applications/ngrok ngrok
```

7. Execute `ngrok http 5000`
8. Setup your repo's Github webhook as shown below and point it to your `ngrok` `https` URL that we generated earlier (via the `ngrok http 5000` command):

![alt text](https://i.imgur.com/kbhtFhK.png "URL and secret setup and response type")

![alt text](https://i.imgur.com/HBogfyB.png "Event types")

- The Github `event` event should report back as successful with a green `200` status code, as shown below:
![alt text](https://i.imgur.com/TU7bilO.png "Successful ping")

9. Pushing to your repository where you setup your web-hook (presumably your `BriteCore` fork), should report back with a successful `200` response as shown below:

![alt text](https://i.imgur.com/BvcCk1s.png "Successful push")

## Updates
- It may be best to uncheck the `push` event from the Github web-hook settings page to prevent being spamming by `400` requests due to the `push` event being filtered out when setting the `ONLY_PROCESS_PR_EVENTS` environment variable to `True`.