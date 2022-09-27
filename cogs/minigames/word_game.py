# Clone of the game wordle

from discord.ext import commands

class WordGame(commands.Cog, name="Word Game"):
    """Plays the word game that is similar to Wordle"""

    def __init__(self, bot):
        self.bot = bot
        self.word = "jeans"
        self.round = -1
        self.current_progress = []


    def checkword(word, checked_word):
        """Compare current word to checked word"""
        currentlist = []
        letterdict = dict()
        for i in range(0, len(checked_word)):
            currentlet = checked_word[i].lower()
            if currentlet in letterdict.keys():
                letterdict[currentlet] += 1
            else:
                letterdict[currentlet] = 1

        for i in range(0, len(word)):
            currentlet = word[i].lower()
            comparedlet = word[i].lower()

            if currentlet == comparedlet:
                currentlist.append("G")
                letterdict[word[i]] -= 1
            else:
                if currentlet in checked_word.lower() and letterdict[currentlet] > 0:
                    currentlist.append("Y")
                    letterdict[comparedlet] -= 1
                else:
                    currentlist.append("B")
        
        return currentlist

    @commands.command()
    async def getword(self, ctx):
        """Returns the test word. FOR DEBUG ONLY!"""
        await ctx.send(self.word)

    ######################################################################
    #   !startGame
    ######################################################################

    @commands.command()
    async def start_game(self, ctx):
        """Starts the word game."""
        if (self.round >= 0):
            await ctx.send("Game already started!")
        else:
            self.round = 0
            # TODO: Add multiple words
            await ctx.send("Game Started!")

    ######################################################################
    #   !addWord
    ######################################################################

    

    ######################################################################
    #   !endGame
    ######################################################################

    @commands.command()
    async def end_game(self, ctx):
        """Ends the word game if not started"""
        if (self.round >= 0):
            self.round = -1
            self.current_progress = []
            await ctx.send("Game ended! The word was " + self.word)
        else:
            await ctx.send("The game hasn't started!")

    ######################################################################
    #   !checkStatus
    ######################################################################

async def setup(bot):
    await bot.add_cog(WordGame(bot))