import openai


def gptReply(messages, user, message):
    """
    :param messages: A dictionary with previous messages and roles of those who have written them
    :param user: User's discord name
    :param message: Prompt that requires a reply
    :return: A reply for the prompt based on previous messages
    """
    try:
        messages[user] += [{'role': 'user', 'content': message}]
    except KeyError:
        messages[user] = []
        messages[user] += [{'role': 'user', 'content': message}]
    history = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages[user])
    reply = history.choices[0].message.content
    messages[user] += [{'role': 'assistant', 'content': reply}]
    return reply
