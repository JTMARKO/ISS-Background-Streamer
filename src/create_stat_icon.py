from PIL import Image, ImageDraw, ImageFont


def create_half_circle_outline(
    size=(400, 200), outline_color=(255, 0, 0), outline_width=5, amount=1
):

    image = Image.new("RGBA", size, (0, 0, 0, 0))

    draw = ImageDraw.Draw(image)

    left = 0
    top = 0
    right = size[0]
    bottom = size[1] * 2

    draw.arc(
        [left, top, right, bottom],
        180,
        180 * amount + 180,
        fill=outline_color,
        width=outline_width,
    )

    return image


def create_percent_filled_half_circle(
    size=(400, 200),
    outline_color=(255, 0, 0),
    outline_widths=(2, 5),
    amount=0.2,
    tic_extension=5,
):

    outter_arc = create_half_circle_outline(
        size, outline_color, outline_widths[1], amount
    )
    width_diff = outline_widths[1] - outline_widths[0]
    inner_size = (size[0] - width_diff, size[1] - width_diff // 2)

    inner_arc = create_half_circle_outline(inner_size, outline_color, outline_widths[0])
    outter_arc.paste(inner_arc, (width_diff // 2, width_diff // 2), inner_arc)

    tic_size = (size[0], size[1] + width_diff // 2)

    tic_marks = Image.new("RGBA", tic_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(tic_marks)

    draw.rectangle(
        [
            0,
            tic_size[1] - outline_widths[0],
            outline_widths[1] + tic_extension,
            tic_size[1],
        ],
        fill=outline_color,
    )

    draw.rectangle(
        [
            tic_size[0] - outline_widths[1] - tic_extension,
            tic_size[1] - outline_widths[0],
            tic_size[0],
            tic_size[1],
        ],
        fill=outline_color,
    )

    tic_marks.paste(outter_arc, (0, 0), outter_arc)

    return tic_marks


def create_stat_with_text(
    size=(400, 200),
    outline_color=(255, 0, 0),
    outline_widths=(2, 5),
    amount=0.2,
    tic_extension=5,
    text="",
    font=None,
    stat_font=None,
):

    stat = create_percent_filled_half_circle(
        (size[0] * 2, size[1] * 2),
        outline_color,
        (outline_widths[0] * 2, outline_widths[1] * 2),
        amount,
        tic_extension * 2,
    )

    height_diff = outline_widths[1] - outline_widths[0]
    height_diff //= 2

    stat = stat.resize((size[0], size[1] + height_diff), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(stat)

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_position = ((size[0] - text_width) // 2, (size[1] - text_height) - 10)

    draw.text(text_position, text, fill=outline_color, font=font)

    percentage_text = f"{amount*100:.2f}%"

    percentage_bbox = draw.textbbox((0, 0), percentage_text, font=stat_font)
    percentage_width = percentage_bbox[2] - percentage_bbox[0]
    percentage_height = percentage_bbox[3] - percentage_bbox[1]

    percentage_position = (
        (size[0] - percentage_width) // 2,
        (size[1] - percentage_height) // 2,
    )

    draw.text(percentage_position, percentage_text, fill=outline_color, font=stat_font)

    return stat


def paste_stat(background, image, position):
    """
    Paste a smaller image onto a larger image at a specific position.

    Parameters:
    image_path (str): Path to the larger image
    image (PIL.Image): Image object to paste onto the larger image
    position (tuple): x and y percentages to paste the image

    Returns:
    PIL.Image: Image object with the smaller image pasted onto the larger image
    """

    background_size = background.size

    paste_position = (
        int(background_size[0] * position[0]),
        int(background_size[1] * position[1]),
    )

    background.paste(image, paste_position, image)

    return background


def main():

    font = ImageFont.truetype("/home/jt/.fonts/ttf/CascadiaCode.ttf", 15)
    stat_font = ImageFont.truetype("/home/jt/.fonts/ttf/CascadiaCode.ttf", 20)

    stat = create_stat_with_text(
        size=(200, 100),
        outline_color="#E7D7AD",
        outline_widths=(4, 20),
        amount=0.8,
        tic_extension=0,
        text="Urine Tank Qty",
        font=font,
        stat_font=stat_font,
    )

    # pass

    dir = "/home/jt/Pictures/Backgrounds/"
    background = "second_iss_#282828_#458588_#E7D7AD_2.png"

    image_path = dir + background

    background = Image.open(image_path)

    paste_stat(background, stat, (0.8, 0.8)).show()


if __name__ == "__main__":
    main()
