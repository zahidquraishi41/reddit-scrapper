from praw.models.reddit.submission import Submission
from typing import List, Dict, Optional


class Image:
    '''Represents an image with different resolutions and corresponding URLs.'''

    def __init__(self, data: Dict) -> None:
        self.extension = data['m'].split('/')[-1]
        self._metadata = {}
        for preview in data['p']:
            resolution = str(preview['x']) + 'x' + str(preview['y'])
            self._metadata[resolution] = preview['u']

    def resolutions(self) -> List[str]:
        '''Returns a list of available resolutions for the image.'''
        return tuple(self._metadata.keys())

    def url_for(self, resolution: str = None) -> Optional[str]:
        '''Returns the URL for a specific resolution, or the highest resolution if not specified.'''
        if resolution is None:
            resolution = self.resolutions()[-1]
        return self._metadata.get(resolution, None)


class ImageGallery:
    '''Represents a collection of images extracted from a Reddit submission.'''
    def __init__(self, submission: 'Submission') -> None:
        self._images = []
        for metadata in submission.media_metadata.values():
            self._images.append(Image(metadata))

    def images(self) -> List['Image']:
        '''Returns a list of Image objects in the gallery.'''
        return self._images

    def urls(self) -> List[str]:
        '''Returns a list of URLs for the highest resolution of each image in the gallery.'''
        url_list = []
        for image in self._images:
            url_list.append(image.url_for())
        return url_list
