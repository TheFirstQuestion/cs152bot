# bot.py
import discord
from discord.ext import commands
import os
import json
import logging
import re
import requests
from report import Report
import pdb

# Set up logging to the console
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# There should be a file called 'tokens.json' inside the same folder as this file
token_path = 'tokens.json'
if not os.path.isfile(token_path):
    raise Exception(f"{token_path} not found!")
with open(token_path) as f:
    # If you get an error here, it means your token is formatted incorrectly. Did you put it in quotes?
    tokens = json.load(f)
    discord_token = tokens['discord']


class ModBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix='.', intents=intents)
        self.group_num = None
        self.mod_channels = {}  # Map from guild to the mod channel id for that guild
        self.reports = {}  # Map from user IDs to the state of their report

    ############################################## Discord Method Overloads ##############################################
    async def on_ready(self):
        '''
        Called when the client is done preparing the data received from Discord. Usually after login is successful and the Client.guilds and co. are filled up.
        '''
        print(f'{self.user.name} has connected to Discord! It is these guilds:')
        for guild in self.guilds:
            print(f' - {guild.name}')
        print('Press Ctrl-C to quit.')

        # Parse the group number out of the bot's name
        match = re.search('[gG]roup (\d+) [bB]ot', self.user.name)
        if match:
            self.group_num = match.group(1)
        else:
            raise Exception(
                "Group number not found in bot's name. Name format should be \"Group # Bot\".")

        # Find the mod channel in each guild that this bot should report to
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == f'group-{self.group_num}-mod':
                    self.mod_channels[guild.id] = channel

    async def on_message(self, message):
        '''
        This function is called whenever a message is sent in a channel that the bot can see (including DMs). Currently the bot is configured to only handle messages that are sent over DMs or in your group's "group-#" channel.
        '''
        # Ignore messages from the bot
        if message.author.id == self.user.id:
            return

        # Check if this message was sent in a server ("guild") or if it's a DM
        if message.guild:
            await self.handle_channel_message(message)
        else:
            await self.handle_dm(message)

    async def on_raw_reaction_add(self, reaction):
        '''
        Called when a message has a reaction added.
        '''
        # Ignore reactions from the bot
        if reaction.user_id == self.user.id:
            return

        # Check if this message was sent in a server ("guild") or if it's a DM
        if reaction.guild_id:
            # Check if message was sent in the mod channel
            if reaction.channel_id == self.mod_channels[reaction.guild_id].id:
                channel = self.get_channel(reaction.channel_id)
                message = await channel.fetch_message(reaction.message_id)

                # Need to get the reporter id
                # Regex: https://regex101.com/r/2ERBIO/1
                author_id = int(
                    re.search(r"\<@(\d*)\>", message.content).group(1))

                # Only respond to reactions if we are in reporting flow
                if author_id not in self.reports:
                    print("no report for this user")
                    return

                # TODO: probably want to do a thread on the mod side
                # Pass this info to the report, and send response
                report = self.reports[author_id]
                reportResponse = await report.handle_reaction(reaction)
                await self.send_report_response(reportResponse, channel)

        else:
            # DM
            author_id = reaction.user_id

            # Only respond to reactions if we are in reporting flow
            if author_id not in self.reports:
                return

            # Pass this info to the report, and send response
            report = self.reports[author_id]
            reportResponse = await report.handle_reaction(reaction)
            await self.send_report_response(reportResponse, self.get_user(reaction.user_id))

        # Check if the report is complete
        await self.check_report_status(report)
        # TODO: tell users the relevant info

    ####################################################### Handlers #####################################################

    async def handle_dm(self, message):
        # Handle a help message
        if message.content == Report.HELP_KEYWORD:
            reply = "\n\nUse the `report` command to begin the reporting process.\n"
            reply += "Use the `cancel` command to cancel the report process.\n"
            await message.channel.send(reply)
            return

        author_id = message.author.id
        responses = []

        # Only respond to messages if they're part of a reporting flow
        if author_id not in self.reports and not message.content.startswith(Report.START_KEYWORD):
            return

        # If we don't currently have an active report for this user, add one
        if author_id not in self.reports:
            self.reports[author_id] = Report(self, author_id)

        report = self.reports[author_id]

        # TODO: add ability for original message of "report <link>" to start a report with that link

        # Let the report class handle this message; forward all the messages it returns to us
        reportResponse = await report.handle_message(message)
        await self.send_report_response(reportResponse, message.channel)

        # Check if the message is complete
        await self.check_report_status(report)

    async def handle_channel_message(self, message):
        # Only handle messages sent in the "group-#" channel
        if not message.channel.name == f'group-{self.group_num}':
            return

        # Forward the message to the mod channel
        # STEVEN: I commented this out just bc it was annoying
        mod_channel = self.mod_channels[message.guild.id]
        # await mod_channel.send(f'Forwarded message:\n{message.author.name}: "{message.content}"')

        scores = self.eval_text(message.content)
        # await mod_channel.send(self.code_format(scores))

    async def handle_report_complete(self, report):
        # Send the completed report to the mod channel
        # TODO: instead of showing emojis, show what that emoji means
        mod_channel = self.mod_channels[report.message.guild.id]
        report_summary = f'{report.reporter.mention} has reported this message from {report.actor.mention}: {report.message_as_quote()} \n See the message in context: {report.message.jump_url} \n Responses: {" ".join(report.responses)} \n Comments: {report.comment} \n\n'
        report_summary += 'What is the status of this report?\n'
        report_summary += '✅ The message violates community standards and the report was filed *correctly*.\n'
        report_summary += '📝 The message violates community standards but the report was filed *incorrectly*.\n'
        report_summary += '🆙 The report is a serious issue that needs to be escalated to a higher level.\n'
        report_summary += '👍 The reported incident does not violate community standards.'

        report_message = await mod_channel.send(report_summary)

        # Add reactions for the available options
        # Must be same as MOD_STATUS_EMOJIS
        options = ['✅', '📝', '🆙', '👍']
        for option in options:
            await report_message.add_reaction(option)

    async def handle_mod_resolution(self, report):
        # Remove report from map
        self.reports.pop(report.reporter.id)

        # TODO: provide more context/details
        # Send the resolution information to the reporter
        report_summary_reporter = f"Your report has been reviewed."
        report_summary_reporter += f"{report.message_as_quote()}\n"
        report_summary_reporter += f"See the message in context: {report.message.jump_url} \n"
        report_summary_reporter += f"**Outcome: {report.ruling}** \n"
        report_summary_reporter += "You are able to appeal this decision."

        await report.reporter.send(report_summary_reporter)

        # Send the resolution information to the actor
        report_summary_actor = f"Your message has been reported and reviewed:"
        report_summary_actor += f"{report.message_as_quote()}\n"
        report_summary_actor += f"See the message in context: {report.message.jump_url} \n"
        report_summary_actor += f"**Outcome: {report.ruling}**\n"
        report_summary_actor += "You are able to appeal this decision."

        await report.actor.send(report_summary_actor)

    async def check_report_status(self, report):
        if report.report_is_complete():
            await self.handle_report_complete(report)
        if report.report_is_resolved():
            await self.handle_mod_resolution(report)

    ################################################# Helper Functions ##################################################

    def eval_text(self, message):
        ''''
        TODO: Once you know how you want to evaluate messages in your channel,
        insert your code here! This will primarily be used in Milestone 3.
        '''
        return message

    def code_format(self, text):
        ''''
        TODO: Once you know how you want to show that a message has been
        evaluated, insert your code here for formatting the string to be
        shown in the mod channel.
        '''
        return "Evaluated: '" + text + "'"

    async def send_report_response(self, response, channel):
        # Send the bot's response message
        responseText = ""
        for m in response["messages"]:
            responseText += m + "\n"
        botResponse = await channel.send(responseText)

        # Add any bot reactions to the response
        for r in response["reactions"]:
            await botResponse.add_reaction(r)


client = ModBot()
client.run(discord_token)
