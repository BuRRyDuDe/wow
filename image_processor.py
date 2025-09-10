from PIL import Image
import os
import concurrent.futures
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_image(image_path):
    """Обработка отдельного изображения с оптимизацией"""
    try:
        filename = os.path.basename(image_path)
        logger.info(f"Processing image: {filename}")
        
        # Создание WebP версии для быстрой загрузки
        webp_path = image_path.rsplit('.', 1)[0] + '.webp'
        if not os.path.exists(webp_path):
            with Image.open(image_path) as img:
                img.save(webp_path, 'WebP', optimize=True, quality=80)
                logger.info(f"Created WebP version: {os.path.basename(webp_path)}")

        # Создание thumbnail
        thumbnail_path = image_path.rsplit('.', 1)[0] + '_thumb.jpg'
        if not os.path.exists(thumbnail_path):
            with Image.open(image_path) as img:
                img.thumbnail((300, 300))
                img.save(thumbnail_path, 'JPEG', optimize=True, quality=85)
                logger.info(f"Created thumbnail: {os.path.basename(thumbnail_path)}")
                
        return True
    except Exception as e:
        logger.error(f"Error processing {image_path}: {str(e)}")
        return False

def process_uploaded_images():
    """Обработка загруженных изображений с многопоточностью"""
    image_dir = os.environ.get('LABEL_STUDIO_DATA_DIR', '/app/data')
    if not os.path.exists(image_dir):
        logger.warning(f"Image directory {image_dir} does not exist.")
        return
    
    image_files = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(image_dir, filename)
            image_files.append(image_path)
    
    if not image_files:
        logger.info("No images found for processing.")
        return
    
    logger.info(f"Found {len(image_files)} images to process.")
    
    # Многопоточная обработка изображений
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_image, image_files))
    
    success_count = results.count(True)
    logger.info(f"Successfully processed {success_count} out of {len(image_files)} images.")

if __name__ == '__main__':
    logger.info("Starting image processing...")
    process_uploaded_images()
    logger.info("Image processing completed.")