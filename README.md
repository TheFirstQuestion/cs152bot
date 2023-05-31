# CS 152 - Trust and Safety Engineering

## Discord Bot Framework Code

This is our CS 152 final project: a Discord moderation bot that focuses on cyberbullying.

### Dependencies

Install the following packages:

```bash
discord openai google-api-python-client 
```

Create `DiscordBot/tokens.json` and/or `API Testing/tokens.json`.

```json
{
 "discord": "API_KEY_HERE",
 "openAI_org": "org-XXXX",
 "openAI_key": "API_KEY_HERE",
 "google": "API_KEY_HERE"
}
```

---

## Classifiers

### [Perspective](https://www.perspectiveapi.com/)

> Perspective is a free API that uses machine learning to identify "toxic" comments, making it easier to host better conversations online. The Perspective Comment Analyzer API provides information about the potential impact of a comment on a conversation (e.g. it can provide a score for the "toxicity" of a comment).

### [OpenAI](https://platform.openai.com/docs/models/moderation)

> The Moderation models are designed to check whether content complies with OpenAI's usage policies. The models provide classification capabilities that look for content in the following categories: hate, hate/threatening, self-harm, sexual, sexual/minors, violence, and violence/graphic. You can find out more in our moderation guide.
