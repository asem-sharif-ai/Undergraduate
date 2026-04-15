
import asyncio

import cv2 as cv
import numpy as np

from pathlib import Path
import os, subprocess, re, unicodedata, requests

from pytubefix import YouTube, Playlist
from youtube_transcript_api import YouTubeTranscriptApi, FetchedTranscript, formatters as F

from googletrans import Translator

def encode(title: str) -> str:
    normalized = unicodedata.normalize('NFKD', title)
    filename = re.sub(r'[\\/*?:"<>|]', '_', normalized).replace(' ', '_').strip('._')
    return filename[:100] if len(filename) > 100 else filename

def clear(title: str) -> str:
    return re.sub(r'[^A-Za-z0-9 _.-]', '', title).strip()

def format_length(length:int) -> str:
    return f'{length//3600:02}:{(length%3600)//60:02}:{length%60:02}'

def format_views(views: int) -> str:
    if views >= 1_000_000_000:
        return f'{views/1_000_000_000:.3f}B'
    elif views >= 1_000_000:
        return f'{views/1_000_000:.2f}M'
    elif views >= 1_000:
        return f'{views/1_000:.1f}K'
    else:
        return f'{views}'

#! ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

class Thumbnail:
    @staticmethod
    def get(url: str) -> np.ndarray:
        try:
            vid = YouTube(url)
            response = requests.get(
                f'https://img.youtube.com/vi/{vid.video_id}/maxresdefault.jpg',
                stream=True
            )

            if response.status_code != 200:
                response = requests.get(vid.thumbnail_url, stream=True)

            response.raise_for_status()

            img = cv.imdecode(np.frombuffer(response.content, dtype=np.uint8), cv.IMREAD_COLOR)
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            _, thresh = cv.threshold(img_gray, 1, 255, cv.THRESH_BINARY)
            x, y, w, h = cv.boundingRect(thresh)
            return img[y:y+h, x:x+w]

        except Exception:
            try:
                response = requests.get(YouTube(url).thumbnail_url, stream=True)
                response.raise_for_status()
                image = cv.imdecode(np.frombuffer(response.content, dtype=np.uint8), cv.IMREAD_COLOR)
                return cv.cvtColor(image, cv.COLOR_GRAY2RGB) if image.ndim == 2 else image
            except:
                return np.zeros((360, 480, 3), dtype=np.uint8)

    @staticmethod
    def download(url: str, filepath: str) -> Path:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        cv.imwrite(str(path), Thumbnail.get(url))
        return path

class Video:
    @staticmethod
    def verify(url:str) -> bool:
        try:
            return True if YouTube(url).watch_url else False
        except:
            return False

    @staticmethod
    def clean(url:str) -> str:
        out = ''
        for l in url:
            if l == '&':
                return out
            out += l
        return out

    @staticmethod
    def information(url:str) -> dict:
        video = YouTube(url)
        return {
            'url': Video.clean(url),
            'title': video.title,
            'author': video.author,
            'date': video.publish_date.strftime('%B %d, %Y. %H:%M.'),
            
            'description': video.description,
            'views': video.views,
            'views_formatted': format_views(video.views),
            'length': video.length,
            'length_formatted': format_length(video.length),
            'streams': {
                'audio': sorted([{
                    'abr': stream.abr,
                    'size': round(stream.filesize / (1024 * 1024), 2)
                    } for stream in video.streams.filter(only_audio=True)],
                                key=lambda x: int(x['abr'].replace('kbps','')),
                                reverse=True
                ),
                'video': {
                    stream.resolution: round(stream.filesize / (1024 * 1024), 2)
                    for stream in video.streams.filter(only_video=True)
                },
                'combined': {
                    f'{stream.abr}-{stream.resolution}': round(stream.filesize / (1024 * 1024), 2)
                    for stream in video.streams.filter(progressive=True)
                }
            }
        }

    #ToDo: ----- ----- Video & Audio ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    @staticmethod
    def download(url, resolution:str, abr:str, filepath:str='.', filename:str='', callback:callable=None, after:callable=None):
        video  = YouTube(url, on_progress_callback=callback)
        stream = video.streams.filter(
            progressive=True,
            res=resolution,
            abr=abr,
            file_extension='mp4'
        ).order_by('fps').desc().first()
    
        if not stream:
            return None

        Path(filepath).mkdir(parents=True, exist_ok=True)
        stream.download(
            filename=f'{encode(filename if filename else video.title)}-[{resolution}-{abr}].mp4',
            output_path=filepath
        )
        
        if after is not None:
            after()

    @staticmethod
    def download_and_merge(
        url, 
        id:str,
        resolution:str, 
        abr:str, 
        filepath:str='.', 
        filename:str='', 
        callback:callable=None, 
        merging:callable=None,
        deleting:callable=None,
        after:callable=None
        ):
        video  = YouTube(url, on_progress_callback=callback)
        video_stream = video.streams.filter(
            only_video=True,
            res=resolution,
            file_extension='mp4'
        ).order_by('fps').desc().first()

        audio  = YouTube(url, on_progress_callback=callback)
        audio_stream = audio.streams.filter(
            only_audio=True,
            abr=abr,
        ).order_by('abr').desc().first()

        if not video_stream or not audio_stream:
            return None

        Path(filepath).mkdir(parents=True, exist_ok=True)
        audio_stream.download(
            filename=f'.{id}.temp.mp3',
            output_path=filepath
        )
        video_stream.download(
            filename=f'.{id}.temp.mp4',
            output_path=filepath
        )

        video_file = Path(filepath) / f'.{id}.temp.mp4'
        audio_file = Path(filepath) / f'.{id}.temp.mp3'
        output_file = Path(filepath) / f'{encode(filename if filename else video.title)}-[{resolution}-{abr}].mp4'

        if not video_file.exists() or not audio_file.exists():
            raise FileNotFoundError('Missing video or audio temp files')

        if merging is not None:
            merging()

        subprocess.run([
            'ffmpeg', '-y', '-i', f'{video_file}', '-i', f'{audio_file}', '-c:v', 'copy', '-c:a', 'aac', f'{output_file}'
        ], check=True)

        if deleting is not None:
            deleting()

        video_file.unlink(missing_ok=True)
        audio_file.unlink(missing_ok=True)

        if after is not None:
            after()

        return output_file

    #ToDo: ----- ----- Video Only ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    @staticmethod
    def download_video(url, resolution:str, filepath:str='.', filename:str='', callback:callable=None, after=None):
        video  = YouTube(url, on_progress_callback=callback)
        stream = video.streams.filter(
            only_video=True,
            res=resolution,
            file_extension='mp4'
        ).order_by('fps').desc().first()

        if not stream:
            return None

        Path(filepath).mkdir(parents=True, exist_ok=True)
        stream.download(
            filename=f'[Video]-{encode(filename if filename else video.title)}-[{resolution}].mp4',
            output_path=filepath
        )
        
        if after is not None:
            after()

    #ToDo: ----- ----- Audio Only ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    @staticmethod
    def download_audio(url, abr:str, filepath:str='.', filename:str='', callback:callable=None, after=None):
        audio  = YouTube(url, on_progress_callback=callback)
        stream = audio.streams.filter(
            only_audio=True,
            abr=abr,
        ).order_by('abr').desc().first()
        
        if not stream:
            print('not found', abr)
            return None

        Path(filepath).mkdir(parents=True, exist_ok=True)
        stream.download(
            filename=f'[Audio]-{encode(filename if filename else audio.title)}-[{abr}].mp3',
            output_path=filepath
        )
        
        if after is not None:
            after()

#! ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

class VideosPlaylist:
    @staticmethod
    def verify(url:str) -> bool:
        try:
            return True if Playlist(url).video_urls else False
        except:
            return False

    @staticmethod
    def videos(url:str) -> list[str]:
        return [video.watch_url for video in Playlist(url).videos]
    
    @staticmethod
    def information(url:str, callback:callable=None) -> dict:
        playlist = Playlist(url)
        videos = VideosPlaylist.videos(url)
        information = {
            'url': url,
            'title': playlist.title,
            'owner': playlist.owner,

            'videos_titles': [YouTube(video).title for video in videos],
            'videos_urls'  : videos,
            'videos_lens'  : [video.length for video in playlist.videos],
            'videos_views' : [video.views for video in playlist.videos],
            'videos_number': len(videos),
            'videos_lens_formatted': [format_length(video.length) for video in playlist.videos],
        }

        information['length'] = sum(information['videos_lens'])
        information['length_formatted'] = format_length(information['length'])
        information['views'] = sum(information['videos_views'])
        information['views_formatted'] = format_views(information['views'])

        try:
            information['last_modified'] = max(YouTube(u).publish_date for u in playlist.video_urls).strftime('%B %d, %Y')
        except:
            information['last_modified'] = ''

        try:
            information['description'] = playlist.description
        except:
            information['description'] = ''

        return information

    @staticmethod
    def make_directory(url, path='.', name=''):
        playlist = Playlist(url)
        playlist_directory = os.path.join(path, encode(f'{playlist.title}-[{playlist.owner}]') if not name else name)
        os.makedirs(name=playlist_directory, exist_ok=True)
        return playlist_directory

#! ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

class Script:
    @staticmethod
    def explore(url:str):
        captions = []
        try:
            video_id = url.split('v=')[-1].split('&')[0]
            if video_id:
                transcripts = YouTubeTranscriptApi().list(video_id)

            for _, t in [*list(transcripts._generated_transcripts.items()), *list(transcripts._manually_created_transcripts.items())]:
                    captions.append(f'{t.language}: `{t.language_code.upper()}`')

        except:
            pass
        return captions
    
    @staticmethod
    def get(url:str, code:str):
        try:
            video_id = url.split('v=')[-1].split('&')[0]
            return YouTubeTranscriptApi().fetch(video_id, languages=[code])
        except:
            return None

    @staticmethod
    def format(script:FetchedTranscript):
        try:
            return F.SRTFormatter().format_transcript(script)
        except:
            return ''

    #! Subtitles are not real sentences; merging them with a separator breaks linguistic context
    #! and causes the translator to restructure meaning across lines. However, its way faster.

    @staticmethod
    def translate_async(script: FetchedTranscript, code: str, batch:int=1, callback:callable=lambda x, y, z, data:None):
        try:
            coro = Script.__t_async(script, code, batch, callback) # Coroutine Object

            try:
                asyncio.get_running_loop()
            except RuntimeError:
                return asyncio.run(coro) # Run synchronously when no event loop

            return asyncio.ensure_future(coro) # Return task if event loop already running 

        except Exception as e:
            return f'Translation failed due to an error: {e}.\n\n{script}'

    @staticmethod
    async def __t_async(script, code, batch_size, callback):
        raw_script = script.to_raw_data()
        translator = Translator()

        #! Subtitles are not real sentences; merging them with a separator breaks linguistic context
        #! and causes the translator to restructure meaning across lines. However, its way faster.

        sep = '\n<<<---|||--->>>\n'
        
        if batch_size == 'ALL':
            merged_text = sep.join(line['text'] for line in raw_script)
            translated = await translator.translate(merged_text, dest=code)
            
            translated_texts = translated.text.split(sep)
            for idx, line in enumerate(raw_script):
                line['text'] = translated_texts[idx]
                
        else:
            now, all = 0, len(raw_script)
            for i in range(0, len(raw_script), batch_size):
                batch = raw_script[i:i + batch_size]

                merged = sep.join(line['text'] for line in batch)
                translated = await translator.translate(merged, dest=code)
                parts = translated.text.split(sep)

                if len(parts) != len(batch): # Safety check
                    raise ValueError('Separator corrupted during translation')

                for line, text in zip(batch, parts):
                    callback(now=now, all=all, percentage=round(now / all, 2)*100, data=(line['text'], text))
                    line['text'] = text
                    now += 1

        return Script.format_srt(raw_data=raw_script)

    @staticmethod 
    def format_srt(raw_data:list):
        def format_time(seconds: float) -> str:
            return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02},{int((seconds - int(seconds)) * 1000):03}"

        srt_lines = []
        for idx, item in enumerate(raw_data, start=1):
            text = item['text'].replace('\n', ' ')
            srt_lines.append(f'{idx}\n{format_time(item["start"])} --> {format_time(item["start"] + item["duration"])}\n{text}\n')

        return '\n'.join(srt_lines)
