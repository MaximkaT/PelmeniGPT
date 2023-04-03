import openai


def gptReply(messages, user, message):
    try:
        messages[user] += [{'role': 'user', 'content': message}]
    except KeyError:
        messages[user] = []
        messages[user] += [{'role': 'user', 'content': message}]
    history = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages[user])
    reply = history.choices[0].message.content
    messages[user] += [{'role': 'assistant', 'content': reply}]
    return reply
