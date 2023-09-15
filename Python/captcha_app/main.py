from PIL import Image
from captcha.image import ImageCaptcha
from io import BytesIO


def main():
    text: str = "Hello"
    captcha: ImageCaptcha = ImageCaptcha(width=400,
                                         height=220,
                                         #fonts=["SF-Pro"],
                                         font_sizes=(80, 70, 100))  # NOA Q

    #captcha.write(text,"sample.png")

    data: BytesIO = captcha.generate(text)

    image: Image = Image.open(data)
    image.show()


if __name__ == '__main__':
    main()