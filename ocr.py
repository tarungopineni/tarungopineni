import easyocr

def detect_license_plate_text(img):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img)
    if result:
        if result[0]:
            if result[0][1]:
                return result[0][1]
