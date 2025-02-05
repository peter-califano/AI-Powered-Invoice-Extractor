import os
import json
import time
import requests
from pdf2image import convert_from_path

# 🔹 Imgur API Key (Replace with your valid Client ID)
IMGUR_CLIENT_ID = "YOUR_CLIENT_ID_HERE"

# 🔹 File to store uploaded image URLs (avoids redundant uploads)
imgur_cache_file = "imgur_uploads.json"

# 🔹 Paths
script_dir = os.path.dirname(__file__)
pdf_folder = os.path.join(script_dir, "Invoices")
temp_image_folder = os.path.join(script_dir, "Temp_Images")

# Ensure temp image folder exists
os.makedirs(temp_image_folder, exist_ok=True)

# 🔹 Load existing Imgur uploads if the file exists
if os.path.exists(imgur_cache_file):
    with open(imgur_cache_file, "r", encoding="utf-8") as f: 
        imgur_cache = json.load(f)
else:
    imgur_cache = {} ### Creates cache

def pdf_to_images(pdf_path):
    """Converts each page of a PDF to an image and stores them in a temporary folder."""
    images = convert_from_path(pdf_path) ### converts to images for each page of the pdfs
    
    image_paths = [] ### creating path list
    for i, img in enumerate(images): ### iterates through pdfs 
        img_path = os.path.join(temp_image_folder, f"{os.path.basename(pdf_path)}_page_{i+1}.png") ### code that automatically structures paths for each image
        img.save(img_path, "PNG") ### saves image for each page
        image_paths.append(img_path) ### appends new .png to image_paths

    return image_paths  # Returns a list of image file paths

def upload_to_imgur(image_path, retries=3, delay=5): ### function for uploading to imgur, requires paths, includes variables for retrying and a delay timer
    """Uploads an image to Imgur if it's not already uploaded and returns the public URL."""
    
    # Check if image was already uploaded
    if image_path in imgur_cache: 
        print(f"✅ Skipping upload: Found existing Imgur URL for {image_path}")
        return imgur_cache[image_path]

    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"} ### API header for IMGUR

    for attempt in range(retries): ### API upload attempt with number of retries
        try:
            with open(image_path, "rb") as img_file: ### uploads file to imgur
                response = requests.post(
                    "https://api.imgur.com/3/image",
                    headers=headers,
                    files={"image": img_file},
                    timeout=15
                )

            if response.status_code == 200: ### indicates upload success
                img_url = response.json()["data"]["link"] ### creates response json
                imgur_cache[image_path] = img_url  ### saves url as json
                save_imgur_cache()
                print(f"✅ Uploaded to Imgur: {img_url}")
                return img_url
            else:
                print(f"⚠️ Error {response.status_code}: {response.json()}") 

        except requests.exceptions.ConnectionError as e:
            print(f"⚠️ Connection error on attempt {attempt + 1}: {e}")

        except requests.exceptions.Timeout:
            print(f"⚠️ Timeout error on attempt {attempt + 1}")

        except Exception as e:
            print(f"⚠️ Unexpected error on attempt {attempt + 1}: {e}")

        # Wait before retrying
        time.sleep(delay)

    print("❌ Failed to upload after multiple attempts.")
    return None

def save_imgur_cache(): 
    """Saves the uploaded image URLs to a JSON file to avoid re-uploading."""
    with open(imgur_cache_file, "w", encoding="utf-8") as f:
        json.dump(imgur_cache, f, indent=4)

# 🔹 Process all invoices and upload images to Imgur
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"): ### searches for .pdf files in pdf directory
        print(f"📄 Processing PDF: {filename}") 
        pdf_path = os.path.join(pdf_folder, filename) ### creates path using file name

        # Convert PDF to images
        images = pdf_to_images(pdf_path) ### uses convert to image function

        # Upload images to Imgur and store URLs
        image_urls = [] 
        for img_path in images:
            image_url = upload_to_imgur(img_path)
            if image_url:
                image_urls.append(image_url)

        if image_urls:
            print(f"✅ Uploaded all images for {filename}: {image_urls}")
        else:
            print(f"❌ No images uploaded for {filename}, skipping...")

print("🎉 Finished processing all PDFs!")
