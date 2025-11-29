#!/usr/bin/env python3
import os
import json
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from inquirer import prompt, List, Path

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
    print("\n--- Image Details ---")
    if "Make" in exif_data:
        print(f"Camera Brand: {exif_data['Make']}")
    if "Model" in exif_data:
        print(f"Camera Model: {exif_data['Model']}")
    if "DateTime" in exif_data:
        print(f"Date Taken: {exif_data['DateTime']}")
    if location:
        print(f"Location (Latitude, Longitude): {location['latitude']}, {location['longitude']}")
        print(f"Google Maps Link: https://www.google.com/maps?q={location['latitude']},{location['longitude']}")
    else:
        print("Location: Not found in EXIF data.")
    print("----------------------\n")

def main():
    questions = [
        List(
            "action",
            message="What do you want to do?",
            choices=["Find details of an image", "Exit"]
        ),
        Path(
            "image_path",
            message="Select an image file:",
            path_type="file",
            validate=lambda _, x: os.path.exists(x),
            when=lambda x: x["action"] == "Find details of an image"
        )
    ]

    answers = prompt(questions)
    if answers["action"] == "Find details of an image":
        exif_data = get_exif_data(answers["image_path"])
        gps_info = get_gps_info(exif_data)
        location = get_location(gps_info)
        print_details(exif_data, gps_info, location)

if __name__ == "__main__":
    main()
