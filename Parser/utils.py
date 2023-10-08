class User:
    def __init__(self, id_: int, name: str, account: str, profile_img_urls, is_followed: bool) -> None:
        self.id = id_
        self.name = name
        self.account = account
        self.profile_img_urls = profile_img_urls
        self.is_followed = is_followed


class Tag:
    def __init__(self, name: str, translated_name: str) -> None:
        self.name = name
        self.translated_name = translated_name


class ImageUrls:
    def __init__(self, square_medium: str = None, medium: str = None, large: str = None, original: str = None) -> None:
        self.square_medium = square_medium
        self.medium = medium
        self.large = large
        self.original = original


class Illust:
    def __int__(self, id_: int, title: str, image_urls: ImageUrls, caption: str, restrict: str, user: User, tags: list,
                tools: list, create_date: str, page_count: int, width: int, height: int, sanity_level: int,
                x_restrict: int, series: str, meta_single_page: list, meta_pages: list, total_view: int,
                total_bookmarks: int, is_bookmarked: bool, visible: bool, is_muted: bool, total_comments: int,
                illust_ai_type: int, illust_book_style: int, comment_access_control: int) -> None:
        self.id = id_
        self.title = title
        self.image_urls = image_urls
        self.captoion = caption
        self.restrict = restrict
        self.user = user
        self.tags = tags
        self.tools = tools
        self.create_date = create_date
        self.page_count = page_count
        self.width = width
        self.height = height
        self.sanity_level = sanity_level
        self.x_restrict = x_restrict
        self.series = series
        self.meta_single_page = meta_single_page
        self.meta_pages = meta_pages
        self.total_view = total_view
        self.total_bookmarks = total_bookmarks
        self.is_bookmarked = is_bookmarked
        self.visible = visible
        self.is_muted = is_muted
        self.total_comments
        self.illust_ai_type = illust_ai_type
        self.illust_book_style = illust_book_style
        self.comment_access_control = comment_access_control
