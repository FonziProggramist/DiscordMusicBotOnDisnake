import disnake
from disnake.ext import commands


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = disnake.Embed(title="Успешно",
                              description="!help - отображает все доступные команды\n!p - находит песню на youtube и проигрывает ее на вашем текущем канале. Возобновляет проигрывание текущей песни, если она была поставлена на паузу\n!q - отображает текущую очередь музыки\n!skip - пропускает текущую проигрываемую песню\n!clear - останавливает музыку и очищает очередь\n!leave - отключает бота от голосового канала\n!pause - приостанавливает проигрывание текущей песни или возобновляет, если она уже поставлена на паузу\n!resume - возобновляет проигрывание текущей песни.",
                              color=disnake.Color.green())
        await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(help(client))