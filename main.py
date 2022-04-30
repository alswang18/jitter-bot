import discord
import newspaper
from newspaper import Article
import nltk
from symbl import generate_payload, send_for_analysis, get_results
import os

nltk.download("punkt")

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN","")

client = discord.Client()

client.notes = False


@client.event
async def on_ready():
    print("bot is ready")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.notes:
        client.speakers.append(str(message.author))
        client.names.append(str(message.author).split("#")[0])
        client.messages.append(message.content)
    else:
        client.speakers = []
        client.names = []
        client.messages = []
    if message.content.startswith(
        #bot user id
        "<@969794010862485554>"
    ) or message.content.startswith("<@&969795384371208245>"):
        statement = message.content.split(" ")
        if len(statement) == 1:
            await message.channel.send(
                "Hey how can I help you? Run `@jitter_bot help` for some commands."
            )
        elif statement[1].lower() == "help":
            await message.channel.send(
                """
You can try our news module:
`@jitter_bot news <URL>`
`@jitter_bot news website <Website_Url>`
`@jitter_bot take-note` to have jitter bot record the convo then run `@jitter_bot parse-note` then `@jitter_bot note-summary` to get the summary of notes.
                """
            )
        elif statement[1].lower() == "news":
            if statement[2].lower() == "website":
                # print(statement[3])
                paper = newspaper.build(statement[3])
                for art in paper.articles:
                    article = Article(art.url)
            else:
                article = Article(statement[2])
            article.download()
            article.parse()
            article.nlp()
            await message.channel.send(article.summary)
        elif statement[1].lower() == "take-note":
            client.speakers = []
            client.names = []
            client.messages = []
            client.notes = True
            return
        elif statement[1].lower() == "parse-note":
            client.notes = False
            payload = generate_payload(client.speakers, client.names, client.messages)
            analysis = send_for_analysis(payload)
            client.convo_id = analysis["conversationId"]

        elif statement[1].lower() == "note-summary":
            if client.notes:
              await message.channel.send("There is no text that has been parsed")
            res = get_results(client.convo_id)["summary"]
            if len(res) == 0:
              await message.channel.send("The summary is being prepared")
            else:
              await message.channel.send(res[0]['text'])
        else:
            await message.channel.send(
                "I don't understand that command. Run `@jitter_bot help` for some commands."
            )
client.run(os.environ.get("DISCORD_TOKEN", ""))
