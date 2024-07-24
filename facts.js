const { Client, Intents } = require('discord.js');
const axios = require('axios');
const fs = require('fs');
require('dotenv').config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

const reminders = {};
const triviaQuestions = [];
const quotes = [];
const weatherAPIKey = 'witheld'; // your api key

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    loadTriviaQuestions();
    loadQuotes();
});

client.on('messageCreate', message => {
    if (message.author.bot) return;

    if (message.content.toLowerCase().startsWith('!remindme')) {
        setReminder(message);
    }

    if (message.content.toLowerCase() === '!trivia') {
        sendTriviaQuestion(message);
    }

    if (message.content.toLowerCase().startsWith('!quote')) {
        sendQuote(message);
    }

    if (message.content.toLowerCase().startsWith('!addquote')) {
        addQuote(message);
    }

    if (message.content.toLowerCase().startsWith('!weather')) {
        sendWeatherUpdate(message);
    }

    if (message.content.toLowerCase() === '!help') {
        sendHelpMessage(message);
    }
});

function setReminder(message) {
    const args = message.content.split(' ').slice(1);
    const time = parseInt(args[0], 10);
    const reminderMessage = args.slice(1).join(' ');

    if (isNaN(time)) {
        message.channel.send('Invalid time format. Please use minutes.');
        return;
    }

    const reminderID = `${message.author.id}-${Date.now()}`;
    reminders[reminderID] = {
        user: message.author.id,
        message: reminderMessage,
        time: Date.now() + time * 60000
    };

    message.channel.send(`Reminder set for ${time} minutes from now.`);

    setTimeout(() => {
        message.author.send(`Reminder: ${reminderMessage}`);
        delete reminders[reminderID];
    }, time * 60000);
}

function loadTriviaQuestions() {
    triviaQuestions.push(
        { question: "What is the capital of France?", answer: "Paris" },
        { question: "What is 2 + 2?", answer: "4" },
        { question: "Who wrote 'To be, or not to be'?", answer: "Shakespeare" }
    );
}

function sendTriviaQuestion(message) {
    if (triviaQuestions.length === 0) {
        message.channel.send('No trivia questions available.');
        return;
    }

    const trivia = triviaQuestions[Math.floor(Math.random() * triviaQuestions.length)];
    message.channel.send(trivia.question);

    const filter = response => response.content.toLowerCase() === trivia.answer.toLowerCase() && response.author.id === message.author.id;

    message.channel.awaitMessages({ filter, max: 1, time: 30000, errors: ['time'] })
        .then(collected => {
            message.channel.send(`Correct, ${collected.first().author}!`);
        })
        .catch(() => {
            message.channel.send('Time is up! The correct answer was: ' + trivia.answer);
        });
}

function loadQuotes() {
    if (fs.existsSync('quotes.json')) {
        const data = fs.readFileSync('quotes.json');
        const json = JSON.parse(data);
        quotes.push(...json);
    }
}

function saveQuotes() {
    fs.writeFileSync('quotes.json', JSON.stringify(quotes, null, 2));
}

function sendQuote(message) {
    if (quotes.length === 0) {
        message.channel.send('No quotes available.');
        return;
    }

    const quote = quotes[Math.floor(Math.random() * quotes.length)];
    message.channel.send(`"${quote.text}" - ${quote.author}`);
}

function addQuote(message) {
    const args = message.content.split(' ').slice(1);
    const quoteText = args.join(' ');

    if (quoteText.length === 0) {
        message.channel.send('Please provide a quote.');
        return;
    }

    const quote = {
        text: quoteText,
        author: message.author.username
    };

    quotes.push(quote);
    saveQuotes();
    message.channel.send('Quote added.');
}

async function sendWeatherUpdate(message) {
    const args = message.content.split(' ').slice(1);
    const location = args.join(' ');

    if (location.length === 0) {
        message.channel.send('Please provide a location.');
        return;
    }

    try {
        const response = await axios.get(`http://api.weatherapi.com/v1/current.json?key=${weatherAPIKey}&q=${location}`);
        const data = response.data;
        const weatherMessage = `The weather in ${data.location.name} is ${data.current.temp_c}°C with ${data.current.condition.text}.`;
        message.channel.send(weatherMessage);
    } catch (error) {
        message.channel.send('Could not fetch weather data.');
        console.error(error);
    }
}

function sendHelpMessage(message) {
    const helpMessage = `
**Bot Commands** 📜
\`!remindme <minutes> <message>\` - Sets a reminder.
\`!trivia\` - Asks a trivia question.
\`!quote\` - Displays a random quote.
\`!addquote <quote>\` - Adds a new quote.
\`!weather <location>\` - Provides a weather update for the specified location.
\`!help\` - Displays this help message.
    `;
    message.channel.send(helpMessage);
}

client.login(process.env.DISCORD_BOT_TOKEN);
