const { Client, Intents } = require('discord.js');
const axios = require('axios');
const fs = require('fs');
require('dotenv').config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

let streamers = {};

const twitchClientId = 'witheld'; // add
const twitchClientSecret = 'witheld'; // add
let twitchToken = '';
let twitchTokenExpiry = 0;

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    loadStreamers();
    checkStreams();
    setInterval(checkStreams, 300000); 
});

client.on('messageCreate', message => {
    if (message.author.bot) return;

    if (message.content.toLowerCase().startsWith('!addstreamer')) {
        addStreamer(message);
    }

    if (message.content.toLowerCase().startsWith('!removestreamer')) {
        removeStreamer(message);
    }

    if (message.content.toLowerCase() === '!liststreamers') {
        listStreamers(message);
    }

    if (message.content.toLowerCase() === '!help') {
        sendHelpMessage(message);
    }
});

async function getTwitchToken() {
    if (twitchToken && Date.now() < twitchTokenExpiry) return twitchToken;

    try {
        const response = await axios.post('https://id.twitch.tv/oauth2/token', null, {
            params: {
                client_id: twitchClientId,
                client_secret: twitchClientSecret,
                grant_type: 'client_credentials'
            }
        });

        twitchToken = response.data.access_token;
        twitchTokenExpiry = Date.now() + response.data.expires_in * 1000;
        return twitchToken;
    } catch (error) {
        console.error('Error getting Twitch token:', error);
    }
}

function loadStreamers() {
    if (fs.existsSync('streamers.json')) {
        const data = fs.readFileSync('streamers.json');
        streamers = JSON.parse(data);
    }
}

function saveStreamers() {
    fs.writeFileSync('streamers.json', JSON.stringify(streamers, null, 2));
}

async function checkStreams() {
    const token = await getTwitchToken();
    const headers = {
        'Client-ID': twitchClientId,
        'Authorization': `Bearer ${token}`
    };

    for (const [channelId, streamerList] of Object.entries(streamers)) {
        for (const streamer of streamerList) {
            try {
                const response = await axios.get(`https://api.twitch.tv/helix/streams?user_login=${streamer.name}`, { headers });

                if (response.data.data.length > 0) {
                    const stream = response.data.data[0];
                    if (!streamer.live) {
                        streamer.live = true;
                        client.channels.cache.get(channelId).send(`${streamer.name} is now live: ${stream.title} - ${stream.viewer_count} viewers\n${stream.thumbnail_url}`);
                    }
                } else {
                    streamer.live = false;
                }
            } catch (error) {
                console.error('Error checking stream status:', error);
            }
        }
    }

    saveStreamers();
}

function addStreamer(message) {
    const args = message.content.split(' ').slice(1);
    const channel = message.channel.id;
    const streamerName = args.join(' ');

    if (!streamerName) {
        message.channel.send('Please provide a streamer name.');
        return;
    }

    if (!streamers[channel]) {
        streamers[channel] = [];
    }

    streamers[channel].push({ name: streamerName, live: false });
    saveStreamers();
    message.channel.send(`Streamer ${streamerName} added to notifications.`);
}

function removeStreamer(message) {
    const args = message.content.split(' ').slice(1);
    const channel = message.channel.id;
    const streamerName = args.join(' ');

    if (!streamers[channel]) {
        message.channel.send('No streamers found for this channel.');
        return;
    }

    const streamerIndex = streamers[channel].findIndex(streamer => streamer.name === streamerName);
    if (streamerIndex === -1) {
        message.channel.send('Streamer not found.');
        return;
    }

    streamers[channel].splice(streamerIndex, 1);
    saveStreamers();
    message.channel.send(`Streamer ${streamerName} removed from notifications.`);
}

function listStreamers(message) {
    const channel = message.channel.id;

    if (!streamers[channel] || streamers[channel].length === 0) {
        message.channel.send('No streamers found for this channel.');
        return;
    }

    const streamerList = streamers[channel].map(streamer => streamer.name).join('\n');
    message.channel.send(`Streamers for this channel:\n${streamerList}`);
}

function sendHelpMessage(message) {
    const helpMessage = `
**Stream Notification Bot Commands** 📜
\`!addstreamer <name>\` - Adds a streamer to the channel notifications.
\`!removestreamer <name>\` - Removes a streamer from the channel notifications.
\`!liststreamers\` - Lists all streamers added to the channel notifications.
\`!help\` - Displays this help message.
    `;
    message.channel.send(helpMessage);
}

client.login(process.env.DISCORD_BOT_TOKEN);
