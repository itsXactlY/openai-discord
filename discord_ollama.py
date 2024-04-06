import discord
import openai
import os

# Create an Intents object to specify which events the bot should listen to
intents = discord.Intents.all()
intents.members = True

# Create a Discord client
client = discord.Client(intents=intents)

import ollama

def generate_ollama_response(input_text):
    response = ollama.chat(model='stable-code', messages=[{'role': 'user', 'content': input_text}])
    return response['message']['content']

async def send_response(message, response):
    try:
        if len(response) > 2000:
            with open("response.txt", "w", encoding="utf-8") as file:
                file.write(response)
            await message.channel.send(file=discord.File("response.txt"))
            os.remove("response.txt")
        else:
            await message.channel.send(response)
    except discord.errors.HTTPException as e:
        print(f'Error sending message: {e}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself and messages without a "!" prefix
    if message.author == client.user or not message.content.startswith('!'):
        return

    input_text = message.content
    response = generate_ollama_response(input_text)

    if not response:
        print(f'Error: Empty response for input "{input_text}"')
        return

    await send_response(message, response)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

client.run('<discord_OAUTH_token>')
