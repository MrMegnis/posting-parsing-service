import json
from utils import *


class IllustDecoder:

    def object_hook(self, dct):
        return Illust(dct['id'], dct['title'], self.decode_image_urls(dct['image_urls']), dct['caption'],
                      dct['restrict'], self.decode_user(dct['user']), self.deocde_tags(dct['tags']),
                      self.decode_tools(dct['tools']), self.decode_create_date(dct['create_date']), dct['page_count'],
                      dct['width'], dct['height'], dct['sanity_level'], dct['x_restrict'], dct['series'],
                      self.decode_meta_single_page(dct['meta_single_page']), self.decode_meta_pages(['meta_pages']),
                      dct['total_view'], dct['total_bookmarks'], dct['is_bookmarked'], dct['visible'], dct['is_muted'],
                      dct['total_comments'], dct['illust_ai_type'], dct['illust_book_style'],
                      dct['comment_access_control'])

    def decode_image_urls(self, dct):
        if "square_medium" not in dct:
            dct['square_medium'] = None
        if "medium" not in dct:
            dct['medium'] = None
        if "large" not in dct:
            dct['large'] = None
        if "original" not in dct:
            dct['original'] = None
        return ImageUrls(dct['square_medium'], dct['medium'], dct['large'], dct['original'])

    def decode_user(self, dct) -> User:
        return User(dct['id'], dct['name'], dct['account'], dct['profile_img_urls'], dct['is_followed'])

    def deocde_tags(self, dct) -> Tag:
        return Tag(dct['name'], dct['translated_name'])

    def decode_create_date(self, s):
        pass

    def decode_tools(self) -> list:
        tools = list()
        return tools

    def decode_meta_single_page(self):
        return

    def decode_meta_pages(self, lst : list) -> list:
        meta_pages = list()
        for i in lst:
            meta_pages.append(self.decode_image_urls(i))
        return meta_pages


class IllustDecoderJSON(json.JSONDecoder, IllustDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(object_hook=self.object_hook, *args, **kwargs)
