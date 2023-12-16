from praw.models.reddit.submission import Submission
from typing import Tuple, Optional, Dict


class RedditGif:
    '''A class representing an gif from a Reddit submission.'''

    def __init__(self, submission: 'Submission') -> None:
        self._submission = submission
        self._metadata = self._extract_metadata()
        self.extension = self._extract_extension()

    def resolutions(self) -> Tuple[str]:
        '''Retrieve available resolutions for the gif.

        Returns:
            Tuple[str]: A tuple of available resolutions.'''
        return tuple(self._metadata.keys())

    def url_for(self, resolution: str, variant: str = 'gif') -> Optional[str]:
        """Get the URL for a specific resolution.

        Args:
            resolution (str): The desired resolution.
            variant (str): can be gif or mp4.

        Returns:
            Optional[str]: The URL for the specified resolution, or None if not available.
        """
        if resolution not in self._metadata:
            return None
        return self._metadata[resolution][variant]

    def source_url(self) -> str:
        '''Retrieve the URL of the gif in its original quality as posted on Reddit.'''
        return self._submission.url

    def _extract_metadata(self) -> Dict:
        metadata = {}
        variants = self._submission.preview['images'][0]['variants']

        # extracting gif metadata
        for resolution in variants['gif']['resolutions']:
            key = f"{resolution['width']}x{resolution['height']}"
            metadata[key] = {'gif': resolution['url']}

        # extracting mp4 metadata
        for resolution in variants['mp4']['resolutions']:
            key = f"{resolution['width']}x{resolution['height']}"
            metadata[key]['mp4'] = resolution['url']

        # extracting source urls for both variant
        source_key = f"{variants['gif']['source']['width']}x{variants['gif']['source']['width']}"
        metadata[source_key] = {'gif': variants['gif']['source']['url']}
        metadata[source_key]['mp4'] = variants['mp4']['source']['url']

        return metadata

    def _extract_extension(self) -> Optional[str]:
        '''Extract the file extension of the gif.'''
        if '.' not in self._submission.url:
            return None
        _ext = self.source_url().split('.')[-1].split('?')[0].lower()
        return None if len(_ext) >= 5 else _ext
