import time
import requests
import disnake
from disnake.ext import commands
from openai.error import *
from config import *
from PILimage import *


class ImageCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.images_urls = {}
        self.bot = bot

    def images_add(self, user_id, prompt):
        if user_id not in self.images_urls:
            self.images_urls[user_id] = []
        self.images_urls[user_id].extend(prompt)

    @commands.slash_command()
    async def image(self, inter: disnake.ApplicationCommandInteraction, prompt):
        await inter.response.defer()
        user_id = inter.user.id
        try:
            self.images_urls[user_id].clear()
        except KeyError:
            pass
        filename = f'{inter.user.name}{prompt[:5]}'
        images = []
        try:
            response = openai.Image.create(prompt=prompt, n=4, size="1024x1024")['data']
        except RateLimitError:
            await inter.edit_original_message('Try again after 1 min')
            return
        except InvalidRequestError:
            await inter.edit_original_message('This word banned')
            return
        for r in response:
            images.append(r['url'])
        self.images_add(user_id, images)
        print(self.images_urls[user_id])
        create_image(self.images_urls[user_id], filename)
        await inter.edit_original_message(
            file=disnake.File(f'{filename}.jpg'),
            components=[
                disnake.ui.Button(label="V1", style=disnake.ButtonStyle.gray, custom_id="1"),
                disnake.ui.Button(label="V2", style=disnake.ButtonStyle.gray, custom_id="2"),
                disnake.ui.Button(label="V3", style=disnake.ButtonStyle.gray, custom_id="3"),
                disnake.ui.Button(label="V4", style=disnake.ButtonStyle.gray, custom_id="4"),
            ],
        )

    @commands.slash_command()
    async def blender(self, inter: disnake.ApplicationCommandInteraction, prompt1, prompt2):
        await inter.response.defer()
        filename = f'{inter.user.name}{time.time()}.jpg'
        is_prompt1_url = False
        is_prompt2_url = False

        if prompt1.startswith('http'):
            try:
                response = requests.get(prompt1)
                response.raise_for_status()
                is_prompt1_url = True
            except (requests.RequestException, OSError):
                pass

        if prompt2.startswith('http'):
            try:
                response = requests.get(prompt2)
                response.raise_for_status()
                is_prompt2_url = True
            except (requests.RequestException, OSError):
                pass

        if is_prompt1_url and is_prompt2_url:
            blender(prompt1, prompt2, filename)
            await inter.edit_original_message(file=disnake.File(filename))
        elif is_prompt1_url:
            try:
                image = openai.Image.create(prompt=prompt2)['data'][0]['url']
            except RateLimitError:
                await inter.edit_original_message('Try again after 1 min')
                return
            except InvalidRequestError:
                await inter.edit_original_message('This word banned')
                return
            blender(image, prompt1, filename)
            await inter.edit_original_message(file=disnake.File(filename))
        elif is_prompt2_url:
            try:
                image = openai.Image.create(prompt=prompt1)['data'][0]['url']
                print(image)
            except RateLimitError:
                await inter.edit_original_message('Try again after 1 min')
                return
            except InvalidRequestError:
                await inter.edit_original_message('This word banned')
                return
            blender(image, prompt2, filename)
            await inter.edit_original_message(file=disnake.File(filename))
        else:
            await inter.edit_original_message('at least one parameter must be a url')

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        user_id = inter.user.id
        if inter.component.custom_id not in ["1", "2", "3", "4"]:
            return

        else:
            await inter.response.send_message(self.images_urls[user_id][int(inter.component.custom_id) - 1])


def setup(bot: commands.Bot):
    bot.add_cog(ImageCommand(bot))

