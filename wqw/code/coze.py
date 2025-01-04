# coding: utf-8

"""
This example is about how to use the streaming interface to start a chat request
and handle chat events
"""

import os

from cozepy import COZE_COM_BASE_URL


# token 配置 https://www.coze.cn/open/oauth/pats
# bot 先发布成 api才行
conf_info = {
    'token':'pat_GiJJJS***',
    'AI客服': {'bot_id':'7447527125353037875'},
    '鹤啸九天助理': {'bot_id':'7374706518413230099'},
    '聪明一休': {'bot_id':'7277598499636707383'},
    '-': {'bot_id':'-'},
}

bot_name = 'AI客服'
# bot_name = '鹤啸九天助理'
token = conf_info['token']
bot_id = conf_info[bot_name]['bot_id']
# 国内需要制定base地址
COZE_COM_BASE_URL = "https://api.coze.cn"
user_id = "wqw" # 随便设置

# Get an access_token through personal access token or oauth.
coze_api_token = os.getenv("COZE_API_TOKEN", token)
# The default access is api.coze.com, but if you need to access api.coze.cn,
# please use base_url to configure the api endpoint to access
coze_api_base = os.getenv("COZE_API_BASE") or COZE_COM_BASE_URL

print(f'[debug] {bot_name=}, {bot_id=}, {coze_api_token=}')


from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType  # noqa

# Init the Coze client through the access_token.
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

# Create a bot instance in Coze, copy the last number from the web link as the bot's ID.
bot_id = os.getenv("COZE_BOT_ID") or bot_id
# The user id identifies the identity of a user. Developers can use a custom business ID
# or a random string.

question = '你是谁'

# Call the coze.chat.stream method to create a chat. The create method is a streaming
# chat and will return a Chat Iterator. Developers should iterate the iterator to get
# chat event and handle them.
for event in coze.chat.stream(
    bot_id=bot_id,
    user_id=user_id,
    additional_messages=[
        Message.build_user_question_text(question),
    ],
):
    if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
        print(event.message.content, end="", flush=True)

    if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
        print("token usage:", event.chat.usage.token_count)