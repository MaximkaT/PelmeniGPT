import openai


def gptReply(messages):
    """
    :param messages: A list with previous messages and roles of those who have written them
    :return: A reply for the prompt based on previous messages
    """
    history = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
    reply = history.choices[0].message.content
    return reply
