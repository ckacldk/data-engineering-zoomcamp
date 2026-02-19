import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time


# Change this to your bucket name
BUCKET_NAME = "dezoomcamp_hw4_2026_dk"

# If you authenticated through the GCP SDK you can comment out these two lines
CREDENTIALS_FILE = "CREDENTIALS_FILE.json"
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
# If commented initialize client with the following
# client = storage.Client(project='zoomcamp-mod3-datawarehouse')


# Base URL for FHV data from GitHub releases
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_"

# Generate FHV files for 2019 only (12 months)
YEARS_MONTHS = {
    2019: range(1, 13),  # Jan-Dec
}

FILES = [
    f"{year}-{month:02d}.csv.gz"
    for year, months in YEARS_MONTHS.items()
    for month in months
]

DOWNLOAD_DIR = "."
CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)


def download_file(filename):
    url = f"{BASE_URL}{filename}"
    file_path = os.path.join(DOWNLOAD_DIR, f"fhv_tripdata_{filename}")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def check_bucket_exists(bucket_name):
    """Check if bucket exists and is accessible"""
    try:
        bucket = client.get_bucket(bucket_name)
        print(f"✓ Bucket '{bucket_name}' exists and is accessible. Proceeding...")
        return True
    except NotFound:
        print(f"✗ Bucket '{bucket_name}' does not exist.")
        print(f"Please create it manually in GCP Console or use gsutil:")
        print(f"  gsutil mb gs://{bucket_name}")
        sys.exit(1)
    except Forbidden:
        print(f"✗ Bucket '{bucket_name}' exists but you don't have access.")
        print(f"Please grant storage.objects.create permission to your service account.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error checking bucket: {e}")
        sys.exit(1)


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    if file_path is None:
        return
        
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    # Check if bucket exists (don't try to create it)
    check_bucket_exists(BUCKET_NAME)

    print(f"Total files to download: {len(FILES)} (FHV 2019 only)")
    
    # Download files
    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, FILES))

    # Upload to GCS
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, filter(None, file_paths))  # Remove None values

    print("All FHV 2019 files processed and verified.")