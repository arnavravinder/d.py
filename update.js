const { Client, Intents } = require('discord.js');
const Parser = require('rss-parser');
const fs = require('fs');
require('dotenv').config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });
const parser = new Parser();

let rssFeeds = {};

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    loadRSSFeeds();
    checkFeeds.start();
});

client.on('messageCreate', message => {
    if (message.author.bot) return;

    if (message.content.toLowerCase().startsWith('!addrss')) {
        addRSSFeed(message);
    }

    if (message.content.toLowerCase().startsWith('!removerss')) {
        removeRSSFeed(message);
    }

    if (message.content.toLowerCase() === '!listrss') {
        listRSSFeeds(message);
    }

    if (message.content.toLowerCase() === '!help') {
        sendHelpMessage(message);
    }
});

function loadRSSFeeds() {
    if (fs.existsSync('rssFeeds.json')) {
        const data = fs.readFileSync('rssFeeds.json');
        rssFeeds = JSON.parse(data);
    }
}

function saveRSSFeeds() {
    fs.writeFileSync('rssFeeds.json', JSON.stringify(rssFeeds, null, 2));
}

async function addRSSFeed(message) {
    const args = message.content.split(' ').slice(1);
    const channel = message.channel.id;
    const url = args.join(' ');

    if (!url) {
        message.channel.send('Please provide a valid RSS feed URL.');
        return;
    }

    try {
        const feed = await parser.parseURL(url);
        if (!rssFeeds[channel]) {
            rssFeeds[channel] = [];
        }
        rssFeeds[channel].push({ url, lastUpdate: feed.items[0].isoDate });
        saveRSSFeeds();
        message.channel.send(`RSS feed added: ${url}`);
    } catch (error) {
        message.channel.send('Failed to add RSS feed. Make sure the URL is correct.');
    }
}

function removeRSSFeed(message) {
    const args = message.content.split(' ').slice(1);
    const channel = message.channel.id;
    const url = args.join(' ');

    if (!rssFeeds[channel]) {
        message.channel.send('No RSS feeds found for this channel.');
        return;
    }

    const feedIndex = rssFeeds[channel].findIndex(feed => feed.url === url);
    if (feedIndex === -1) {
        message.channel.send('RSS feed not found.');
        return;
    }

    rssFeeds[channel].splice(feedIndex, 1);
    saveRSSFeeds();
    message.channel.send(`RSS feed removed: ${url}`);
}

function listRSSFeeds(message) {
    const channel = message.channel.id;

    if (!rssFeeds[channel] || rssFeeds[channel].length === 0) {
        message.channel.send('No RSS feeds found for this channel.');
        return;
    }

    const feedList = rssFeeds[channel].map(feed => feed.url).join('\n');
    message.channel.send(`RSS feeds for this channel:\n${feedList}`);
}

async function checkFeeds() {
    for (const channel in rssFeeds) {
        for (const feed of rssFeeds[channel]) {
            try {
                const parsedFeed = await parser.parseURL(feed.url);
                const newItems = parsedFeed.items.filter(item => new Date(item.isoDate) > new Date(feed.lastUpdate));

                if (newItems.length > 0) {
                    const channelObject = client.channels.cache.get(channel);
                    for (const item of newItems) {
                        channelObject.send(`New update from ${parsedFeed.title}:\n${item.title}\n${item.link}`);
                    }
                    feed.lastUpdate = newItems[0].isoDate;
                    saveRSSFeeds();
                }
            } catch (error) {
                console.error(`Failed to fetch RSS feed: ${feed.url}`, error);
            }
        }
    }
}

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);
});

const checkFeedsInterval = setInterval(checkFeeds, 60000);

client.on('messageCreate', async (message) => {
    if (message.author.bot) return;

    if (message.content.toLowerCase().startsWith('!addrss')) {
        addRSSFeed(message);
    }

    if (message.content.toLowerCase().startsWith('!removerss')) {
        removeRSSFeed(message);
    }

    if (message.content.toLowerCase() === '!listrss') {
        listRSSFeeds(message);
    }

    if (message.content.toLowerCase() === '!help') {
        sendHelpMessage(message);
    }
});

function sendHelpMessage(message) {
    const helpMessage = `
**RSS Feed Bot Commands** 📜
\`!addrss <URL>\` - Adds an RSS feed to the channel.
\`!removerss <URL>\` - Removes an RSS feed from the channel.
\`!listrss\` - Lists all RSS feeds for the channel.
\`!help\` - Displays this help message.
    `;
    message.channel.send(helpMessage);
}

client.login(process.env.DISCORD_BOT_TOKEN);
