import random, re, string, io, asyncio
from PIL import Image
from io import BytesIO
import base64
from spongemock import spongemock
from zalgo_text import zalgo
import os
from pathlib import Path
import glob

import nltk # shitty lib, but it does work
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from typing import Optional, List
from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async
from deeppyer import deepfry

from haruka import dispatcher, DEEPFRY_TOKEN, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

# D A N K modules by @deletescape vvv


@run_async
def owo(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        faces = ['(・`ω´・)',';;w;;','owo','UwU','>w<','^w^','\(^o\) (/o^)/','( ^ _ ^)∠☆','(ô_ô)','~:o',';____;', '(*^*)', '(>_', '(♥_♥)', '*(^O^)*', '((+_+))']
        reply_text = re.sub(r'[rl]', "w", message.reply_to_message.text)
        reply_text = re.sub(r'[ｒｌ]', "ｗ", message.reply_to_message.text)
        reply_text = re.sub(r'[RL]', 'W', reply_text)
        reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
        reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
        reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
        reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
        reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
        reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
        reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
        reply_text += ' ' + random.choice(faces)
        message.reply_to_message.reply_text(reply_text)

@run_async
def copypasta(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        emojis = ["😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
        reply_text = random.choice(emojis)
        b_char = random.choice(message.reply_to_message.text).lower() # choose a random character in the message to be substituted with 🅱️
        for c in message.reply_to_message.text:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(emojis)
        message.reply_to_message.reply_text(reply_text)


@run_async
def bmoji(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        b_char = random.choice(message.reply_to_message.text).lower() # choose a random character in the message to be substituted with 🅱️
        reply_text = message.reply_to_message.text.replace(b_char, "🅱️").replace(b_char.upper(), "🅱️")
        message.reply_to_message.reply_text(reply_text)


@run_async
def clapmoji(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        reply_text = "👏 "
        reply_text += message.reply_to_message.text.replace(" ", " 👏 ")
        reply_text += " 👏"
        message.reply_to_message.reply_text(reply_text)



@run_async
def stretch(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        count = random.randint(3, 10)
        reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message.reply_to_message.text)
        message.reply_to_message.reply_text(reply_text)


@run_async
def vapor(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    if not message.reply_to_message:
        if not args:
            message.reply_text("I need a message to convert to vaporwave text.")
        else:
            noreply = True
            data = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        noreply = False
        data = message.reply_to_message.text
    else:
        data = ''

    reply_text = str(data).translate(WIDE_MAP)
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)

# D A N K modules by @deletescape ^^^
# Less D A N K modules by @skittles9823 # holi fugg I did some maymays vvv

@run_async
def mafiatext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "Give some text to meme !")

    if not Path('/root/haruka/images/mafia.jpg').is_file():
        LOGGER.warning(
            "/root/haruka/images/mafia.jpg not found! Mafia memes module is turned off!")
        return

    for mocked in glob.glob("/root/haruka/mafiaed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    
    magick = """convert /root/haruka/images/mafia.jpg -font Open-Sans -pointsize 50 -size 1280x720 -stroke white -strokewidth 1 -fill black -background none -gravity north caption:"{}" -flatten /root/haruka/mafiaed.jpg""".format(
        reply_text)
    os.system(magick)
    with open('/root/haruka/mafiaed.jpg', 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('/root/haruka/mafiaed.jpg')


@run_async
def pidortext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "Give some text to meme !")

    if not Path('/root/haruka/images/4pda.jpg').is_file():
        LOGGER.warning(
            "/root/haruka/images/4pda.jpg not found! Pidor memes module is turned off!")
        return
    for mocked in glob.glob("/root/haruka/4pdaed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    
    magick = """convert /root/haruka/images/4pda.jpg -font Open-Sans -pointsize 50 -size 400x300 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten /root/haruka/4pdaed.jpg""".format(
        reply_text)
    os.system(magick)
    with open('/root/haruka/4pdaed.jpg', 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('/root/haruka/4pdaed.jpg')


@run_async
def kimtext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "Give some text to meme !")

    if not Path('/root/haruka/images/kim.jpg').is_file():
        LOGGER.warning(
            "/root/haruka/images/kim.jpg not found! Kim memes module is turned off!")
        return
    for mocked in glob.glob("/root/haruka/kimed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    
    magick = """convert /root/haruka/images/kim.jpg -font Open-Sans -pointsize 50 -size 480x360 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten /root/haruka/kimed.jpg""".format(
        reply_text)
    os.system(magick)
    with open('/root/haruka/kimed.jpg', 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('/root/haruka/kimed.jpg')


@run_async
def hitlertext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "Give some text to meme !")

    if not Path('/root/haruka/images/hitler.jpg').is_file():
        LOGGER.warning(
            "/root/haruka/images/hitler.jpg not found! Hitler memes module is turned off!")
        return
    for mocked in glob.glob("/root/haruka/hitlered*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    
    magick = """convert /root/haruka/images/hitler.jpg -font Open-Sans -pointsize 50 -size 615x409 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten /root/haruka/hitlered.jpg""".format(
        reply_text)
    os.system(magick)
    with open('/root/haruka/hitlered.jpg', 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('/root/haruka/hitlered.jpg')


@run_async
def spongemocktext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "Give some text to meme !")

    if not Path('/root/haruka/images/bob.jpg').is_file():
        LOGGER.warning(
            "/root/haruka/images/bob.jpg not found! Spongemock memes module is turned off!")
        return
    for mocked in glob.glob("/root/haruka/mocked*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    
    magick = """convert /root/haruka/images/bob.jpg -font Open-Sans -pointsize 30 -size 512x300 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten /root/haruka/mocked.jpg""".format(
        reply_text)
    os.system(magick)
    with open('/root/haruka/mocked.jpg', 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('/root/haruka/mocked.jpg')


@run_async
def zalgotext(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = str('Insolant human, you must reply to something to zalgofy it!')

    reply_text = zalgo.zalgo().zalgofy(data)
    message.reply_text(reply_text)

# Less D A N K modules by @skittles9823 # holi fugg I did some maymays ^^^
# shitty maymay modules made by @divadsn vvv

@run_async
def forbesify(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = ''

    data = data.lower()
    accidentals = ['VB', 'VBD', 'VBG', 'VBN']
    reply_text = data.split()
    offset = 0

    # use NLTK to find out where verbs are
    tagged = dict(nltk.pos_tag(reply_text))

    # let's go through every word and check if it's a verb
    # if yes, insert ACCIDENTALLY and increase offset
    for k in range(len(reply_text)):
        i = reply_text[k + offset]
        if tagged.get(i) in accidentals:
            reply_text.insert(k + offset, 'accidentally')
            offset += 1

    reply_text = string.capwords(' '.join(reply_text))
    message.reply_to_message.reply_text(reply_text)


@run_async
def deepfryer(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.photo
        data2 = message.reply_to_message.sticker
    else:
        data = []
        data2 = []

    # check if message does contain media and cancel when not
    if not data and not data2:
        message.reply_text("What am I supposed to do with this?!")
        return

    # download last photo (highres) as byte array
    if data:
        photodata = data[len(data) - 1].get_file().download_as_bytearray()
        image = Image.open(io.BytesIO(photodata))
    elif data2:
        sticker = bot.get_file(data2.file_id)
        sticker.download('sticker.png')
        image = Image.open("sticker.png")

    # the following needs to be executed async (because dumb lib)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(process_deepfry(image, message.reply_to_message, bot))
    loop.close()

async def process_deepfry(image: Image, reply: Message, bot: Bot):
    # DEEPFRY IT
    image = await deepfry(
        img=image,
        token=DEEPFRY_TOKEN,
        url_base='westeurope'
    )

    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')

    # send it back
    bio.seek(0)
    reply.reply_photo(bio)
    if Path("sticker.png").is_file():
        os.remove("sticker.png")

# shitty maymay modules made by @divadsn ^^^


@run_async
def shout(bot: Bot, update: Update, args):
    if len(args) == 0:
        update.effective_message.reply_text("Where is text?")
        return

    msg = "```"
    text = " ".join(args)
    result = []
    result.append(' '.join([s for s in text]))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")


# no help string
__help__ = """
Some memes command, find it all out yourself!

/owo: OWO de text
/stretch: STRETCH de text
/clapmoji: Type in reply to a message and see magic
/bmoji: Type in reply to a message and see magic
/copypasta: Type in reply to a message and see magic
/vapor: owo vapor dis
/hitler: Quote a message and type this command to make a caption of hitler
/mock: Does the same as /hitler but spongemock instead
/kim: Does the same as /hitler but with Kim Jong Un instead (O no plox dont bomb my house)
/pidor: 4pda memes
/forbesify: Correct your punctuations better use the advanged spell module 
/shout: Write anything that u want it to should
/zalgofy: reply to a message to g̫̞l̼̦i̎͡tͫ͢c̘ͭh̛̗ it out!
"""

__mod_name__ = "Memes"
COPYPASTA_HANDLER = DisableAbleCommandHandler("copypasta", copypasta, admin_ok=True)
CLAPMOJI_HANDLER = DisableAbleCommandHandler("clapmoji", clapmoji, admin_ok=True)
BMOJI_HANDLER = DisableAbleCommandHandler("bmoji", bmoji, admin_ok=True)
OWO_HANDLER = DisableAbleCommandHandler("owo", owo, admin_ok=True)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor", vapor, pass_args=True, admin_ok=True)
MOCK_HANDLER = DisableAbleCommandHandler("mock", spongemocktext, admin_ok=True, pass_args=True)
KIM_HANDLER = DisableAbleCommandHandler("kim", kimtext, admin_ok=True, pass_args=True)
MAFIA_HANDLER = DisableAbleCommandHandler("mafia", mafiatext, admin_ok=True, pass_args=True)
PIDOR_HANDLER = DisableAbleCommandHandler("pidor", pidortext, admin_ok=True, pass_args=True)
HITLER_HANDLER = DisableAbleCommandHandler("hitler", hitlertext, admin_ok=True, pass_args=True)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext)
FORBES_HANDLER = DisableAbleCommandHandler("forbes", forbesify, admin_ok=True)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry", deepfryer, admin_ok=True)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, pass_args=True)
FORBES_HANDLER = DisableAbleCommandHandler("forbesify", forbesify, admin_ok=True)

dispatcher.add_handler(MAFIA_HANDLER)
dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(CLAPMOJI_HANDLER)
dispatcher.add_handler(BMOJI_HANDLER)
dispatcher.add_handler(PIDOR_HANDLER)
dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(FORBES_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(ZALGO_HANDLER)
dispatcher.add_handler(FORBES_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER)
dispatcher.add_handler(KIM_HANDLER)
dispatcher.add_handler(HITLER_HANDLER)

