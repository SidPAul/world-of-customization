from PIL import Image
import os

def extract_butterfly(path, out_path):
    if not os.path.exists(path):
        print("File not found")
        return
    
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    
    # We want to separate the butterfly from the text.
    # We can scan from left to right, looking for a column of transparent pixels
    # that separates the butterfly from the text.
    
    # Butterfly is on the left.
    transparent_col = -1
    for x in range(w):
        is_transparent = True
        for y in range(h):
            if img.getpixel((x, y))[3] > 0:
                is_transparent = False
                break
        
        # If we find a transparent col after some non-transparent cols, it's the gap
        if is_transparent and x > int(w * 0.1): # Ensure we passed the left edge of butterfly
            transparent_col = x
            break
            
    if transparent_col != -1:
        butterfly = img.crop((0, 0, transparent_col, h))
        # Tight crop butterfly
        bbox = butterfly.getbbox()
        if bbox:
            butterfly = butterfly.crop(bbox)
        butterfly.save(out_path)
        print(f"Extracted butterfly to {out_path}, size {butterfly.size}")
    else:
        # If no gap found, maybe just crop left 30%
        butterfly = img.crop((0, 0, int(w * 0.35), h))
        butterfly = butterfly.crop(butterfly.getbbox())
        butterfly.save(out_path)
        print(f"Fallback extracted butterfly to {out_path}, size {butterfly.size}")

if __name__ == "__main__":
    extract_butterfly(r"d:\Sem6 - Copy\static\images\logo.png", r"d:\Sem6 - Copy\static\images\butterfly_logo.png")
