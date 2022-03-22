from fastapi import APIRouter, Request

# 라우터
router_v1 = APIRouter()


@router_v1.post("/test", status_code=201)
async def create_question_test_ver(
        *,
        question: str,
):
    from apps.backend.chatbot.question.tasks import ka_ka_o_ai
    ka_ka_o_ai.delay(content=question)
    return None


@router_v1.post("/", status_code=201)
async def create_question(
        *,
        request: Request,
):
    body = await request.body()
    # 요청 값
    from apps.backend.chatbot.question.tasks import ka_ka_o_ai
    from apps.backend.chatbot.memo.controllers.properties import KaKaoProperty
    prop = KaKaoProperty(body)
    content = prop.text.get('text')
    ka_ka_o_ai.delay(content=content)
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "JAY 챗봇 동작중"
                        },
                        "items": [
                            {
                                "title": "문의가 등록되었습니다.",
                                "description": ": " + content,
                                "imageUrl": "http://k.kakaocdn.net/dn/APR96/btqqH7zLanY/kD5mIPX7TdD2NAxgP29cC0/1x1.jpg",
                                "link": {
                                    "web": ""
                                }
                            }
                        ],
                        "buttons": [
                            {
                                "label": "데이터 보러가기",
                                "action": "webLink",
                                "webLinkUrl": "http://api.ja-y.com/docs/"
                            }
                        ]
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "전체 명령어",
                    "action": "message",
                    "label": "전체 명령어"
                }
            ]
        }
    }
