import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the scripts to run in order
scripts = [
    os.path.join(script_dir, "pdf2image-imgur-upload.py"),
    os.path.join(script_dir, "openai_invoice_processing.py"),
    os.path.join(script_dir, "json_to_csv.py")
]

# Run each script sequentially
for script in scripts:
    try:
        logging.info(f"Running {script}...")
        subprocess.run(["python", script], check=True)
        logging.info(f"✅ Successfully completed {script}\n")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error running {script}: {e}")
        break  # Stop execution if any script fails

logging.info("🎉 Data pipeline execution complete!")
