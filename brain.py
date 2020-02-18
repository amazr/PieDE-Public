import discord
import json
import asyncio
import os
import time
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
#User created files
import stock
import kitty
import ytaudio
import t2s
import convertPiethon

client = discord.Client()
audio_complete_msg = "Finished. Errors: "

@client.event
async def on_ready():
    print("Fired up!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'hi PieDE'.lower() or message.content.lower() == 'hello PieDE'.lower():
        author = message.author.name
        output = "OMG, " + author + " HI HI HI HI!"
        await message.channel.send(output)

    if message.content.startswith('$'):
        symbol = message.content.replace('$', '')
        output = stock.stock(symbol)
        await message.channel.send(output)
        
    if message.content.startswith('alert '):
        symbol = message.content.replace('alert ', '')
        output = stock.alert(symbol)
        await message.channel.send(output)

    if message.content == '!kitty' or message.content == '!cat':
        kitty.getCatLink()
        await message.channel.send(file=discord.File('img/temp-cat.jpg'))

    #WORK IN PROGRESS
    if message.content.startswith('!t2s'):
        translate = message.content[5:]
        t2s.synthesize_ssml(translate)
        channel = message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('output.mp3'), after=lambda e: print(audio_complete_msg, e))

    if message.content.startswith('!sax'):
        channel = message.author.voice.channel
        vc = await channel.connect()
        await message.channel.send(file=discord.File('preload/saxgif.gif'))
        time.sleep(0.5)
        vc.play(discord.FFmpegPCMAudio('preload/sax.mp3'), after=lambda e: print(audio_complete_msg, e))
        time.sleep(8)
        await message.channel.purge(limit=1, check=is_me)
        guild = message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
    
    if message.content.startswith('!play'):
        channel = message.author.voice.channel
        await message.delete()
        await message.channel.send("Playing...")
        url = ""
        url = message.content[6:]
        if url != "":
            ytaudio.createAudio(url)
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('temp-audio.mp3'), after=lambda e: print(audio_complete_msg, e))

    if message.content.startswith('!code'):
        wf = open("userUploadPie.py", "w")
        wf.write(message.content[5:])
        wf.close()

        output = convertPiethon.convert()
        
        for i in output:
            await message.channel.send(i)

    if message.content == '!leave':
        guild = message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()

@client.event
async def on_typing(channel, user, when):
    if user.name == "sophiajb":
        await channel.send("I'm SORRY??")


def is_me(m):
    return m.author == client.user

async def disconnect_voice(channel, e):
    print(audio_complete_msg, e)
    await channel.disconnect()

client.run('bot key here')