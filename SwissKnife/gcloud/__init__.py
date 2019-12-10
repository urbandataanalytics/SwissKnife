import sys

try:
    import google
except ModuleNotFoundError:
    print("ERROR: You need install SwissKnife with 'gcloud' tag.")
    sys.exit(-1)
