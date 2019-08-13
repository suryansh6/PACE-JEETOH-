 
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent
import datetime


BOT_OWNER_ROLE = 'RUNNER' # change to what you need
#BOT_OWNER_ROLE_ID = "544387608378343446"
  
 

 
oot_channel_id_list = ["609549355132911646",#galaxy
"593070663548403743",
"593990638329004032",
"595636121124208640",
"609405527335763971"

]


answer_pattern = re.compile(r'(not|n)?([1-4]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)
print(answer_pattern)
apgscore = 2450
nomarkscore = 1860
markscore = 1700

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Nelson Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="Trivia Plus", description="**Answer Choice**",color=0x98FB98)
        self.embed.set_author(name ='',url=' ',icon_url='')
        self.embed.add_field(name="Option I", value="0", inline=False)
        self.embed.add_field(name="Option II", value="0", inline=False)
        self.embed.add_field(name="Option III", value="0", inline=False)
        self.embed.add_field(name="Option III", value="0", inline=False)
        self.embed.add_field(name="option 5",value="0")
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/583982556349857812/595644489301753907/JPEG_20190702_210236.jpg")
        self.embed.set_footer(text=f"zlex#0168", \
            icon_url="https://cdn.discordapp.com/attachments/583982556349857812/595644489301753907/JPEG_20190702_210236.jpg")
        # await bot.add_reaction(message = "self.embed",emoji = ":wink")
        # await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):

         

        one_check = ""
        two_check = ""
        three_check = ""
        four_check=""
        bold1=""
        bold2=""
        bold3=""
        bold4=""
        line1=""
        line2=""
        line3=""
        

        lst_scores = list(self.answer_scores)

        highest = max(lst_scores)
#         lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        best_answer=":hourglass_flowing_sand:"
        if highest >0:
          if answer ==1:
            one_check="```"
            best_answer=":regional_indicator_a:"
          if answer==1:
            bold1=""
          else:
            bold1=":x:"
          if answer ==2:
            two_check="```"
            best_answer=":regional_indicator_b:"
          if answer ==2:
            bold2=""
          else:
            bold2=":x:"
          
          if answer ==3:
            three_check="```"
            best_answer=":regional_indicator_c:"
          if answer ==3:
            bold3=""
          else:
            bold3=":x:"
            
          if answer==4:
          	four_check="```"
          	best_answer=":regional_indicator_d:"
          	
          if answer==4:
          	bold4=""
          else:
          	bold4=":x:"
 #add your games deailts and server name etc. what you need you can change         
			
        self.embed=discord.Embed(title="**__TRIVIA NATION 2.0__**\n\n**__CONNECTING TO JEETOH__**......", description=f"**__OPTION A__**\n{one_check}{lst_scores[0]}{one_check}{bold1}\n\n**__OPTION B__**\n{two_check}{lst_scores[1]}{two_check}{bold2}\n\n**__OPTION C__**\n{three_check}{lst_scores[2]} {three_check}{bold3}\n\n**__OPTION D__**\n{four_check}{lst_scores[3]}{four_check}{bold4}\n\n**__BEST ANSWER__**\n\n{best_answer}\n",color=0x98FB98)
        self.embed.set_footer(text=f"KESHAV RAJ ᴳᵒᵈ#7735",icon_url="https://cdn.discordapp.com/attachments/609581567135842314/609937606964281365/JPEG_20190811_080005.jpg")

        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Nelson Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()

        await asyncio.sleep(5)
        await self.change_presence(activity=discord.Activity(type=1,name='with JEETOH.'))
        await asyncio.sleep(5)
#here add status of bot
    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return
#thats is command lo
        if message.content.lower() == "+j":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction("<:emoji_3:609588150976905216>")
                # await self.embed_msg.add_reaction(":white_check_mark:")
                await self.embed_msg.add_reaction("<:emoji_4:609588641358151698>")
                     
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**Lol** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            return

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NjA5Njg4NzIxNzcxNzI0ODE5.XU64Vw.5h41JE3UUg6IHdPgwPrKs47iZTs'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NTY4MjU1NDk4MTQ3ODU2Mzg1.XRHU4Q.hx4iPVIytfjjQ52jxYX7SyuKTOw',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=4)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
