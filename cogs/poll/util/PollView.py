from typing import List
import discord
import matplotlib.pyplot as plt

class PollView(discord.ui.View):
	def __init__(self, title: str, content: List[str], embed: discord.Embed, timeout:int, poll_id:str) -> None:
		self.title = title
		self.content = content
		self.embed = embed
		self.num_polls = len(content)
		self.voted = [[] for i in range(self.num_polls)]
		self.poll_id = poll_id
		super().__init__(timeout=60*timeout)

		# Generate buttons based on how many options
		for i in range(self.num_polls):
			button = discord.ui.Button(
				# TODO Change button label to display number emojis instead
				custom_id=f"{self.poll_id}:{i}",
				style=discord.ButtonStyle.blurple,
			  label=str(i)
			)
			button.callback = self.button_callback
			self.add_item(button)
		
	async def on_timeout(self) -> None:
		# TODO Manually stop the poll
		print(f"Poll {self.poll_id}:{self.title} timed out.")

		# Create a bar plot and save it with the poll id
		count = [len(poll) for poll in self.voted]
		plt.title(label=self.title)
		plt.bar(x=self.content, height=count)
		plt.yticks(ticks=[i for i in range(max(count)+1)])
		plt.savefig(f'{self.poll_id}.png')
		plt.close()
		
		# TODO Clearing buttons does not work??
		self.clear_items()

	async def button_callback(self, interaction: discord.Interaction) -> None:
		# Check to see if the button clicked corresponds with this poll
		id = interaction.data["custom_id"]
		delimiter_idx = id.index(":")
		poll_id = id[:delimiter_idx]
		if (poll_id != self.poll_id):
			return
		button_id = int(id[delimiter_idx+1:])

		# Add or remove the user from the option clicked
		if interaction.user in self.voted[button_id]:
			self.voted[button_id].remove(interaction.user)
		else:
			self.voted[button_id].append(interaction.user)

		# Update the users who voted on this option on the embed
		self.embed.set_field_at(
			index=button_id,
			name=self.embed.fields[button_id].name,
			value=f"**{self.content[button_id]}**\n" + "\n".join(map(lambda user: user.display_name, self.voted[button_id]))
			)
		await interaction.response.edit_message(embed=self.embed)