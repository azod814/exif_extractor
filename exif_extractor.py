#!/usr/bin/env python3
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from questionary import select, path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Clear terminal screen
def clear_screen():
    os.system("clear")

# Banner (UNCHANGED – same UI)
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
   Kali Linux Tool | Educational Purpose Only
"""

def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_raw = img._getexif()
        if not exif_raw:
            return {}

        exif = {}
        for tag, value in exif_raw.items():
            tag_name = TAGS.get(tag, tag)
            exif[tag_name] = value
        return exif
    except Exception as e:
        return {"Error": str(e)}

def get_gps_info(exif_data):
    gps_info = {}
    if "GPSInfo" in exif_data:
        for key, value in exif_data["GPSInfo"].items():
            gps_tag = GPSTAGS.get(key, key)
            gps_info[gps_tag] = value
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

def print_if_exists(label, value):
    if value:
        print(Fore.GREEN + f"{label:<20}: {value}")

def print_details(exif_data, gps_info, location):
    print(Fore.CYAN + "\n━━━━━━━━━━ IMAGE METADATA ━━━━━━━━━━\n")

    # Camera info
    print_if_exists("Brand", exif_data.get("Make"))
    print_if_exists("Device Model", exif_data.get("Model"))
    print_if_exists("Lens Model", exif_data.get("LensModel"))

    # Camera settings
    print_if_exists("Aperture (FNumber)", exif_data.get("FNumber"))
    print_if_exists("Focal Length", exif_data.get("FocalLength"))
    print_if_exists("Exposure Time", exif_data.get("ExposureTime"))
    print_if_exists("ISO", exif_data.get("ISOSpeedRatings"))
    print_if_exists("Flash", exif_data.get("Flash"))

    # Time info
    print_if_exists("Date Taken", exif_data.get("DateTimeOriginal"))
    print_if_exists("Date Modified", exif_data.get("DateTime"))

    # Software / Editing trace
    print_if_exists("Software", exif_data.get("Software"))

    # GPS info
    if location:
        print(Fore.YELLOW + "\n📍 GPS LOCATION FOUND")
        print(Fore.YELLOW + f"Latitude           : {location['latitude']}")
        print(Fore.YELLOW + f"Longitude          : {location['longitude']}")
        print(Fore.BLUE + "\n🌍 Google Maps Link:")
        print(Fore.BLUE + f"https://www.google.com/maps?q={location['latitude']},{location['longitude']}")
    else:
        print(Fore.RED + "\n❌ GPS Location: Not available")

    print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def main():
    clear_screen()
    print(BANNER)

    action = select(
        "Select an option:",
        choices=[
            "📂 Extract image EXIF details",
            "❌ Exit"
        ]
    ).ask()

    if action == "📂 Extract image EXIF details":
        image_path = path(
            "Select an image file:",
            file_filter=lambda x: x.lower().endswith((".jpg", ".jpeg", ".png")),
            validate=lambda x: os.path.exists(x)
        ).ask()

        exif_data = get_exif_data(image_path)
        gps_info = get_gps_info(exif_data)
        location = get_location(gps_info)
        print_details(exif_data, gps_info, location)

if __name__ == "__main__":
    main()
