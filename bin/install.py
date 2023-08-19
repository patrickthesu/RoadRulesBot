import subprocess
import sys


def makeInstall(packages: list):
    for package in packages:
        try: 
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as err:
            print (err)

if __name__ == "__main__":
    makeInstall (open("deps").read().strip().split("\n"))
