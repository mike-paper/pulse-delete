import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

token = os.environ.get('PAPER_SLACK_TOKEN')

client = WebClient(token=token)

def testPush():
    print('testPush...')
    response = client.chat_postMessage(
        channel='#demo',
        blocks = [
            {
                "type": "section", 
                "text": {
                    "type": "plain_text", "text": "Hello world"
                    },
                "accessory": {
                    "type": "image",
                    "image_url": "https://seekwell.ngrok.io/assets/altair_saverchart.png",
                    "alt_text": "alt text for image"
                }
            }
        ]
        )
    print('testPush result...', response["message"])

def push(d):
    print('push...')
    try:
        # response = client.chat_postMessage(channel='#random', text="Hello world!")
        response = client.chat_postMessage(
            channel='#demo',
            text="Paper Alert",
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":moneybag: MRR: ${d['summary']['currentMrrK']}k",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": d['summary']['mrrMsg']
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": d['url'],
                        "alt_text": "MRR"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":smiley: Customers: {d['summary']['currentCustomers']}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": d['summary']['customerMsg']
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": d['url'],
                        "alt_text": "MRR"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Open Pulse",
                                "emoji": True
                            },
                            "value": "open_paper",
                            "url": "https://trypaper.io?ref=open_paper",
                            "action_id": "open_paper"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Update Goals",
                                "emoji": True
                            },
                            "value": "set_goals",
                            "url": "https://trypaper.io?ref=set_goals",
                            "action_id": "set_goals"
                        }
                    ]
                },
            ]
        )
        print('push...', response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"slack pints error: {e.response['error']}")