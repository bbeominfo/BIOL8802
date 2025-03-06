import os
import subprocess

class FileManager:
    def __init__(self, remote, localDir, cloudDir):
        self.remote = remote            # name of remote repository (kkim907)
        self.localDir = localDir        # local directory 
        self.cloudDir = cloudDir        # cloud directory 

    def convertLocalToCloud(self, localFilename):
        # Local -> Cloud 
        relativePath = os.path.relpath(localFilename, self.localDir)
        cloudFilename = f"{self.remote}:{self.cloudDir}/{relativePath}"
        return cloudFilename

    def convertCloudToLocal(self, cloudFilename):
        # Cloud -> Local
        if not cloudFilename.startswith(f"{self.remote}:"):
            raise ValueError("Invalid cloud filename format")

        cloudPath = cloudFilename[len(f"{self.remote}:"):]  
        relativePath = os.path.relpath(cloudPath, self.cloudDir)
        localFilename = os.path.join(self.localDir, relativePath)
        return localFilename

    def uploadData(self, localFilename):
        # Files uploading from local to cloud (rclone copy)
        cloudFilename = self.convertLocalToCloud(localFilename)
        cloudFolder = os.path.dirname(cloudFilename)

        cmd = ["rclone", "copy", localFilename, cloudFolder]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Uploaded {localFilename} to {cloudFolder}")
        else:
            print(f"Upload failed: {result.stderr}")

    def downloadData(self, cloudFilename):
        # Filed downloading from cloud to local
        localFilename = self.convertCloudToLocal(cloudFilename)
        localFolder = os.path.dirname(localFilename)

        os.makedirs(localFolder, exist_ok=True)

        cmd = ["rclone", "copy", cloudFilename, localFolder]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Downloaded {cloudFilename} to {localFolder}")
        else:
            print(f"Download failed: {result.stderr}")

if __name__ == "__main__":
    fm = FileManager(
        remote="kkim907",  
        localDir="/Users/bbeominfo/temp",  
        cloudDir="/Kyungbeom Kim/BIOL8802"  
    )

    # for testing
    test_local_file = "/Users/bbeominfo/temp/test.txt"

    # for testing(uploading)
    fm.uploadData(test_local_file)

    # for testing(downloading)
    test_cloud_file = "kkim907:/Kyungbeom Kim/BIOL8802/test.txt"
    fm.downloadData(test_cloud_file)
