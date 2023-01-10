# import requests
#
# from src.baseclasses.response import Response
# from src.enums.global_enums import GlobalErrorMessages
#
# sl = 0
#
#
# def test_getting_posts():
#     r = requests.get(url=sl)
#     response = Response(r)
#     response.assert_status_code(200).validate(POST_SCHEMA)