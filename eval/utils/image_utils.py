import io
import base64
from PIL import Image

def load_image(image_path):
    """加载图片并转换为RGB格式"""
    try:
        img = Image.open(image_path).convert("RGB")
        return img
    except Exception as e:
        print(f'图片加载失败({image_path}): {str(e)}')
        return None
    
def image_to_base64(image, max_size=1800):
    """将图片转换为base64格式，并可选调整大小以减小数据量"""
    if isinstance(image, str):  # 如果传入的是路径而不是图片对象
        image = load_image(image)
        if image is None:
            return None
    
    # 调整图片大小，保持纵横比
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='JPEG')
    byte_arr = byte_arr.getvalue()
    base64_str = base64.b64encode(byte_arr).decode('utf-8')
    return "data:image/jpeg;base64," + base64_str