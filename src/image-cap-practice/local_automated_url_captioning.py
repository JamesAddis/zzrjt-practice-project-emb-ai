import glob
import requests
import os
from PIL import Image
from io import BytesIO
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Specify the directory where your images are
image_dir = os.path.join(os.path.dirname(__file__), "local_images")
image_exts = ["jpg", "jpeg", "png"]  # specify the image file extensions to search for
text = "the image of"

# Open a file to write the captions
with open("local_captions.txt", "w") as caption_file:
    for image_ext in image_exts:
        for img_path in glob.glob(os.path.join(image_dir, f"*.{image_ext}")):
            try:
                # Load your image
                raw_image = Image.open(img_path).convert('RGB')

                # You do not need a question for image captioning
                inputs = processor(images=raw_image, text=text, return_tensors="pt")
                # Generate a caption for the image
                outputs = model.generate(**inputs, max_length=50)
                # Decode the generated tokens to text
                caption = processor.decode(outputs[0], skip_special_tokens=True)

                caption_file.write(f"{img_path}: {caption}\n")
            except OSError:
                # Skip images PIL cannot open (SVG, ICO, corrupt files)
                continue
            except Exception as e:
                print(f"[{img_path}] Error: {e}")
                continue