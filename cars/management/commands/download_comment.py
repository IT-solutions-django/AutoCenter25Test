import requests
from bs4 import BeautifulSoup
from cars.models import Reviews
from django.core.management import BaseCommand


def download_comments():
    url = "https://www.vl.ru/commentsgate/ajax/thread/company/autocenter/embedded"

    params = {
        "theme": "company",
        "appVersion": "2024101514104",
        "_dc": "0.362485456772323",
        "pastafarian": "0fb682602c07c4ae9bdb8969e7c43add3b898f4e7b14548c8c2287a29032d6b1",
        "location": "https://www.vl.ru/autocenter#comments",
        "moderatorMode": "1"
    }

    headers = {
        "Host": "www.vl.ru",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Sec-Ch-Ua": "\"Chromium\";v=\"129\", \"Not=A?Brand\";v=\"8\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vl.ru/autocenter",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }

    cookies = {
        "PHPSESSID": "rhjcp9pkfg82bvcda7tve2a9m0",
        "city": "4",
        "region": "103",
        "visitor": "ad5f2acbb35cd457a9dc57c692437d9261e1d5606ea33280caabd64f0fa3d0d6",
        "ring": "980791ab6a297547f26234387e1a5012",
        "analytics_user": "980791ab6a297547f26234387e1a5012",
        "spravochnik_windowSessionID": "ad061bf1730033306880",
        "_ym_uid": "1730033307709177970",
        "_ym_d": "1730033307",
        "sprRecentlyWatchedCompanyIds": "460034",
        "_ym_isad": "2",
        "_gid": "GA1.2.1877505797.1730033311",
        "_ga": "GA1.3.1517315620.1730033307",
        "_ga_3XHX5WMXEB": "GS1.2.1730033312.1.0.1730033312.60.0.0",
        "_ga_D3RZ9TRN3Y": "GS1.3.1730033312.1.0.1730033312.60.0.0",
        "_ga_1XW1PCV9KF": "GS1.2.1730033312.1.1.1730034975.8.0.0",
        "_ym_visorc": "w",
        "spravochnik_windowSessionTS": "1730035316115",
        "_ga_3X07YH0D78": "GS1.1.1730035314.2.1.1730035316.0.0.0",
        "_gat": "1",
        "_gat_allProjects": "1",
        "_gat_glCommonTracker": "1",
        "_gat_commentsvlru": "1",

    }

    response = requests.get(url, headers=headers, params=params, cookies=cookies)

    if response.status_code == 200:
        res = response.json()['data']['content']
        soup = BeautifulSoup(res, 'html.parser')
        review_elements = soup.find_all('li', {'data-type': 'review'})
        reviews = []
        for review in review_elements:
            user_avatar = review.find('div', class_='user-avatar').find('img')
            if user_avatar:
                user_avatar = user_avatar['src']

            user_name_tag = review.find('span', class_='user-name')
            user_name = user_name_tag.text.strip() if user_name_tag else 'N/A'

            review_text_tag = review.find('div', class_='cmt-content').find('p', class_='comment-text')
            if review_text_tag and "Комментарий:" in review_text_tag.text:
                review_text = review_text_tag.text.strip().split("Комментарий:", 1)[1].strip()
            else:
                continue

            review_images = review.find('div', class_='comment-images-wrapper')
            if review_images:
                review_images = [url_img['data-orig-url'] for url_img in review_images.find_all('a')][:2]
            else:
                continue

            reviews.append({
                'user_name': user_name,
                'review_text': review_text,
                'review_images': review_images,
                'user_avatar': user_avatar
            })

        for i, review in enumerate(reviews, 1):
            if len(review['review_images']) == 1:
                image_1 = review['review_images'][0]
                image_2 = None
            else:
                image_1 = review['review_images'][0]
                image_2 = review['review_images'][1]

            rev, _ = Reviews.objects.get_or_create(name=review['user_name'], text_review=review['review_text'],
                                                   num_view=i,
                                                   image1=image_1, image2=image_2, icon_user=review['user_avatar'])
    else:
        print(f"Ошибка: {response.status_code}")


class Command(BaseCommand):
    help = "Добавляет данные с API"

    def handle(self, *args, **kwargs):
        download_comments()
        print("Загрузка завершена!")
