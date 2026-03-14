from PIL import Image
import os

def surgical_crop(path, threshold=30):
    if not os.path.exists(path):
        return "File not found"
    
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    
    left, top, right, bottom = w, h, 0, 0
    found = False
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = img.getpixel((x, y))
            brightness = (r + g + b) / 3
            if brightness > threshold:
                found = True
                if x < left: left = x
                if y < top: top = y
                if x > right: right = x
                if y > bottom: bottom = y
    
    if found:
        # Tightly crop content (no padding for "fully splash" look)
        cropped = img.crop((left, top, right, bottom))
        res = f"Tight Crop ({threshold}): {cropped.size} from {img.size} (L:{left}, T:{top}, R:{right}, B:{bottom})"
        cropped.save(path)
        return res
    else:
        return "No content found"

if __name__ == "__main__":
    result = surgical_crop(r"d:\Sem6 - Copy\static\images\logo.png")
    with open(r"d:\Sem6 - Copy\crop_result.txt", "w") as f:
        f.write(result)
