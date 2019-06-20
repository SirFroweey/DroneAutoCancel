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

    def perform_sha_hash_check(self, compare_sha_hash, amount_to_check=2):
        previous_build = {}
        builds = self.get_builds()
        for index in range(amount_to_check):
            previous_build = builds[index]
            if (compare_sha_hash and compare_sha_hash != previous_build['after']) or (not compare_sha_hash):
                return (self.stop_build(previous_build['number']), previous_build)
        response = {"message": "The given previous build cannot be the recently pushed Drone build we are attempting to stop."}
        return (response, previous_build)

    def stop_latest_build(self, compare_sha_hash=None):
        """
        Stop latest (last) build. Iterates through build feed and finds recent 'running' builds and stops them.
        :param compare_sha_hash (optional) (str) -> to be provided by github web hook? To be used to ensure latest build is not the recently 
        pushed build.

        Returns tuple -> (json object, latest drone build json object).
        """
        result = self.perform_sha_hash_check(compare_sha_hash, 2)
        return result

if __name__ == "__main__":
    api = Drone(DRONE_SERVER, DRONE_ACCESS_TOKEN, DRONE_REPO_OWNER_USERNAME, DRONE_REPO_NAME)
    print api.get_latest_build()
    print api.stop_latest_build()
