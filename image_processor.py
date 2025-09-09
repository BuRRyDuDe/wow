from PIL import Image
import os

def process_uploaded_images():
    """Обработка загруженных изображений"""
    image_dir = os.environ.get('LABEL_STUDIO_DATA_DIR', '/app/data')
    if not os.path.exists(image_dir):
        print(f"Image directory {image_dir} does not exist.")
        return
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(image_dir, filename)

            # Создание WebP версии для быстрой загрузки
            webp_path = image_path.rsplit('.', 1)[0] + '.webp'
            with Image.open(image_path) as img:
                img.save(webp_path, 'WebP', optimize=True, quality=80)

            # Создание thumbnail
            thumbnail_path = image_path.rsplit('.', 1)[0] + '_thumb.jpg'
            with Image.open(image_path) as img:
                img.thumbnail((300, 300))
                img.save(thumbnail_path, 'JPEG', optimize=True, quality=85)

if __name__ == '__main__':
    process_uploaded_images()