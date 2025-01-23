#!/usr/bin/env python3


from streamer import ISSListener
from create_stat_icon import create_stat_with_text, paste_stat
from PIL import ImageFont, Image

import subprocess
import time
import os

BACKGROUND_IMG = "second_iss_#282828_#458588_#E7D7AD_2.png"
FONT = "CascadiaCode.ttf"
SLEEP_TIME_SECONDS = 4
TMP_PATH = "/tmp/temp_wallpaper.png"


def create_wallpaper(font, stat_font, background, amount, position, text, color):

    icon = create_stat_with_text(
        size=(200, 100),
        outline_color=color,
        outline_widths=(2, 20),
        amount=amount,
        tic_extension=4,
        text=text,
        font=font,
        stat_font=stat_font,
    )

    background = paste_stat(background, icon, position)

    return background


def set_wallpaper(file_path=TMP_PATH):
    subprocess.run(
        [
            # "dbus-launch",
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri-dark",
            # "file:///tmp/temp_wallpaper.png",
            # f"file://{file_path}",
            file_path,
        ]
    )


def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.dirname(script_dir)

    background_path = os.path.join(script_dir, "background", BACKGROUND_IMG)

    font_path = os.path.join(script_dir, "fonts", FONT)

    font = ImageFont.truetype(font_path, 15)
    stat_font = ImageFont.truetype(font_path, 20)

    listener = ISSListener()

    last_urine, last_clean, last_waste = float("inf"), float("inf"), float("inf")

    while True:

        urine, clean, waste = listener.get_latest_value()
        print(urine, clean, waste)

        # Checks if the listener is disconnected
        if None in (urine, clean, waste):
            set_wallpaper(background_path)
            time.sleep(SLEEP_TIME_SECONDS)
            continue

        # Saves a re-write of the same image
        stat_similarities = [
            f"{stat:.2f}" == f"{last_stat:.2f}"
            for stat, last_stat in zip(
                (urine, clean, waste), (last_urine, last_clean, last_waste)
            )
        ]

        if all(stat_similarities):
            time.sleep(SLEEP_TIME_SECONDS)
            continue

        urine /= 100
        clean /= 100
        waste /= 100

        background = Image.open(background_path)

        recent_urine_increase, recent_clean_increase, recent_waste_increase = (
            listener.get_recent_increases()
        )

        for stat, pos, recent_increase, text in [
            (urine, (0.85, 0.75), recent_urine_increase, "Urine Tank Qty"),
            (clean, (0.7, 0.75), recent_clean_increase, "Clean Water Qty"),
            (waste, (0.85, 0.6), recent_waste_increase, "Waste Water Qty"),
        ]:

            color = "#458588" if recent_increase else "#E7D7AD"

            background = create_wallpaper(
                font,
                stat_font,
                background,
                stat,
                pos,
                text,
                color,
            )

        last_urine, last_clean, last_waste = urine, clean, waste

        background.save(TMP_PATH)
        set_wallpaper()
        time.sleep(SLEEP_TIME_SECONDS)


if __name__ == "__main__":
    main()
