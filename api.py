import requests
import os

DRONE_SERVER = os.getenv('DRONE_SERVER')
DRONE_ACCESS_TOKEN = os.getenv('DRONE_TOKEN')
DRONE_REPO_OWNER_USERNAME = os.getenv('DRONE_REPO_OWNER_USERNAME')
DRONE_REPO_NAME = os.getenv('DRONE_REPO_NAME')


class Drone:
    """DroneIO API interface.
    """
    def __init__(self, host, access_token, repo_owner, repo_name):
        """
        :param access_token -> Drone API token.
        :param repo_owner (str) -> Repo owner username.
        :param repo_name (str) -> Repo name.
        """
        self.host = host
        self.access_token = access_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_builds(self):
        """
        Get all builds on feed.
        """
        builds = requests.get("{host}/api/repos/{owner}/{repo}/builds?access_token={token}".format(
            host=self.host,
            owner=self.repo_owner,
            repo=self.repo_name,
            token=DRONE_ACCESS_TOKEN)
        ).json()
        return builds
	
    def get_latest_build(self):
        """
        Get latest (last) build.
        """
        return self.get_builds()[0]

    def stop_build(self, build_no):
        """Stop the specified build. 
        Please note this api requires administrative privileges and the request parameter {build} is not the build id but the build number.
        """
        stopped = requests.delete("{host}/api/repos/{owner}/{repo}/builds/{build}?access_token={token}".format(
            host=self.host,
            owner=self.repo_owner,
            repo=self.repo_name,
            build=build_no,
            token=DRONE_ACCESS_TOKEN
            )
        ).json()
        return stopped

    def stop_latest_build(self, compare_sha_hash=None):
        """
        Stop latest (last) build.
        :param compare_sha_hash (optional) (str) -> to be provided by github web hook? To be used to ensure latest build is not the recently 
        pushed build.

        Returns tuple -> (json object, latest drone build json object).
        """
        last_build = self.get_latest_build()
        if (compare_sha_hash and compare_sha_hash != last_build['after']) or (not compare_sha_hash):
            return (self.stop_build(last_build['number']), last_build)
        else:
            response = {"message": "Latest (last) build cannot be recently pushed build."}
            return (response, last_build)


if __name__ == "__main__":
    api = Drone(DRONE_SERVER, DRONE_ACCESS_TOKEN, DRONE_REPO_OWNER_USERNAME, DRONE_REPO_NAME)
    print api.get_latest_build()
    print api.stop_latest_build()
