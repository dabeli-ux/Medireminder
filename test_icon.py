import math
from PIL import Image, ImageDraw, ImageFilter

def create_preview_icon():
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Background: Deep rich gradient from #131131 to #2A2468
    for y in range(size):
        ratio = y / size
        r = int(21 * (1 - ratio) + 49 * ratio)
        g = int(16 * (1 - ratio) + 46 * ratio)
        b = int(59 * (1 - ratio) + 129 * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Add subtle radial glow at top-left
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([size * 0.1, size * 0.05, size * 0.7, size * 0.65], fill=(99, 102, 241, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img = Image.alpha_composite(img, glow)

    # Foreground elements:
    fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(fg)

    # Reminder Clock / Bell Arc in top-right
    arc_box = [size * 0.32, size * 0.18, size * 0.84, size * 0.70]
    fdraw.arc(arc_box, start=270, end=75, fill=(165, 180, 252, 190), width=int(size * 0.035))
    
    # Bell hammer at top of bell arc
    bx, by = size * 0.68, size * 0.18
    fdraw.ellipse([bx - size * 0.035, by - size * 0.035, bx + size * 0.035, by + size * 0.035], fill=(255, 255, 255, 220))
    
    # Small notification pulse dot
    px, py = size * 0.81, size * 0.35
    fdraw.ellipse([px - size * 0.02, py - size * 0.02, px + size * 0.02, py + size * 0.02], fill=(56, 189, 248, 240))

    # Draw Pill
    pw = int(size * 0.25)
    ph = int(size * 0.56)
    pr = pw // 2

    cx, cy = size // 2, size // 2
    px0 = cx - pw // 2
    px1 = cx + pw // 2
    py0 = cy - ph // 2
    py1 = cy + ph // 2
    split_y = cy

    top_mask = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    tmdraw = ImageDraw.Draw(top_mask)
    tmdraw.rounded_rectangle([px0, py0, px1, split_y + 10], radius=pr, fill=(16, 185, 129, 255))
    tmdraw.rectangle([0, split_y, size, size], fill=(0, 0, 0, 0))

    bot_mask = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bmdraw = ImageDraw.Draw(bot_mask)
    bmdraw.rounded_rectangle([px0, split_y - 10, px1, py1], radius=pr, fill=(248, 250, 252, 255))
    bmdraw.rectangle([0, 0, size, split_y], fill=(0, 0, 0, 0))

    # Pill shadow underneath
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([px0, py0, px1, py1], radius=pr, fill=(0, 0, 0, 100))
    shadow = shadow.rotate(-38, center=(cx, cy), resample=Image.BICUBIC)
    shadow_offset = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow_offset.paste(shadow, (int(size * 0.03), int(size * 0.05)), shadow)
    shadow_blur = shadow_offset.filter(ImageFilter.GaussianBlur(15))

    pill_combined = Image.alpha_composite(top_mask, bot_mask)

    pcdraw = ImageDraw.Draw(pill_combined)
    pcdraw.line([(px0, split_y), (px1, split_y)], fill=(15, 23, 42, 60), width=4)

    # Specular gloss highlight on top-left of pill
    gloss = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gldraw = ImageDraw.Draw(gloss)
    gl_w = int(pw * 0.22)
    gl_h = int(ph * 0.32)
    gldraw.rounded_rectangle([px0 + int(pw * 0.16), py0 + int(pw * 0.25), px0 + int(pw * 0.16) + gl_w, py0 + int(pw * 0.25) + gl_h], radius=gl_w // 2, fill=(255, 255, 255, 140))
    pill_combined = Image.alpha_composite(pill_combined, gloss)

    # Medical cross in center
    cw = int(pw * 0.65)
    ct = int(cw * 0.34)
    pcdraw.rounded_rectangle([cx - cw // 2, cy - ct // 2, cx + cw // 2, cy + ct // 2], radius=ct // 3, fill=(255, 255, 255, 255))
    pcdraw.rounded_rectangle([cx - ct // 2, cy - cw // 2, cx + ct // 2, cy + cw // 2], radius=ct // 3, fill=(255, 255, 255, 255))

    rotated_pill = pill_combined.rotate(-38, center=(cx, cy), resample=Image.BICUBIC)

    img = Image.alpha_composite(img, shadow_blur)
    img = Image.alpha_composite(img, fg)
    img = Image.alpha_composite(img, rotated_pill)

    img.save(r"C:\Users\ABC\.gemini\antigravity\brain\9a15afa0-cdb7-41da-9e0b-3f682dbdcf76\preview_icon.png")
    print("Saved preview_icon.png successfully")

if __name__ == "__main__":
    create_preview_icon()
