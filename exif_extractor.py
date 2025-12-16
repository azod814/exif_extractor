#!/usr/bin/env python3
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from questionary import select, path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Clear screen function
def clear_screen():
    os.system("clear")

# Colored ASCII Banner
BANNER = f"""
{Fore.GREEN}
 _______      ___    ___ ___  ________                     
|\  ___ \    |\  \  /  /|\  \|\  _____\                    
\ \   __/|   \ \  \/  / | \  \ \  \__/                     
 \ \  \_|/__  \ \    / / \ \  \ \   __\                    
  \ \  \_|\ \  /     \/   \ \  \ \  \_|                    
   \ \_______\/  /\   \    \ \__\ \__\                     
    \|_______/__/ /\ __\    \|__|\|__|                     
             |__|/ \|__|                                   
{Fore.YELLOW}
   EXIF IMAGE METADATA & GPS EXTRACTOR
{Style.DIM}
   Built for Kali Linux | Educational Purpose Only
"""

def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return {"error": "No EXIF data found."}

        exif = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif[tag_name] = value
        return exif
    except Exception as e:
        return {"error": str(e)}

def get_gps_info(exif_data):
    gps_info = {}
    if "GPSInfo" in exif_data:
        for key in exif_data["GPSInfo"].keys():
            gps_tag = GPSTAGS.get(key, key)
            gps_info[gps_tag] = exif_data["GPSInfo"][key]
        return gps_info
    return None

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def get_location(gps_info):
    if not gps_info:
        return None

    lat = gps_info.get("Latitude")
    lon = gps_info.get("Longitude")
    lat_ref = gps_info.get("LatitudeRef", "N")
    lon_ref = gps_info.get("LongitudeRef", "E")

    if lat and lon:
        lat_deg = convert_to_degrees(lat)
        lon_deg = convert_to_degrees(lon)
        if lat_ref == "S":
            lat_deg = -lat_deg
        if lon_ref == "W":
            lon_deg = -lon_deg
        return {"latitude": lat_deg, "longitude": lon_deg}
    return None

def print_details(exif_data, gps_info, location):
    print(Fore.CYAN + "\n━━━━━━━━━━ IMAGE DETAILS ━━━━━━━━━━\n")

    if "Make" in exif_data:
        print(Fore.GREEN + f"📷 Camera Brand  : {exif_data['Make']}")
    if "Model" in exif_data:
        print(Fore.GREEN + f"📸 Camera Model  : {exif_data['Model']}")
    if "DateTime" in exif_data:
        print(Fore.GREEN + f"🕒 Date Taken    : {exif_data['DateTime']}")

    if location:
        print(Fore.YELLOW + f"\n📍 Location Found")
        print(Fore.YELLOW + f"Latitude  : {location['latitude']}")
        print(Fore.YELLOW + f"Longitude : {location['longitude']}")
        print(Fore.BLUE + f"\n🌐 Google Maps:")
        print(Fore.BLUE + f"https://www.google.com/maps?q={location['latitude']},{location['longitude']}")
    else:
        print(Fore.RED + "\n❌ Location: Not found in EXIF data.")

    print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def main():
    clear_screen()
    print(BANNER)

    action = select(
        "Select an option:",
        choices=[
            "📂 Find details of an image",
            "❌ Exit"
        ]
    ).ask()

    if action == "📂 Find details of an image":
        image_path = path(
            "Select an image file:",
            file_filter=lambda x: x.lower().endswith(('.jpg', '.jpeg', '.png')),
            validate=lambda x: os.path.exists(x)
        ).ask()

        exif_data = get_exif_data(image_path)
        gps_info = get_gps_info(exif_data)
        location = get_location(gps_info)
        print_details(exif_data, gps_info, location)

if __name__ == "__main__":
    main()
