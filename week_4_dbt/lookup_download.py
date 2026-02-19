import urllib.request
import os

# URL for the Taxi Zone Lookup Table
URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

# Download directory (current directory)
DOWNLOAD_DIR = "."
FILE_NAME = "taxi_zone_lookup.csv"

# Create full file path
file_path = os.path.join(DOWNLOAD_DIR, FILE_NAME)

try:
    print(f"Downloading {URL}...")
    urllib.request.urlretrieve(URL, file_path)
    print(f"Downloaded successfully: {file_path}")
    
    # Show file size
    file_size = os.path.getsize(file_path)
    print(f"📊 File size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
    
    # Show first few lines
    print("\n📄 First 5 lines of the file:")
    print("-" * 50)
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if i < 5:
                print(line.strip())
            else:
                break

except Exception as e:
    print(f"error: {e}")