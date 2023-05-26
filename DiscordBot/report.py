from enum import Enum, auto
import discord
import re


class State(Enum):
    REPORT_START = auto()
    AWAITING_MESSAGE = auto()
    MESSAGE_IDENTIFIED = auto()
    MESSAGE_CLASSIFIED = auto()
    WAITING_ON_SECONDARY_CLASSIFICATION = auto()
    WAITING_ON_MESSAGE = auto()
    REPORT_COMPLETE = auto()
    REPORT_CANCELLED = auto()
    RESOLVED_BY_MOD = auto()

    # Daniel edits:
    BULLYING_TYPE_IDENTIFIED = auto()
    DANGER_IDENTIFIED = auto()
    WAITING_ON_BLOCK = auto()
    BLOCK_CHOSEN = auto()


CLASSIFICATION_EMOJIS = ["💩", "👿", "💳", "🔪", "✍️", "🙅"]
SECONDARY_CLASSIFICATION_EMOJIS = ["🧛", "🕵", "🦹"]
DANGER_EMOJIS = ["❌", "⭕️"]
BLOCK_EMOJIS = ["❌", "⭕️"]
DM_SETTING_EMOJIS = ["❌", "⭕️"]

# TODO: make a util function for how to format reports, so consistent for user + mod


class Report:
    START_KEYWORD = "report"
    CANCEL_KEYWORD = "cancel"
    HELP_KEYWORD = "help"

    def __init__(self, client, reporter):
        self.state = State.REPORT_START
        self.client = client
        self.message = None
        self.comment = "None."
        self.responses = []
        self.reporter = client.get_user(reporter)
        self.actor = None

    async def handle_message(self, message):
        '''
        This function makes up the meat of the user-side reporting flow. It defines how we transition between states and what prompts to offer at each of those states.
        Returns a dict with keys "messages" and "reactions". Corresponding value is an array of strings of that type.
        '''

        if message.content == self.CANCEL_KEYWORD:
            self.state = State.REPORT_CANCELLED
            return {"messages": ["Report cancelled."], "reactions": []}

        if self.state == State.REPORT_START:
            reply = "\nThank you for starting the reporting process. "
            reply += "Say `help` at any time for more information.\n\n"
            reply += "Please copy paste the link to the message you want to report.\n"
            reply += "You can obtain this link by right-clicking the message and clicking `Copy Message Link`."
            self.state = State.AWAITING_MESSAGE
            return {"messages": [reply], "reactions": []}

        # We don't yet have a message
        if self.state == State.AWAITING_MESSAGE:
            # Do some error checking...
            # Parse out the three ID strings from the message link
            m = re.search('/(\d+)/(\d+)/(\d+)', message.content)
            if not m:
                return {"messages": ["I'm sorry, I couldn't read that link. Please try again or say `cancel` to cancel."], "reactions": []}

            guild = self.client.get_guild(int(m.group(1)))
            if not guild:
                return {"messages": ["I cannot accept reports of messages from guilds that I'm not in. Please have the guild owner add me to the guild and try again, or say `cancel` to cancel."], "reactions": []}

            channel = guild.get_channel(int(m.group(2)))
            if not channel:
                return {"messages": ["It seems this channel was deleted or never existed. Please try again or say `cancel` to cancel."], "reactions": []}

            try:
                message = await channel.fetch_message(int(m.group(3)))
            except discord.errors.NotFound:
                return {"messages": ["It seems this message was deleted or never existed. Please try again or say `cancel` to cancel."], "reactions": []}

            # Begin the reporting flow: get information about the type of abuse
            self.state = State.MESSAGE_IDENTIFIED
            self.message = message
            self.actor = message.author

            return {
                "messages": [f"You are reporting this message from {self.actor.mention}:", f"```{self.actor.name}: {self.message.content}```", "Why are you reporting this message? \n",
                             "💩 This message contains content that is inappropriate for this context and people shouldn't see it.",
                             "👿 This message is harassment, bullying, or generally mean or hurtful.",
                             "💳 I think that this is a spam message or a scam, not a real person genuinely trying to interact.",
                             "🔪 I think this message could lead to bad stuff happening offline.",
                             "✍️ None of these, some other reason.",
                             "🙅 I didn't mean to report this message! No action needed."],
                "reactions": CLASSIFICATION_EMOJIS}

        if self.state == State.WAITING_ON_MESSAGE:
            self.comment = message.content
            self.state = State.REPORT_COMPLETE
            return {"messages": ["We have received your report. Our moderation team will review the and notify you of the outcome  of the review."], "reactions": []}

        # Base case -- something has gone wrong if we reach this
        self.state = State.REPORT_CANCELLED
        return {"messages": ["I'm sorry, something has gone wrong. Please report this error."], "reactions": ["😭"]}

    async def handle_reaction(self, reaction):
        emoji = reaction.emoji.name
        # First-level classification (identify as person being mean)
        if self.state == State.MESSAGE_IDENTIFIED and emoji in CLASSIFICATION_EMOJIS:
            self.responses.append(emoji)
            if emoji == "🙅":
                self.state = State.REPORT_CANCELLED
                return {"messages": ["Your report has been cancelled. Have a nice day!"], "reactions": []}

            if emoji == "✍️":
                self.state = State.WAITING_ON_MESSAGE
                return {"messages": ["Please help us understand why this message may violate our policies. Your message will be sent to our moderation team for review."], "reactions": []}
            if emoji == "👿":
                self.state = State.WAITING_ON_SECONDARY_CLASSIFICATION
                return {"messages": ["Please tell us more about what is happening.",
                                     "🧛 This person or message is intimidating or physically threatening.",
                                     "🕵 This person or message is invading my privacy (stalking, doxxing, revealing of personal information). ",
                                     "🦹 This person or message is otherwise mean, abusive, or making me uncomfortable."],
                        "reactions": SECONDARY_CLASSIFICATION_EMOJIS}
            self.state = State.REPORT_COMPLETE
            return {"messages": ["We have received your report. Our moderation team will review the report and notify you of the outcome  of the review."], "reactions": []}

        # Second-level classification (identify as cyberbullying)
        if self.state == State.WAITING_ON_SECONDARY_CLASSIFICATION and emoji in SECONDARY_CLASSIFICATION_EMOJIS:
            self.responses.append(emoji)
            self.state = State.REPORT_COMPLETE
            return {"messages": ["Nice!"], "reactions": []}

        # Hopefully this doesn't happen
        self.state = State.REPORT_CANCELLED
        return {"messages": ["I'm sorry, something has gone wrong. Please report this error."], "reactions": ["😭"]}

    async def handle_imminent_danger(self, danger):
        emoji = danger.emoji.name
        if self.state == State.BULLYING_TYPE_IDENTIFIED and emoji in DANGER_EMOJIS:
            if emoji == "❌":
                self.state = State.DANGER_IDENTIFIED
                return {"messages": ["We have received your report. Our moderation team will review this message and notify you of the outcome  of the review.The reported post may be removed; and the account posting violating messages may be suspended. Your report may be sent to local law enforcement authorities where necessary."], "reactions": []}
            elif emoji == "⭕️":
                self.state = State.DANGER_IDENTIFIED
                return {"messages": ["Please help us understand why this message may violate our policies. Your message will be sent to our moderation team for review."], "reactions": []}

        return {"messages": ["I'm sorry, something has gone wrong. Please report this error."], "reactions": ["😭"]}

    async def handle_block(self, block):
        emoji = block.emoji.name
        if self.state == State.DANGER_IDENTIFIED and emoji in BLOCK_EMOJIS:
            if emoji == "❌":
                self.state = State.BLOCK_CHOSEN
                return {"messages": ["You have chosen not to block the user."], "reactions": []}
            elif emoji == "⭕️":
                self.state = State.BLOCK_CHOSEN
                return {"messages": ["We have blocked the user from accessing your profile or directly messaging you. Thank you for your report."], "reactions": []}

        return {"messages": ["I'm sorry, something has gone wrong. Please report this error."], "reactions": ["😭"]}

    async def handle_dm_setting(self, dm_setting):
        emoji = dm_setting.emoji.name
        if self.state == State.DANGER_IDENTIFIED and emoji in DM_SETTING_EMOJIS:
            if emoji == "❌":
                self.state = State.DANGER_IDENTIFIED
                return {"messages": ["We have received your report. Our moderation team will review this message and notify you of the outcome  of the review.The reported post may be removed; and the account posting violating messages may be suspended. Your report may be sent to local law enforcement authorities where necessary."], "reactions": []}
            elif emoji == "⭕️":
                self.state = State.DANGER_IDENTIFIED
                return {"messages": ["Please help us understand why this message may violate our policies. Your message will be sent to our moderation team for review."], "reactions": []}

        return {"messages": ["I'm sorry, something has gone wrong. Please report this error."], "reactions": ["😭"]}

    def report_is_complete(self):
        return self.state == State.REPORT_COMPLETE
