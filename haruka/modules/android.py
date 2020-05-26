import urllib

from hurry.filesize import size as sizee
from telethon import custom
from haruka.events import register
from haruka import LOGGER
from haruka.modules.translations.strings import tld

from requests import get
import rapidjson as json


@register(pattern=r"^/magisk$")
async def magisk(event):
    if event.from_id == None:
        return

    url = 'https://raw.githubusercontent.com/topjohnwu/magisk_files/'
    releases = '**Latest Magisk Releases:**\n'
    variant = [
        'master/stable', 'master/beta', 'canary/release', 'canary/debug'
    ]
    for variants in variant:
        fetch = get(url + variants + '.json')
        data = json.loads(fetch.content)
        if variants == "master/stable":
            name = "**Stable**"
            cc = 1
            branch = "master"
        elif variants == "master/beta":
            name = "**Beta**"
            cc = 0
            branch = "master"
        elif variants == "canary/release":
            name = "**Canary**"
            cc = 1
            branch = "canary"
        elif variants == "canary/debug":
            name = "**Canary (Debug)**"
            cc = 1
            branch = "canary"

        releases += f'{name}: [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | ' \
                    f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | '

        if cc == 1:
            releases += f'[Uninstaller]({data["uninstaller"]["link"]}) | ' \
                        f'[Changelog]({url}{branch}/notes.md)\n'
        else:
            releases += f'[Uninstaller]({data["uninstaller"]["link"]})\n'

    await event.reply(releases, link_preview=False)


__help__ = """
 - /magisk: Get latest magisk updates 
 - /app <appname>: Search for an app in playstore 
"""

__mod_name__ = "Android"
