import os
from PIL import Image, ImageDraw

def generate_mipmaps():
    src_path = r"C:\Users\ABC\.gemini\antigravity\brain\9a15afa0-cdb7-41da-9e0b-3f682dbdcf76\composited_icon.png"
    master = Image.open(src_path).convert("RGBA")
    w, h = master.size

    # Densities and sizes:
    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192
    }

    base_res = r"c:\Users\ABC\Desktop\Sem 5\MAD\Assignment\MediReminder\app\src\main\res"

    for folder, size in densities.items():
        folder_path = os.path.join(base_res, folder)
        os.makedirs(folder_path, exist_ok=True)

        # 1. Square / Squircle ic_launcher.webp
        # High-res supersampled mask for smooth rounded corners (e.g. radius ~ 22% of size)
        supersample = 4
        ss_size = size * supersample
        resized_master = master.resize((ss_size, ss_size), Image.Resampling.LANCZOS)

        # Rounded rectangle mask for standard launcher icon
        sq_mask = Image.new("L", (ss_size, ss_size), 0)
        sq_draw = ImageDraw.Draw(sq_mask)
        radius = int(ss_size * 0.22)
        sq_draw.rounded_rectangle([0, 0, ss_size - 1, ss_size - 1], radius=radius, fill=255)

        sq_icon = Image.new("RGBA", (ss_size, ss_size), (0, 0, 0, 0))
        sq_icon.paste(resized_master, (0, 0), sq_mask)
        final_sq = sq_icon.resize((size, size), Image.Resampling.LANCZOS)
        
        sq_dest = os.path.join(folder_path, "ic_launcher.webp")
        final_sq.save(sq_dest, format="WEBP", quality=95)
        print(f"Generated {sq_dest} ({size}x{size})")

        # 2. Circular ic_launcher_round.webp
        circ_mask = Image.new("L", (ss_size, ss_size), 0)
        circ_draw = ImageDraw.Draw(circ_mask)
        circ_draw.ellipse([0, 0, ss_size - 1, ss_size - 1], fill=255)

        circ_icon = Image.new("RGBA", (ss_size, ss_size), (0, 0, 0, 0))
        circ_icon.paste(resized_master, (0, 0), circ_mask)
        final_circ = circ_icon.resize((size, size), Image.Resampling.LANCZOS)

        circ_dest = os.path.join(folder_path, "ic_launcher_round.webp")
        final_circ.save(circ_dest, format="WEBP", quality=95)
        print(f"Generated {circ_dest} ({size}x{size})")

    # Also save a 512x512 high-res version in drawable for in-app or Play Store use
    hi_res = master.resize((512, 512), Image.Resampling.LANCZOS)
    hi_res_dest = os.path.join(base_res, "drawable", "ic_app_logo.png")
    hi_res.save(hi_res_dest, format="PNG")
    print(f"Generated {hi_res_dest} (512x512)")

if __name__ == "__main__":
    generate_mipmaps()
