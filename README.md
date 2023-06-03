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

---

## Data Sources

<https://www.kaggle.com/datasets/andrewmvd/cyberbullying-classification>
this dataset contains more than 47000 tweets labelled according to the class of cyberbullying
J. Wang, K. Fu, C.T. Lu, “SOSNet: A Graph Convolutional Network Approach to Fine-Grained Cyberbullying Detection,” Proceedings of the 2020 IEEE International Conference on Big Data (IEEE BigData 2020), December 10-13, 2020.

<https://www.kaggle.com/datasets/saurabhshahane/cyberbullying-dataset?resource=download>
The data is from different social media platforms like Kaggle, Twitter, Wikipedia Talk pages and YouTube. The data contain text and labeled as bullying or not. The data contains different types of cyber-bullying like hate speech, aggression, insults and toxicity.
Elsafoury, Fatma (2020), “Cyberbullying datasets”, Mendeley Data, V1, doi: 10.17632/jf4pzyvnpj.1

<https://aclanthology.org/2021.woah-1.16/> -> <https://bitbucket.org/ssalawu/cyberbullying-twitter/src/master/>
Uses Tweet IDs
