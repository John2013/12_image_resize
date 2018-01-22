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
        original_file = Image.open(image_path)
    except IOError:
        return None
    return original_file


def get_new_size_by_width(size_format, width):
    return width, round(width / size_format)


def get_new_size_by_height(size_format, height):
    return round(height * size_format), height


def scale_size(scale, size):
    width_key, height_key = 0, 1
    return round(size[width_key] * scale), round(size[height_key] * scale)


def get_new_size(origin_size, scale, width, height):
    width_key, height_key = 0, 1
    size_format = origin_size[width_key] / origin_size[height_key]

    if scale == 1:
        if width and height:
            print('Пропорции изображения могут быть искажены')
            return width, height
        elif width:
            return get_new_size_by_width(size_format, width)
        elif height:
            return get_new_size_by_height(size_format, height)
        else:
            return None
    elif width or height:
        return None
    else:
        return scale_size(scale, origin_size)


def get_result_filename(origin_path, new_size, result_file_name):
    if result_file_name:
        return result_file_name

    origin_dirpath, origin_filename = split(origin_path)
    origin_filename_root, origin_filename_ext = splitext(origin_filename)
    width_key, height_key = 0, 1

    return join(
        origin_dirpath,
        '{name}__{width}x{height}{ext}'.format(
            name=origin_filename_root,
            width=new_size[width_key],
            height=new_size[height_key],
            ext=origin_filename_ext
        )
    )


def resize_image(original_path, result_path, new_size):
    try:
        image = Image.open(original_path)
        image.thumbnail(new_size)
        image.save(result_path)
    except IOError:
        return False
    else:
        return True


if __name__ == '__main__':
    args = parse_args()
    width_key, height_key = 0, 1

    original_file = get_original_image(args.origin)
    if original_file is None:
        exit(
            'Не найдено исходное изображение или файл не является изображением'
        )

    if args.scale != 1 and args.width and args.height:
        exit('Ошибка: Запрещено задавать увеличение вместе с размерами')
    elif args.scale == 1 and not (args.width or args.height):
        exit('Ошибка: Увеличение и размеры не заданы')

    new_size = get_new_size(
        original_file.size,
        args.scale,
        args.width,
        args.height
    )

    result_file_path = get_result_filename(args.origin, new_size, args.result)

    if not resize_image(args.origin, result_file_path, new_size):
        exit('Не удалось изменить размер файла {}'.format(args.origin))
    else:
        print('Готово:\n{}'.format(result_file_path))
