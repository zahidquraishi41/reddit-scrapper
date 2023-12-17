from praw.models.reddit.submission import Submission
import requests
from xml.dom import minidom
from typing import Dict, List, Optional
import re


class RedditVideo:
    def __init__(self, submission: 'Submission') -> None:
        self._submission = submission
        self._metadata = self._extract_metadata()
        self.extension = self._extract_extension()

    def video_qualities(self) -> List[str]:
        return tuple(self._metadata['video'].keys())

    def audio_qualities(self) -> List[str]:
        return tuple(self._metadata['audio'].keys())

    def video_url(self, quality: str = None) -> Optional[str]:
        '''Returns the URL of the video. If no specific quality is requested, the URL for the highest available quality will be provided.'''
        if quality is None:
            quality = self.video_qualities()[-1]
        if quality not in self._metadata['video']:
            return None
        return self._metadata['video'][quality]

    def audio_url(self, quality: str = None) -> Optional[str]:
        '''Returns the URL of the audio. If no specific quality is requested, the URL for the highest available quality will be provided.'''
        if len(self.audio_qualities()) == 0:
            return None
        if quality is None:
            quality = self.audio_qualities()[-1]
        if quality not in self._metadata['audio']:
            return None
        return self._metadata['audio'][quality]

    def _extract_metadata(self) -> Dict:
        """Retrieves metadata for video and audio associated with the submission."""
        video = {}

        dash_url = self._submission.media['reddit_video']['dash_url']
        mpd = requests.get(dash_url).text
        dom = minidom.parseString(mpd)
        adaptation_set = dom.getElementsByTagName('AdaptationSet')

        for e in adaptation_set[0].getElementsByTagName('BaseURL'):
            base_url = e.firstChild.nodeValue
            quality = re.findall(r'\d+', base_url)[0] + 'p'
            video[quality] = self._submission.url + '/' + base_url

        if len(adaptation_set) == 1:
            return {'video': video, 'audio': {}}

        audio = {}
        for e in adaptation_set[1].getElementsByTagName('BaseURL'):
            base_url = e.firstChild.nodeValue
            quality = re.findall(r'\d+', base_url)[0] + 'kbps'
            audio[quality] = self._submission.url + '/' + base_url

        return {
            'video': video,
            'audio': audio
        }

    def _extract_extension(self) -> Optional[str]:
        '''Extract the file extension of the video.'''
        if '.' not in self.video_url():
            return None
        ext = self.video_url().split('.')[-1].split('?')[0].lower()
        return None if len(ext) >= 5 else ext
