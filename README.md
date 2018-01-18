# Image Resizer

Creates resized image

# How to install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# How to use

```bash
usage: image_resize.py [-h] [--origin ORIGIN] [--height HEIGHT]
                       [--width WIDTH] [--scale SCALE] [--result RESULT]

Сжатие изображения.

optional arguments:
  -h, --help            show this help message and exit
  --origin ORIGIN, -o ORIGIN
                        path to original image (default:origin.jpg)
  --width WIDTH, -w WIDTH
                        width of result image in px
  --height HEIGHT, -he HEIGHT
                        height of result image ix px
  --scale SCALE, -s SCALE
                        scale multiplier (default:1)
  --result RESULT, -r RESULT
                        path to result image (default: None)
```

Example:
```bash
python image_resize.py -w 200
Исходный файл: C:\Users\NaWashington\PycharmProjects\12_image_resize\origin.jpg JPEG 2560x1700
Готово:
C:\Users\NaWashington\PycharmProjects\12_image_resize\origin__200x133.jpg
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
