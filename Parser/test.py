from pixivpy3 import *
from pixiv_auth import refresh


def main():
    api = AppPixivAPI()
    refresh_token = "bcUSLH30_xqfPe5VwMkk2nH82JIJig9_q0d6rbCYo5U"
    auth_token = refresh(refresh_token)[0]
    # api.auth(refresh_token="bcUSLH30_xqfPe5VwMkk2nH82JIJig9_q0d6rbCYo5U")
    api.set_auth(access_token=auth_token, refresh_token=refresh_token)
    # print(api.illust_follow())
    # print(api.illust_detail("111035834"))
    # print(api.illust_comments("59580629"))
    # print(api.illust_related("59580629"))
    # print(api.illust_recommended())
    # print(api.illust_ranking(mode="day"))
    # print(api.trending_tags_illust())
    print(api.search_illust("raiden", search_target="exact_match_for_tags"))
    # print(api.ugoira_metadata("59580629"))
    # print(api.illust_new())


if __name__ == "__main__":
    main()