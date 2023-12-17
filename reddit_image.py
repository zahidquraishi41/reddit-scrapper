from praw.models.reddit.submission import Submission
from typing import Tuple, Optional, Dict


class RedditImage:
    '''A class representing an image from a Reddit submission.'''

    def __init__(self, submission: 'Submission') -> None:
        self._submission = submission
        self._metadata = self._extract_metadata()
        self.extension = self._extract_extension()

    def resolutions(self) -> Tuple[str]:
        '''Retrieve available resolutions for the image.

        Returns:
            Tuple[str]: A tuple of available resolutions.'''
        return tuple(self._metadata.keys())

    def url_for(self, resolution: str) -> Optional[str]:
        """Get the URL for a specific resolution.

        Args:
            resolution (str): The desired resolution.

        Returns:
            Optional[str]: The URL for the specified resolution, or None if not available.
        """
        return self._metadata.get(resolution, None)

    def source_url(self) -> str:
        '''Retrieve the URL of the image in its original quality as posted on Reddit.'''
        return self._submission.url

    def _extract_metadata(self) -> Dict:
        '''Extract metadata from the Reddit submission.'''
        metadata = {}
        preview = self._submission.preview['images'][0]

        for resolution in preview['resolutions']:
            key = f"{resolution['width']}x{resolution['height']}"
            metadata[key] = resolution['url']
        source = f"{preview['source']['width']}x{preview['source']['height']}"
        metadata[source] = preview['source']['url']

        return metadata

    def _extract_extension(self) -> Optional[str]:
        '''Extract the file extension of the image.'''
        if '.' not in self.source_url():
            return None
        ext = self.source_url().split('.')[-1].split('?')[0].lower()
        return None if len(ext) >= 5 else ext
