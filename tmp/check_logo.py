from PIL import Image
import os

def check_image(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    bbox = img.getbbox()
    print(f"Size: {w}x{h}")
    print(f"BBox: {bbox}")
    
    # Check edges
    left_edge = all(img.getpixel((0, y))[3] == 0 for y in range(h))
    top_edge = all(img.getpixel((x, 0))[3] == 0 for x in range(w))
    right_edge = all(img.getpixel((w-1, y))[3] == 0 for y in range(h))
    bottom_edge = all(img.getpixel((x, h-1))[3] == 0 for x in range(w))
    
    print(f"Transparent edges: L:{left_edge}, T:{top_edge}, R:{right_edge}, B:{bottom_edge}")

if __name__ == "__main__":
    check_image(r"d:\Sem6 - Copy\static\images\logo.png")
