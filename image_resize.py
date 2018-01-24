from PIL import Image
from argparse import ArgumentParser

from os.path import splitext


def parse_args():
    parser = ArgumentParser(description='Сжатие изображения.')
    parser.add_argument(
        '--origin',
        '-o',
        type=str,
        help='Путь к исходному изображению',
        required=True
    )
    parser.add_argument(
        '--height',
        '-H',
        type=int,
        default=None,
        help='Ширина результирующего изображения'
    )
    parser.add_argument(
        '--width',
        '-w',
        type=int,
        default=None,
        help='Высота результирующего изображения'
    )
    parser.add_argument(
        '--scale',
        '-s',
        type=float,
        default=1,
        help='Множитель размера изображения'
    )
    parser.add_argument(
        '--result',
        '-r',
        type=str,
        default=None,
        help='Путь к изображению результату'
    )
    return parser.parse_args()


def get_original_image(image_path):
    try:
        return Image.open(image_path)
    except IOError:
        return None


def get_new_size_by_width(size_format, width):
    return width, round(width / size_format)


def get_new_size_by_height(size_format, height):
    return round(height * size_format), height


def scale_size(scale, original_image_size):
    width, height = original_image_size
    return round(width * scale), round(height * scale)


def get_new_size(original_image_size, width, height, scale):
    origin_width, origin_height = original_image_size
    size_format = origin_width / origin_height

    if scale != 1:
        return scale_size(scale, original_image_size)

    if width and height:
        print('Пропорции изображения могут быть искажены')
        return width, height
    elif width:
        return get_new_size_by_width(size_format, width)
    else:
        return get_new_size_by_height(size_format, height)


def resize_image(original_image, new_size):
    return original_image.resize(new_size)


def get_result_filename(origin_path, new_size):
    origin_image_path, origin_image_ext = splitext(origin_path)
    width, height = new_size

    return '{name}__{width}x{height}{ext}'.format(
        name=origin_image_path,
        width=width,
        height=height,
        ext=origin_image_ext
    )


def save_image(resized_image, original_image_path, result_path):
    if result_path:
        result_image_path = result_path
    else:
        new_size = resized_image.size
        result_image_path = get_result_filename(original_image_path, new_size)
    resized_image.save(result_image_path, resized_image.format)
    return result_image_path


if __name__ == '__main__':
    args = parse_args()

    if args.scale != 1 and (args.width or args.height):
        exit('Ошибка: Запрещено задавать увеличение вместе с размерами')

    if args.scale == 1 and not (args.width or args.height):
        exit('Ошибка: Увеличение и размеры не заданы')

    original_image = get_original_image(args.origin)
    if original_image is None:
        exit(
            'Не найдено исходное изображение или файл не является изображением'
        )

    new_size = get_new_size(
        original_image.size,
        args.width,
        args.height,
        args.scale
    )

    resized_image = resize_image(original_image, new_size)

    result_image_path = save_image(resized_image, args.origin, args.result)

    print('Готово:\n{}'.format(result_image_path))
