from datetime import datetime


def log(message):
    from apps.backend.service.notice.controllers.send import send_slack_background_task
    from apps.backend.service.notice.schemas import SendSlackRequest

    # 슬랙 전송
    message = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    send_slack_background_task(SendSlackRequest(
        room='stock',
        message=message
    ))

    from conf.caches import ka_ka_o_cache
    from apps.backend.external.kakao.controllers.message import MessageTemplate
    from apps.backend.external.kakao.controllers.message import send_to_me_message

    # 카카오 나에게 메시지 전송
    access_token = ka_ka_o_cache.get('access_token')
    template = MessageTemplate.default_text(message)
    send_to_me_message(access_token=access_token, template=template)


def get_bs_obj(com_code):
    import requests
    from bs4 import BeautifulSoup

    url = "https://finance.naver.com/item/main.nhn?code=" + com_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj


def get_price(com_code):
    try:
        bs_obj = get_bs_obj(com_code)
        no_today = bs_obj.find("p", {"class": "no_today"})
        blind_now = no_today.find("span", {"class": "blind"})
        price = str(blind_now.text).replace(",", "").strip()
        return int(price)
    except:
        return -1


def get_percent(com_code):
    bs_obj = get_bs_obj(com_code)
    no_now = bs_obj.find_all("em", {"class": "no_down"})
    if len(no_now) < 1:
        no_now = bs_obj.find_all("em", {"class": "no_up"})
    blind_no_now = no_now[2].find("span", {"class": "blind"})
    if '-' in no_now[2].text:
        percent = '-' + blind_no_now.text + '%'
    else:
        percent = blind_no_now.text + '%'
    return percent


def schedule_send_stock():
    from conf.settings.prod import settings
    my_code = str(settings.SEND_STOCK_MY_CODE)
    buy_price = int(settings.SEND_STOCK_BUY_PRICE)
    qty = int(settings.SEND_STOCK_QTY)

    total = buy_price * qty
    t_now = datetime.now()
    t_start = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
    t_exit = t_now.replace(hour=15, minute=20, second=0, microsecond=0)
    today = datetime.today().weekday()
    if t_start < t_now < t_exit and not (today == 5 or today == 6):
        current_price = get_price(my_code)
        if current_price < 1:
            log('[상태] 값 불러오기 실패 종료')
        else:
            current_total = current_price * qty
            plus_minus = current_total - total
            total_diff = int(((float(current_price) - buy_price) / (
                    float(current_price) - (float(current_price) - buy_price))) * 1000) / 10  # 등락률
            log(
                f'합계: {format(current_total, ",")}원 / '
                f'손익: {format(plus_minus, ",")}원({total_diff}%) / '
                f'현재가: {format(current_price, ",")}원({get_percent(my_code)})'
            )
