# 程序创建@李宏宇
# 创建时间 ：2023/5/24
import json
import os.path
import re

from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 项目根目录
DRI_ROOT = os.path.dirname(os.path.abspath(__file__))
HOT_DATA_ROOT = os.path.join(DRI_ROOT, "hot_info", '1.json')


def data_test():
    """数据获取测试"""

    headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'douyin.com; ttwid=1%7CWP4mCaW3X8f3V58F6OHlnNRyEkVqYPxjQL73dfd3LIU%7C1681093426%7Cc767089a70297960fd10508898790ce841fa5055935577db93caf77b267a149f; passport_csrf_token=6d96a7a26d8854677ec5b45069549987; passport_csrf_token_default=6d96a7a26d8854677ec5b45069549987; s_v_web_id=verify_lgoygtp9_NT6wfH86_8SLo_4NQX_Awp9_NyPPrPoLrHrd; xgplayer_user_id=129087249187; __live_version__=%221.1.0.8723%22; pwa2=%223%7C0%22; n_mh=_YYFAsdKF-atR-PKycJJCSJnkHK4DjqJLX3B91ypCU4; store-region=cn-gd; store-region-src=uid; _tea_utm_cache_2018=undefined; publish_badge_show_info=%220%2C0%2C0%2C1684811594641%22; download_guide=%223%2F20230523%22; my_rd=1; passport_assist_user=CjxdxPFEtRX2o2W2pPN8CVthSMH916GuAOfdMvXm-6vEtM3q1YKeDR5sNatn39ZtBW3jxBCdhiHGdNIZVqMaSAo8O6yEk6HOGtpcbtrE_pGFteCMA2KDfAH9IPqNf_flVpxUPT5d485fofsYu7sLBMgfNKJBrMxhFRK0C7t3EPTysQ0Yia_WVCIBA7Ux2XA%3D; sso_uid_tt=7ba4e3e0d77807be75adaf752bcdfefa; sso_uid_tt_ss=7ba4e3e0d77807be75adaf752bcdfefa; toutiao_sso_user=0a4f6fe5b7df1c27a7d9ed0d6b671d30; toutiao_sso_user_ss=0a4f6fe5b7df1c27a7d9ed0d6b671d30; sid_ucp_sso_v1=1.0.0-KDExNmFjYmFlYzBkZmIwOGEyODNiNjZjMTA0Njg0ZDM5NjM4MDQ2NTAKHQjCgbvP2QIQkoeyowYY7zEgDDCkpP_TBTgGQPQHGgJobCIgMGE0ZjZmZTViN2RmMWMyN2E3ZDllZDBkNmI2NzFkMzA; ssid_ucp_sso_v1=1.0.0-KDExNmFjYmFlYzBkZmIwOGEyODNiNjZjMTA0Njg0ZDM5NjM4MDQ2NTAKHQjCgbvP2QIQkoeyowYY7zEgDDCkpP_TBTgGQPQHGgJobCIgMGE0ZjZmZTViN2RmMWMyN2E3ZDllZDBkNmI2NzFkMzA; odin_tt=09c15e9de5321a63ce74cfa2bcb29de44545afb88829fa05df26810ed967839e3e1717432db4d5eafe1782f078e769bc; passport_auth_status=74785976b8991f7aaaf2e6f74c72f2da%2C; passport_auth_status_ss=74785976b8991f7aaaf2e6f74c72f2da%2C; uid_tt=4f9e059632a6983b613e8f27945ab390; uid_tt_ss=4f9e059632a6983b613e8f27945ab390; sid_tt=6bb111a57804f15790925205b0bc136e; sessionid=6bb111a57804f15790925205b0bc136e; sessionid_ss=6bb111a57804f15790925205b0bc136e; LOGIN_STATUS=1; sid_guard=6bb111a57804f15790925205b0bc136e%7C1684833173%7C5183999%7CSat%2C+22-Jul-2023+09%3A12%3A52+GMT; sid_ucp_v1=1.0.0-KDRiODkwY2UzODA5NjkxYTIxNzRhYTY4NjNmZTgzZTdiMGMyNTAzYmIKGQjCgbvP2QIQlYeyowYY7zEgDDgGQPQHSAQaAmhsIiA2YmIxMTFhNTc4MDRmMTU3OTA5MjUyMDViMGJjMTM2ZQ; ssid_ucp_v1=1.0.0-KDRiODkwY2UzODA5NjkxYTIxNzRhYTY4NjNmZTgzZTdiMGMyNTAzYmIKGQjCgbvP2QIQlYeyowYY7zEgDDgGQPQHSAQaAmhsIiA2YmIxMTFhNTc4MDRmMTU3OTA5MjUyMDViMGJjMTM2ZQ; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1685447508201%2C%22type%22%3A1%7D; douyin.com; strategyABtestKey=%221684893216.381%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNlcnQiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS1cbk1JSUNFekNDQWJxZ0F3SUJBZ0lVZmdhdHBhbUx3WGd4ZEdEeEYxZllFMUlVK3VZd0NnWUlLb1pJemowRUF3SXdcbk1URUxNQWtHQTFVRUJoTUNRMDR4SWpBZ0JnTlZCQU1NR1hScFkydGxkRjluZFdGeVpGOWpZVjlsWTJSellWOHlcbk5UWXdIaGNOTWpNd05ESXhNRFF4TmpBeldoY05Nek13TkRJeE1USXhOakF6V2pBbk1Rc3dDUVlEVlFRR0V3SkRcblRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERcbkFRY0RRZ0FFelM5UTlTMVpsVTBqVUtuRGxhVWpTQkZ4TmFnZTN4QWdOSzg3VnJQRmNlVjBhWHRWVlA3ZUQyY3ZcbkxRZzdRUjEvSnlySSt3ckl4Ynk0R1RIWWlHNFBpS09CdVRDQnRqQU9CZ05WSFE4QkFmOEVCQU1DQmFBd01RWURcblZSMGxCQ293S0FZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ0JnZ3JCZ0VGQlFjREF3WUlLd1lCQlFVSEF3UXdcbktRWURWUjBPQkNJRUlFa1haUUxDY21IMEZhRWRmU1NKaUVBU3RteHJaWDBiQWNIL3hnbmEwL3B6TUNzR0ExVWRcbkl3UWtNQ0tBSURLbForcU9aRWdTamN4T1RVQjdjeFNiUjIxVGVxVFJnTmQ1bEpkN0lrZURNQmtHQTFVZEVRUVNcbk1CQ0NEbmQzZHk1a2IzVjVhVzR1WTI5dE1Bb0dDQ3FHU000OUJBTUNBMGNBTUVRQ0lDbFU1aUpyYUdiWGlhT25cblZVTmxzMzNoTmwwQXpCSmNjZGdjNzMyZDl4Y3RBaUEvTzE2ZjIrd0JqRUMvNEdVVmU1MTlQNXV6UEc5Q3lzSzVcbkYrUHZxay9tQ0E9PVxuLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLVxuIn0=; SEARCH_RESULT_LIST_TYPE=%22single%22; csrf_session_id=dfcbc46faf20691ba92f8d8c2cc0be2e; home_can_add_dy_2_desktop=%221%22; tt_scid=-29JI9s9tao8Oe4AVvUZtM63dyBobrl.WkAuKx6dpAXLCZhyY9nJJmENRNrAUTGb655f; passport_fe_beating_status=true; msToken=MFiP8Y7QcL8yC1JnfTUtPEvk79khTNuMgPLnx3HHQqRjhx2unNzH29a6AyHtWtbdPNDa9LtDg7Dc2sw5Z5pqnYcdjmti8jjy3igH9ekH2Rb8V1VJeGBUqEzZR6m1gbw=; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAZttkn5D-y8WWy7dDbYZT6mcI_JW7DeZeV_PLCexBZ08%2F1684944000000%2F0%2F0%2F1684910839229%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAZttkn5D-y8WWy7dDbYZT6mcI_JW7DeZeV_PLCexBZ08%2F1684944000000%2F0%2F1684910239229%2F0%22; msToken=XijbHQ4Pa0XyepNl95N-x9ymcO0WfRz1MowioXcDMdYoMfvCrWpdU0CtZp_-JC7naUkuQJsI2QRv_DGBOgAgk5tZSBmBJFrKYZZYJzbzqNDcQY0vUkKWwekOwq28T1Q=; __ac_nonce=0646db0ae004ab29b93bd; __ac_signature=_02B4Z6wo00f01Smj9JgAAIDASqk08E44p70pg.AAAC4I7QnFcutDDAjlUSxnEbfWQCE-g3dfmVf3hFDrdh1XJlbAv122uyhFNucavLDUBb4D9hZM2Ll4W7ZAaNyU.jwts5Ab7YDGcqbtfnyM6a; __ac_referer=__ac_blank',
        'referer': 'https://www.douyin.com/hot/1218856',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }
    url = 'https://www.douyin.com/hot/1220067'
    response = requests.get(url, headers = headers)
    my_etree = etree.HTML(response.text)
    # 点赞收藏关注转发
    collect_xpath = '//div[@class="UwvcKsMK"]/div'
    result = my_etree.xpath(collect_xpath)
    print(response.url)
    for i in result:
        j = i[1].text
        jj = j[-1::-1]
        print(jj)
        # print(int(i[1].text) * 10000)
        print(i[1].text)
    # 作者id
    user_xpath = '//div[@class="Yja39qrE"]//div[@class="CjPRy13J"]/a/@href'
    # 作者url
    user_url = my_etree.xpath(user_xpath)
    print(str(user_url[0]))
    user_id = re.search(r'/(MS4[\w-]+)/?', user_url[0])
    print(user_id.group(1))

    # 创建Chrome浏览器选项
    chrome_options = Options()
    # 启用无界面模式
    chrome_options.add_argument('--headless')
    # 初始化Chrome浏览器
    my_driver = webdriver.Chrome(options = chrome_options)
    my_driver.get(url)
    url_late = my_driver.current_url
    print(url_late)
    # 提取视频ID
    video_id = re.findall(r'/video/(\d+)\?', url_late)[0]
    print(video_id)
    # 提取hotValue参数
    hot_value = re.findall(r'hotValue=(\d+)', url_late)[0]
    print(hot_value)

    # 粉丝和获赞数


def hot_test():
    hot_url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&board_type=0&board_sub_type=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=108.0.0.0&browser_online=true&engine_name=Blink&engine_version=108.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7220241251533325879&msToken=09bb7bdtFpKczdRjEP693s3ueQRca2bgB2EdXOm-oAavCoVUSkl0t1pRlxo6uMAsVK0a6knoklybWgnCNSRmql8R_c3yE0FeZ_SVvirum1JpSfmkmrGPdEjQK1s5Chs=&X-Bogus=DFSzswVOw7bANHnXttLBiRXAIQRd'
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'ttwid=1%7CWP4mCaW3X8f3V58F6OHlnNRyEkVqYPxjQL73dfd3LIU%7C1681093426%7Cc767089a70297960fd10508898790ce841fa5055935577db93caf77b267a149f; passport_csrf_token=6d96a7a26d8854677ec5b45069549987; passport_csrf_token_default=6d96a7a26d8854677ec5b45069549987; s_v_web_id=verify_lgoygtp9_NT6wfH86_8SLo_4NQX_Awp9_NyPPrPoLrHrd; xgplayer_user_id=129087249187; __live_version__=%221.1.0.8723%22; pwa2=%223%7C0%22; n_mh=_YYFAsdKF-atR-PKycJJCSJnkHK4DjqJLX3B91ypCU4; store-region=cn-gd; store-region-src=uid; _tea_utm_cache_2018=undefined; publish_badge_show_info=%220%2C0%2C0%2C1684811594641%22; download_guide=%223%2F20230523%22; my_rd=1; passport_assist_user=CjxdxPFEtRX2o2W2pPN8CVthSMH916GuAOfdMvXm-6vEtM3q1YKeDR5sNatn39ZtBW3jxBCdhiHGdNIZVqMaSAo8O6yEk6HOGtpcbtrE_pGFteCMA2KDfAH9IPqNf_flVpxUPT5d485fofsYu7sLBMgfNKJBrMxhFRK0C7t3EPTysQ0Yia_WVCIBA7Ux2XA%3D; sso_uid_tt=7ba4e3e0d77807be75adaf752bcdfefa; sso_uid_tt_ss=7ba4e3e0d77807be75adaf752bcdfefa; toutiao_sso_user=0a4f6fe5b7df1c27a7d9ed0d6b671d30; toutiao_sso_user_ss=0a4f6fe5b7df1c27a7d9ed0d6b671d30; sid_ucp_sso_v1=1.0.0-KDExNmFjYmFlYzBkZmIwOGEyODNiNjZjMTA0Njg0ZDM5NjM4MDQ2NTAKHQjCgbvP2QIQkoeyowYY7zEgDDCkpP_TBTgGQPQHGgJobCIgMGE0ZjZmZTViN2RmMWMyN2E3ZDllZDBkNmI2NzFkMzA; ssid_ucp_sso_v1=1.0.0-KDExNmFjYmFlYzBkZmIwOGEyODNiNjZjMTA0Njg0ZDM5NjM4MDQ2NTAKHQjCgbvP2QIQkoeyowYY7zEgDDCkpP_TBTgGQPQHGgJobCIgMGE0ZjZmZTViN2RmMWMyN2E3ZDllZDBkNmI2NzFkMzA; odin_tt=09c15e9de5321a63ce74cfa2bcb29de44545afb88829fa05df26810ed967839e3e1717432db4d5eafe1782f078e769bc; passport_auth_status=74785976b8991f7aaaf2e6f74c72f2da%2C; passport_auth_status_ss=74785976b8991f7aaaf2e6f74c72f2da%2C; uid_tt=4f9e059632a6983b613e8f27945ab390; uid_tt_ss=4f9e059632a6983b613e8f27945ab390; sid_tt=6bb111a57804f15790925205b0bc136e; sessionid=6bb111a57804f15790925205b0bc136e; sessionid_ss=6bb111a57804f15790925205b0bc136e; LOGIN_STATUS=1; sid_guard=6bb111a57804f15790925205b0bc136e%7C1684833173%7C5183999%7CSat%2C+22-Jul-2023+09%3A12%3A52+GMT; sid_ucp_v1=1.0.0-KDRiODkwY2UzODA5NjkxYTIxNzRhYTY4NjNmZTgzZTdiMGMyNTAzYmIKGQjCgbvP2QIQlYeyowYY7zEgDDgGQPQHSAQaAmhsIiA2YmIxMTFhNTc4MDRmMTU3OTA5MjUyMDViMGJjMTM2ZQ; ssid_ucp_v1=1.0.0-KDRiODkwY2UzODA5NjkxYTIxNzRhYTY4NjNmZTgzZTdiMGMyNTAzYmIKGQjCgbvP2QIQlYeyowYY7zEgDDgGQPQHSAQaAmhsIiA2YmIxMTFhNTc4MDRmMTU3OTA5MjUyMDViMGJjMTM2ZQ; douyin.com; strategyABtestKey=%221684893216.381%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNlcnQiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS1cbk1JSUNFekNDQWJxZ0F3SUJBZ0lVZmdhdHBhbUx3WGd4ZEdEeEYxZllFMUlVK3VZd0NnWUlLb1pJemowRUF3SXdcbk1URUxNQWtHQTFVRUJoTUNRMDR4SWpBZ0JnTlZCQU1NR1hScFkydGxkRjluZFdGeVpGOWpZVjlsWTJSellWOHlcbk5UWXdIaGNOTWpNd05ESXhNRFF4TmpBeldoY05Nek13TkRJeE1USXhOakF6V2pBbk1Rc3dDUVlEVlFRR0V3SkRcblRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERcbkFRY0RRZ0FFelM5UTlTMVpsVTBqVUtuRGxhVWpTQkZ4TmFnZTN4QWdOSzg3VnJQRmNlVjBhWHRWVlA3ZUQyY3ZcbkxRZzdRUjEvSnlySSt3ckl4Ynk0R1RIWWlHNFBpS09CdVRDQnRqQU9CZ05WSFE4QkFmOEVCQU1DQmFBd01RWURcblZSMGxCQ293S0FZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ0JnZ3JCZ0VGQlFjREF3WUlLd1lCQlFVSEF3UXdcbktRWURWUjBPQkNJRUlFa1haUUxDY21IMEZhRWRmU1NKaUVBU3RteHJaWDBiQWNIL3hnbmEwL3B6TUNzR0ExVWRcbkl3UWtNQ0tBSURLbForcU9aRWdTamN4T1RVQjdjeFNiUjIxVGVxVFJnTmQ1bEpkN0lrZURNQmtHQTFVZEVRUVNcbk1CQ0NEbmQzZHk1a2IzVjVhVzR1WTI5dE1Bb0dDQ3FHU000OUJBTUNBMGNBTUVRQ0lDbFU1aUpyYUdiWGlhT25cblZVTmxzMzNoTmwwQXpCSmNjZGdjNzMyZDl4Y3RBaUEvTzE2ZjIrd0JqRUMvNEdVVmU1MTlQNXV6UEc5Q3lzSzVcbkYrUHZxay9tQ0E9PVxuLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLVxuIn0=; SEARCH_RESULT_LIST_TYPE=%22single%22; csrf_session_id=dfcbc46faf20691ba92f8d8c2cc0be2e; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1685515801278%2C%22type%22%3A1%7D; __ac_signature=_02B4Z6wo00f01pFl6bwAAIDD8m8p1xd2gx6RRe0AAMBAyOrEGORqG0vM8Bj6PMpD-P-uwfO2R9DFkWFa-yNFVhHQFO73.yaOnEucO0T9UI7NmsLvKD8I52TIblx1.zeUwFRW8uuZ2KTbN3qG8c; passport_fe_beating_status=true; tt_scid=O4qR6r3iNx-c1odONo8ojfLZqVg-h9I8M6Sdc5k5HIGNQtfRTFBrDwsOXtH7ZzRvae0d; msToken=ixvaBaMNba3Yn6Xizu3AHouvGqjzvXIUgdZafG7gw2bXoKw9ClRIxLyc3VD_kxCuqopZX48LO7N1JzD0bZC4T5qLvQxeY85N7fYoHXqJ4ZxyJ0BU9XJ8-h0rAV6f6vk=; __ac_nonce=0646dcfde00a948737a53; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAZttkn5D-y8WWy7dDbYZT6mcI_JW7DeZeV_PLCexBZ08%2F1684944000000%2F0%2F0%2F1684918848580%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAZttkn5D-y8WWy7dDbYZT6mcI_JW7DeZeV_PLCexBZ08%2F1684944000000%2F0%2F0%2F1684919448580%22; home_can_add_dy_2_desktop=%221%22; msToken=09bb7bdtFpKczdRjEP693s3ueQRca2bgB2EdXOm-oAavCoVUSkl0t1pRlxo6uMAsVK0a6knoklybWgnCNSRmql8R_c3yE0FeZ_SVvirum1JpSfmkmrGPdEjQK1s5Chs=',
        'referer': 'https://www.douyin.com/discover',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    response = requests.get(url = hot_url, headers = headers)
    print(response.text)
    json.dump(response.json(), open(HOT_DATA_ROOT, "w", encoding = "utf-8"), ensure_ascii = False)


data_test()
# hot_test()
