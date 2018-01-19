from PIL import Image
import argparse

from os.path import realpath, join, split, splitext
from sys import stderr


def get_original_image(image_path):
    try:
        origin = Image.open(image_path)
    except IOError:
        print(
            "Не найдено исходное изображение или файл не является "
            "изображением",
            file=stderr
        )
        return None
    print(
        "Исходный файл:",
        realpath(image_path),
        origin.format,
        "{}x{}".format(origin.size[width], origin.size[height])
    )
    return origin


def get_new_size_by_one_side(size_format, width, height):
    if width:
        height = round(width / size_format)
    elif height:
        width = round(height * size_format)
    else:
        return None

    return width, height


def scale_size(scale, size):
    return round(size[0] * scale), round(size[1] * scale)


def get_new_size(origin, scale, width, height):
    width_key, height_key = 0, 1
    size_format = origin.size[width_key] / origin.size[height_key]
    default_scale = 1

    if scale == default_scale:
        if width and height:
            print("Пропорции изображения могут быть искажениы")
            return width, height
        elif width or height:
            return get_new_size_by_one_side(size_format, width, height)
        else:
            print("Ошибка: Увеличение и размеры не заданы", file=stderr)
    else:
        if width or height:
            print(
                "Ошибка: Запрещено задавать увеличение вместе с размерами",
                file=stderr
            )

        return scale_size(scale, origin.size)

    return None


def get_result_filename(origin, new_size):
    origin_path = realpath(origin)
    origin_dirpath, origin_filename = split(origin_path)
    origin_filename_root, origin_filename_ext = splitext(origin_filename)
    width, height = 0, 1
    return join(
        origin_dirpath,
        "{}__{}x{}{}".format(
            origin_filename_root,
            new_size[width],
            new_size[height],
            origin_filename_ext
        )
    )


def resize_image(original_path, result_path, new_size):
    try:
        image = Image.open(original_path)
        image.thumbnail(new_size)
        image.save(result_path)
    except IOError:
        print(
            "Не удалось изменить размер файла {}".format(original_path),
            file=stderr
        )
        return False
    else:
        print("Готово:\n{}".format(result_path))
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Сжатие изображения.')
    parser.add_argument(
        "--origin",
        "-o",
        type=str,
        default='origin.jpg',
        help="Путь к исходному изображению"
    )
    parser.add_argument(
        "--height",
        "-he",
        type=int,
        default=None,
        help="Ширина результирующего изображения"
    )
    parser.add_argument(
        "--width",
        "-w",
        type=int,
        default=None,
        help="Высота результирующего изображения"
    )
    parser.add_argument(
        "--scale",
        "-s",
        type=int,
        default=1,
        help="Множитель увеличения изображения"
    )
    parser.add_argument(
        "--result",
        "-r",
        type=str,
        default=None,
        help="Путь к результирующему изображению"
    )
    width, height = 0, 1
    args = parser.parse_args()

    origin = get_original_image(args.origin)
    if origin is None:
        exit(1)

    new_size = get_new_size(origin, args.scale, args.width, args.height)

    if new_size is None:
        exit(1)

    if args.result:
        result_path = realpath(args.result)
    else:
        result_path = get_result_filename(args.origin, new_size)

    if not resize_image(args.origin, result_path, new_size):
        exit(1)
