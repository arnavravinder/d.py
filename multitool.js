const { Client, Intents } = require('discord.js');
const axios = require('axios');
const fs = require('fs');
require('dotenv').config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

let polls = [];
let userStats = {};

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    loadPolls();
    loadUserStats();
});

client.on('messageCreate', message => {
    if (message.author.bot) return;

    if (message.content.toLowerCase().startsWith('!poll')) {
        createPoll(message);
    }

    if (message.content.toLowerCase().startsWith('!vote')) {
        votePoll(message);
    }

    if (message.content.toLowerCase() === '!joke') {
        sendJoke(message);
    }

    if (message.content.toLowerCase() === '!stats') {
        sendUserStats(message);
    }

    if (message.content.toLowerCase() === '!leaderboard') {
        sendLeaderboard(message);
    }

    if (message.content.toLowerCase() === '!help') {
        sendHelpMessage(message);
    }

    updateUserStats(message.author.id);
});

function loadPolls() {
    if (fs.existsSync('polls.json')) {
        const data = fs.readFileSync('polls.json');
        polls = JSON.parse(data);
    }
}

function savePolls() {
    fs.writeFileSync('polls.json', JSON.stringify(polls, null, 2));
}

function createPoll(message) {
    const args = message.content.split(' ').slice(1);
    const question = args.join(' ');
    const poll = {
        id: polls.length + 1,
        question,
        options: [],
        votes: {}
    };
    polls.push(poll);
    savePolls();
    message.channel.send(`Poll created: ${question}`);
}

function votePoll(message) {
    const args = message.content.split(' ').slice(1);
    const pollId = parseInt(args[0], 10);
    const option = args.slice(1).join(' ');

    const poll = polls.find(p => p.id === pollId);
    if (!poll) {
        message.channel.send('Poll not found.');
        return;
    }

    if (!poll.options.includes(option)) {
        poll.options.push(option);
    }

    poll.votes[message.author.id] = option;
    savePolls();
    message.channel.send(`Vote recorded: ${option}`);
}

function loadUserStats() {
    if (fs.existsSync('userStats.json')) {
        const data = fs.readFileSync('userStats.json');
        userStats = JSON.parse(data);
    }
}

function saveUserStats() {
    fs.writeFileSync('userStats.json', JSON.stringify(userStats, null, 2));
}

function updateUserStats(userId) {
    if (!userStats[userId]) {
        userStats[userId] = { messages: 0, votes: 0 };
    }
    userStats[userId].messages += 1;
    saveUserStats();
}

function sendUserStats(message) {
    const userId = message.author.id;
    const stats = userStats[userId];
    if (stats) {
        message.channel.send(`${message.author.username}, you have sent ${stats.messages} messages and cast ${stats.votes} votes.`);
    } else {
        message.channel.send('No stats found for you.');
    }
}

function sendLeaderboard(message) {
    const sortedUsers = Object.entries(userStats).sort((a, b) => b[1].messages - a[1].messages);
    const leaderboard = sortedUsers.map(([userId, stats], index) => `${index + 1}. <@${userId}> - ${stats.messages} messages`).join('\n');
    message.channel.send(`Leaderboard:\n${leaderboard}`);
}

async function sendJoke(message) {
    try {
        const response = await axios.get('https://official-joke-api.appspot.com/random_joke');
        const joke = `${response.data.setup} - ${response.data.punchline}`;
        message.channel.send(joke);
    } catch (error) {
        message.channel.send('Sorry, I couldn\'t fetch a joke at this time.');
        console.error(error);
    }
}

function sendHelpMessage(message) {
    const helpMessage = `
**Bot Commands** 📜
\`!poll <question>\` - Creates a new poll.
\`!vote <pollId> <option>\` - Votes in a poll.
\`!joke\` - Sends a random joke.
\`!stats\` - Shows your user statistics.
\`!leaderboard\` - Shows the leaderboard for the most messages sent.
\`!help\` - Displays this help message.
    `;
    message.channel.send(helpMessage);
}

client.login(process.env.DISCORD_BOT_TOKEN);
