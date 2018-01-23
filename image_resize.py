from PIL import Image
import argparse

from os.path import join, split, splitext


def parse_args():
    parser = argparse.ArgumentParser(
        description='Сжатие изображения.'
    )
    required_paramss = parser.add_argument_group('Обязательные аргументы')
    required_paramss.add_argument(
        '--origin',
        '-o',
        type=str,
        help='Путь к исходному изображению',
        required=True
    )
    parser.add_argument(
        '--height',
        '-e',
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
        original_image = Image.open(image_path)
    except IOError:
        return None
    return original_image


def get_new_size_by_width(size_format, width):
    return width, round(width / size_format)


def get_new_size_by_height(size_format, height):
    return round(height * size_format), height


def scale_size(scale, size):
    width, height = size
    return round(width * scale), round(height * scale)


def get_new_size(origin_size, width, height):
    origin_width, origin_height = origin_size
    size_format = origin_width / origin_height

    if width and height:
        print('Пропорции изображения могут быть искажены')
        return width, height
    elif width:
        return get_new_size_by_width(size_format, width)
    elif height:
        return get_new_size_by_height(size_format, height)
    else:
        return None


def get_result_filename(origin_path, new_size):
    origin_image_path, origin_image_ext = splitext(origin_path)
    width, height = new_size

    return '{name}__{width}x{height}{ext}'.format(
        name=origin_image_path,
        width=width,
        height=height,
        ext=origin_image_ext
    )


def resize_image(original_image, result_path, new_size):
    try:
        original_image.resize(new_size)
        original_image.save(result_path)
    except IOError:
        return False
    else:
        return True


if __name__ == '__main__':
    args = parse_args()

    original_image = get_original_image(args.origin)
    if original_image is None:
        exit(
            'Не найдено исходное изображение или файл не является изображением'
        )

    if args.scale != 1:
        if args.width and args.height:
            exit('Ошибка: Запрещено задавать увеличение вместе с размерами')
        else:
            new_size = scale_size(args.scale, original_image.size)

    else:
        if not (args.width or args.height):
            exit('Ошибка: Увеличение и размеры не заданы')
        else:
            new_size = get_new_size(
                original_image.size,
                args.width,
                args.height
            )

    if args.result:
        result_image_path = args.result
    else:
        result_image_path = get_result_filename(args.origin, new_size)

    if not resize_image(original_image, result_image_path, new_size):
        exit('Не удалось изменить размер файла {}'.format(args.origin))
    else:
        print('Готово:\n{}'.format(result_image_path))
