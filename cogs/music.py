import disnake
from disnake.ext import commands

from youtube_dl import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(disnake.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    embed = disnake.Embed(title="Ошибка", description="Я не могу подключится к голосовому каналу!", color=disnake.Color.red())
                    await ctx.reply(embed=embed)
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(disnake.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"])
    async def play(self, ctx, *args):
        if  ctx.author.voice is None:
            embed6546546=disnake.Embed(title="Ошибка", description=f"Подключитесь к голосовому каналу! {ctx.author.mention}", color=disnake.Color.red())
            await ctx.reply(embed=embed6546546)
        else:
            query = " ".join(args)

            voice_channel = ctx.author.voice.channel
            if voice_channel is None:

                embed1 = disnake.Embed(title="Ошибка",
                                       description=f"Подключитесь к голосовому каналу! {ctx.author.mention}",
                                       color=disnake.Color.red())
                await ctx.reply(embed=embed1)
            elif self.is_paused:
                self.vc.resume()
            else:
                song = self.search_yt(query)
                if type(song) == type(True):
                    embed2 = disnake.Embed(title="Ошибка",
                                           description=f"Не удалось загрузить песню. Неправильный формат Попробуйте другое ключевое слово. Это может быть связано с плейлистом или форматом livestream. {ctx.author.mention}",
                                           color=disnake.Color.red())
                    await ctx.reply(embed=embed2)
                else:
                    embed3 = disnake.Embed(title="Успешно",
                                           description=f"Песня добавлен в очередь! {ctx.author.mention}",
                                           color=disnake.Color.green())
                    await ctx.reply(embed=embed3)
                    self.music_queue.append([song, voice_channel])

                    if self.is_playing == False:
                        await self.play_music(ctx)

    @commands.command(name="pause")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"])
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"])
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()

            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"])
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):

            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            embed5 = disnake.Embed(title="Успешно", description=retval, color=disnake.Color.green())
            await ctx.reply(embed=embed5)
        else:
            embed4 = disnake.Embed(title="Ошибка", description=f'Музыки нету в очереде! {ctx.author.mention}', color=disnake.Color.red())
            await ctx.reply(embed=embed4)

    @commands.command(name="clear", aliases=["c", "bin"])
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        embed6 = disnake.Embed(title="Успешно", description=f"Музыка в очереде очищен! {ctx.author.mention}", color=disnake.Color.green())
        await ctx.reply(embed=embed6)

    @commands.command(name="leave", aliases=["disconnect", "l", "d"])
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

def setup(client):
    client.add_cog(music_cog(client))