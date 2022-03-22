from main import test_client


def test_success_create_product():
    response = test_client.get("/")
    print(response.text)
    pass
