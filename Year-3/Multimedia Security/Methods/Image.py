import cv2
import pywt
import numpy as np
from PIL import Image

def str_to_bitarray(text: str) -> np.ndarray:
    return np.array([int(bit) for char in text.encode('utf-8') for bit in format(char, '08b')], dtype=np.float32)

def bitarray_to_str(bit_array: np.ndarray) -> str:
    return bytes(
        bytearray(
            [int(''.join(str(int(b)) for b in bit_array[i:i+8]), 2) for i in range(0, len(bit_array), 8)]
        )
    ).decode('utf-8', errors='ignore')

def binarize(image_pil: Image.Image, threshold: int, mode:str) -> Image.Image:
    return Image.fromarray((np.array(image_pil.convert('L')) > threshold).astype(np.uint8) * 255, mode='L').convert(mode)

def apply_geometric_attacks(image_pil: Image.Image, params: dict) -> Image.Image:
    image = np.array(image_pil)
    if image.ndim == 2:
        pass
    else:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 1. SCALE
    if (scale_factor := params.get('Scale', 1.0)) != 1.0:
        image = cv2.resize(
            src=image,
            dsize=(int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor)),
            interpolation=cv2.INTER_LINEAR
        )

    # 2. ROTATE
    if (rotate_angle := params.get('Rotate', 0)) != 0:
        h, w = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), rotate_angle, 1.0)
        image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    # 3. RESIZE
    if (resize_dims := params.get('Resize', {})):
        if (w := resize_dims.get('width')) and (h := resize_dims.get('height')):
            image = cv2.resize(image, (w, resize_dims.get('height')), interpolation=cv2.INTER_AREA)

    # 4. CROP
    if (crop := params.get('Crop', {})):
        h, w = image.shape[:2]
        sx = int(w * crop.get('start_x', 0) / 100)
        sy = int(h * crop.get('start_y', 0) / 100)
        ex = sx + int(w * crop.get('end_x', 100) / 100)
        ey = sy + int(h * crop.get('end_y', 100) / 100)

        if sx < ex and sy < ey:
            image = image[sy:ey, sx:ex]

    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def apply_text_watermark(image_pil: Image.Image, params: dict) -> Image.Image:
    image = cv2.cvtColor(np.array(image_pil.convert('RGB')), cv2.COLOR_RGB2BGR)

    h, w = image.shape[:2]
    x = int((params.get('X', 10) / 100) * w)
    y = int((params.get('Y', 10) / 100) * h)

    color = params.get('Color', (255, 255, 255))
    if image_pil.mode not in ('RGB', 'RGBA'):
        avg = int(sum(color) / 3)
        color = (avg, avg, avg)

    cv2.putText(
        image, params.get('Text', 'Watermark'), (x, y),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale= 0.5 + (params.get('Size', 1) - 1) * 0.5,
        color=(int(color[2]), int(color[1]), int(color[0])),
        thickness=params.get('Bold', 1),
        lineType=cv2.LINE_AA
    )

    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def apply_overlay_watermark(image_pil: Image.Image, watermark_pil: Image.Image, method: str, key: int) -> Image.Image:
    method = {
        'Additive'      : lambda src, wm, k: np.clip(src + k * wm, 0, 1),
        'Multiplicative': lambda src, wm, k: np.clip(src * (1 + k * wm), 0, 1),
        'Transparency'  : lambda src, wm, k: np.clip((1 - k) * src + k * wm, 0, 1)
    }[method]

    return Image.fromarray((method(
        src=np.array(image_pil).astype(np.float32) / 255.0,
        wm=np.array(watermark_pil.resize((image_pil.size[0], image_pil.size[1]), Image.LANCZOS)).astype(np.float32) / 255.0,
        k=np.clip(key / 100.0, 0.01, 0.99)
    ) * 255).astype(np.uint8), mode=image_pil.mode)

def embed_lsb_watermark(image_pil: Image.Image, watermark_pil: Image.Image, layer: str, bit_index: int):
    image_rgb = np.array(image_pil.convert('RGB'))
    h, w, _ = image_rgb.shape
    watermark_bin = (cv2.resize(np.array(watermark_pil.convert('L')), (w, h)) > 128).astype(np.uint8)

    if layer in ['R', 'G', 'B']:
        idx = {'R': 0, 'G': 1, 'B': 2}[layer]
        image_rgb[:, :, idx] = (image_rgb[:, :, idx] & ~(1 << bit_index)) | (watermark_bin << bit_index)
        return Image.fromarray(image_rgb)

    elif layer in ['H', 'S', 'I']:
        image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV).astype(np.uint8)
        idx = {'H': 0, 'S': 1, 'I': 2}[layer]
        image_hsv[:, :, idx] = (image_hsv[:, :, idx] & ~(1 << bit_index)) | (watermark_bin << bit_index)
        return Image.fromarray(cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB))

    else:
        image_gray = np.array(image_pil.convert('L'))
        return Image.fromarray((image_gray & ~(1 << bit_index)) | (watermark_bin << bit_index).astype(np.uint8))

def embed_dct_watermark(image_pil: Image.Image, watermark_pil: Image.Image, alpha: float, block_size:int):
    imgage = np.array(image_pil.convert('L')).astype(np.float32)
    h, w = imgage.shape
    watermark = (cv2.resize(np.array(watermark_pil.convert('L')), (w // block_size, h // block_size)) > 128).astype(np.float32).flatten()

    watermarked = np.copy(imgage)

    wm_idx = 0
    i_pos = j_pos = block_size // 2
    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            if wm_idx >= len(watermark):
                break

            dct_block = cv2.dct(watermarked[i:i+block_size, j:j+block_size])
            dct_block[i_pos, j_pos] += alpha * (1 if watermark[wm_idx] else -1)
            idct_block = cv2.idct(dct_block)
            
            watermarked[i:i+block_size, j:j+block_size] = idct_block
            wm_idx += 1

    return Image.fromarray(np.clip(watermarked, 0, 255).astype(np.uint8))

def embed_dwt_watermark(image_pil: Image.Image, watermark_pil: Image.Image, alpha:float, level:int):
    image  = np.array(image_pil.convert('L')).astype(np.float32)
    coeffs = pywt.wavedec2(data=image, level=level, wavelet='haar')

    watermark = (cv2.resize(np.array(watermark_pil.convert('L')), (coeffs[0].shape[1], coeffs[0].shape[0])) > 128).astype(np.float32)

    coeffs = list(coeffs)
    coeffs[0] = coeffs[0] + alpha * watermark

    watermarked = pywt.waverec2(coeffs, wavelet='haar')
    return Image.fromarray(np.clip(watermarked, 0, 255).astype(np.uint8))

def embed_dct_text(image_pil: Image.Image, text: str, alpha: float, block_size: int) -> Image.Image:
    image = np.array(image_pil.convert('L')).astype(np.float32)
    h, w = image.shape
    watermarked = np.copy(image)

    watermark_bits = str_to_bitarray(text)
    if len(watermark_bits) > (h // block_size) * (w // block_size):
        raise image_pil

    wm_idx = 0
    mid = block_size // 2
    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            if wm_idx >= len(watermark_bits):
                break

            dct_block = cv2.dct(watermarked[i:i+block_size, j:j+block_size])
            dct_block[mid, mid] += alpha * (1 if watermark_bits[wm_idx] else -1)
            watermarked[i:i+block_size, j:j+block_size] = cv2.idct(dct_block)
            wm_idx += 1

    return Image.fromarray(np.clip(watermarked, 0, 255).astype(np.uint8))

def extract_dct_text(watermarked_pil: Image.Image, original_pil: Image.Image, block_size: int, length: int) -> str:
    watermarked = np.array(watermarked_pil.convert('L')).astype(np.float32)
    original = np.array(original_pil.convert('L')).astype(np.float32)
    h, w = watermarked.shape

    wm_bits = []
    mid = block_size // 2
    required = length * 8
    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            if len(wm_bits) >= required:
                break

            dct = cv2.dct(original[i:i+block_size, j:j+block_size])
            dct_wm = cv2.dct(watermarked[i:i+block_size, j:j+block_size])
            wm_bits.append(1 if dct_wm[mid, mid] - dct[mid, mid] > 0 else 0)

    return bitarray_to_str(np.array(wm_bits, dtype=np.uint8))

def embed_dwt_text(image_pil: Image.Image, text: str, alpha: float, level: int) -> Image.Image:
    image = np.array(image_pil.convert('L')).astype(np.float32)
    coeffs = pywt.wavedec2(image, wavelet='haar', level=level)

    watermark_bits = str_to_bitarray(text)

    if len(watermark_bits) > coeffs[0].shape[0] * coeffs[0].shape[1]:
        raise image_pil

    wm_array = np.zeros_like(coeffs[0], dtype=np.float32)
    flat = wm_array.flatten()
    flat[:len(watermark_bits)] = 2 * watermark_bits - 1
    wm_array = flat.reshape(coeffs[0].shape)

    coeffs = list(coeffs)
    coeffs[0] = coeffs[0] + alpha * wm_array

    return Image.fromarray(np.clip(pywt.waverec2(coeffs, wavelet='haar'), 0, 255).astype(np.uint8))

def extract_dwt_text(watermarked_pil: Image.Image, original_pil: Image.Image, alpha: float, level: int, length: int) -> str:
    coeffs = pywt.wavedec2(
        data=np.array(original_pil.convert('L')).astype(np.float32),
        wavelet='haar',
        level=level
    )
    coeffs_wm = pywt.wavedec2(
        data=np.array(watermarked_pil.convert('L')).astype(np.float32),
        wavelet='haar',
        level=level
    )

    diff = (coeffs_wm[0] - coeffs[0]) / alpha
    return bitarray_to_str((diff.flatten()[:length * 8] > 0).astype(np.uint8))