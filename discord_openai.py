import discord
import openai

# client = discord.Client()

# Create an Intents object to specify which events the bot should listen to
intents = discord.Intents.all()
intents.members = False

# Create a Discord client
client = discord.Client(intents=intents)

openai.api_key = "openapi-key"

def generate_response(input_text):
  try:
    completions = openai.Completion.create(
      engine="text-davinci-003",
      prompt=input_text,
      max_tokens=2048,
      n=1,
      temperature=0.5,
    )
  except openai.api_errors.ApiError as e:
    print(f'Error generating response: {e}')
    return ''

  if len(completions.choices) == 0:
    print('Error: No choices returned')
    return ''

  message = completions.choices[0].text
  return message

@client.event
async def on_message(message):
  # Ignore messages from the bot itself
  if message.author == client.user:
    return

  input_text = message.content
  response = generate_response(input_text)

  if not response:
    print(f'Error: Empty response for input "{input_text}"')
    return

  try:
    await message.channel.send(response)
  except discord.errors.HTTPException as e:
    print(f'Error sending message: {e}')

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
client.run('discord-key')