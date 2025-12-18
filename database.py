from supabase import create_client
import supabase
import cv2
from datetime import datetime
import io

bucket_name = 'license_plates'
url = "url"
key = "API_KEY"
supabase = create_client(url,key)
def upload_frame(frame, folder_name, file_prefix = "license_plate"):
    success, encoded_image = cv2.imencode(".jpg", frame)
    if not success:
        raise ValueError("Failed to encode frame")

    img_bytes = io.BytesIO(encoded_image.tobytes())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{file_prefix}_{timestamp}.jpg"
    file_path = f"{folder_name}/{file_name}"

    resp = supabase.storage.from_(bucket_name).update(
    file_path,
    img_bytes.getvalue(),
    {"content-type": "image/jpeg", "upsert": True}
    )
    return True
