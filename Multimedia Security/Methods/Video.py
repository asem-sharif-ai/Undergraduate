import os
import cv2
import pywt
import tempfile
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip

def validate(path: str):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return (None, False)
    return (cap, True)

def get_properties(path: str, cap: cv2.VideoCapture):
    if not cap or not cap.isOpened():
        return {'Error': 'Invalid video capture object.'}

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps if fps > 0 else 0

    ret, frame = cap.read()
    if not ret:
        color_mode = 'UnKnown'
    else:
        channels = frame.shape[2] if len(frame.shape) == 3 else 1
        color_mode = {1: 'Grayscale', 3: 'RGB', 4: 'RGBA'}.get(channels, f'{channels}-Channel')
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    audio_info = 'None'
    audio_channels = audio_fps = audio_bitdepth = audio_peak = audio_duration = '-'
    if path and os.path.exists(path):
        try:
            clip = VideoFileClip(path)
            audio_duration = clip.duration
            if clip.audio:
                audio_info = 'Present'
                audio_channels = clip.audio.nchannels
                audio_fps = clip.audio.fps
                audio_samples = clip.audio.to_soundarray(fps=audio_fps)
                audio_bitdepth = 16 if audio_samples.dtype == np.int16 else 32
                audio_peak = np.max(np.abs(audio_samples)) / (2 ** (audio_bitdepth - 1))
        except Exception as e:
            audio_info = f'Error ({e}).'

    return {
        'Path': path,
        'Video': {
            'Resolution': f'{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))} x {int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}',
            'Frame_Count': frame_count,
            'FPS': fps,
            'Duration_Seconds': duration,
            'Duration': f'{int(duration // 60)}:{int(duration % 60)}',
            'Color_Mode': color_mode
        },
        'Audio': {
            'Audio_Present': audio_info,
            'Duration_Seconds': audio_duration,
            'Duration': f'{int(audio_duration // 60)}:{int(audio_duration % 60)}',
            'Sample_Rate': audio_fps,
            'Channels': audio_channels,
            'Bit_Depth': audio_bitdepth,
            'Peak_Amplitude': audio_peak
        }
    }

def format_properties(info: dict):
    return f'''File Path:
    - `{info['Path']}`

Video Properties:
    - Resolution     : {info['Video']['Resolution']}
    - Color Mode     : {info['Video']['Color_Mode']}
    - Frame Count    : {info['Video']['Frame_Count']}
    - Duration       : {info['Video']['Duration_Seconds']:.2f} Seconds [{info['Video']['Duration']}]
    - FPS            : {info['Video']['FPS']:.2f}

Audio Properties:
    - Audio Present  : {info['Audio']['Audio_Present']}
    - Duration       : {info['Audio']['Duration_Seconds']:.2f} Seconds [{info['Audio']['Duration']}]
    - Sample Rate    : {info['Audio']['Sample_Rate']} Hz
    - Channels       : {info['Audio']['Channels']}
    - Bit Depth      : {info['Audio']['Bit_Depth']} Bits
    - Peak Amplitude : {info['Audio']['Peak_Amplitude']}'''

def apply_dct_watermark(video_path: str, watermark_path: str, alpha: float) -> cv2.VideoCapture:
    watermark_img = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)
    watermark_img = np.float32(cv2.resize(watermark_img, (64, 64)))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    temp_fd, temp_path = tempfile.mkstemp(suffix='.avi')
    os.close(temp_fd)

    out = cv2.VideoWriter(temp_path, fourcc, fps, (w, h), isColor=True)
    while True:
        ret, frame = cap.read()
        if not ret: break

        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        y_channel = np.float32(ycrcb[:, :, 0])

        dct_y = cv2.dct(y_channel)
        dct_y += alpha * cv2.resize(watermark_img, (y_channel.shape[1], y_channel.shape[0]))

        ycrcb[:, :, 0] = np.clip(cv2.idct(dct_y), 0, 255)
        out.write(cv2.cvtColor(np.uint8(ycrcb), cv2.COLOR_YCrCb2BGR))

    cap.release()
    out.release()

    return cv2.VideoCapture(temp_path)

def apply_dwt_watermark(video_path: str, watermark_path: str, alpha: float) -> cv2.VideoCapture:

    watermark_img = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)
    watermark_img = np.float32(cv2.resize(watermark_img, (64, 64)))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    temp_fd, temp_path = tempfile.mkstemp(suffix='.avi')
    os.close(temp_fd)

    out = cv2.VideoWriter(temp_path, fourcc, fps, (w, h), isColor=True)
    while True:
        ret, frame = cap.read()
        if not ret: break

        coeffs = pywt.dwt2(np.float32(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)), 'haar')
        LL, (LH, HL, HH) = coeffs

        LL_wm = LL + alpha * cv2.resize(watermark_img, (LL.shape[1], LL.shape[0]))
        watermarked = np.clip(pywt.idwt2((LL_wm, (LH, HL, HH)), 'haar'), 0, 255).astype(np.uint8)

        out.write(cv2.cvtColor(watermarked, cv2.COLOR_GRAY2RGB))

    cap.release()
    out.release()

    return cv2.VideoCapture(temp_path)

def export_video(path: str, video_capture: cv2.VideoCapture):
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    writer = cv2.VideoWriter(
        path,
        cv2.VideoWriter_fourcc(*'XVID'),
        video_capture.get(cv2.CAP_PROP_FPS),
        (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )

    while True:
        ret, frame = video_capture.read()
        if not ret: break
        writer.write(frame)

    writer.release()
