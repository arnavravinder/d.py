const { Client, Intents } = require('discord.js');
const axios = require('axios');
const fs = require('fs');
require('dotenv').config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

let reminders = {};
const facts = [
    'Honey never spoils.',
    'A flock of crows is known as a murder.',
    'Bananas are berries, but strawberries aren’t.',
    'Octopuses have three hearts.',
    'Cows can sleep standing up, but they can only dream lying down.'
];
const quotes = [
    'The best way to get started is to quit talking and begin doing. - Walt Disney',
    'The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty. - Winston Churchill',
    'Don’t let yesterday take up too much of today. - Will Rogers',
    'You learn more from failure than from success. Don’t let it stop you. Failure builds character. - Unknown',
    'It’s not whether you get knocked down, it’s whether you get up. - Vince Lombardi'
];

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    loadReminders();
});

client.on('messageCreate', message => {
    if (message.author.bot) return;

    if (message.content.toLowerCase().startsWith('!remindme')) {
        setReminder(message);
    }

    if (message.content.toLowerCase() === '!fact') {
        sendFact(message);
    }

    if (message.content.toLowerCase() === '!quote') {
        sendQuote(message);
    }

    if (message.content.toLowerCase().startsWith('!convert')) {
        convertCurrency(message);
    }

    if (message.content.toLowerCase() === '!help') {
        sendHelpMessage(message);
    }
});

function loadReminders() {
    if (fs.existsSync('reminders.json')) {
        const data = fs.readFileSync('reminders.json');
        reminders = JSON.parse(data);
        Object.keys(reminders).forEach(reminderID => {
            const reminder = reminders[reminderID];
            const timeLeft = reminder.time - Date.now();
            if (timeLeft > 0) {
                setTimeout(() => {
                    const user = client.users.cache.get(reminder.user);
                    if (user) {
                        user.send(`Reminder: ${reminder.message}`);
                    }
                    delete reminders[reminderID];
                    saveReminders();
                }, timeLeft);
            } else {
                delete reminders[reminderID];
                saveReminders();
            }
        });
    }
}

function saveReminders() {
    fs.writeFileSync('reminders.json', JSON.stringify(reminders, null, 2));
}

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
        saveReminders();
    }, time * 60000);
}

function sendFact(message) {
    const randomFact = facts[Math.floor(Math.random() * facts.length)];
    message.channel.send(randomFact);
}

function sendQuote(message) {
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    message.channel.send(randomQuote);
}

async function convertCurrency(message) {
    const args = message.content.split(' ').slice(1);
    if (args.length < 3) {
        message.channel.send('Usage: !convert <amount> <from_currency> <to_currency>');
        return;
    }

    const amount = parseFloat(args[0]);
    const fromCurrency = args[1].toUpperCase();
    const toCurrency = args[2].toUpperCase();

    if (isNaN(amount)) {
        message.channel.send('Invalid amount.');
        return;
    }

    try {
        const response = await axios.get(`https://api.exchangerate-api.com/v4/latest/${fromCurrency}`);
        const rate = response.data.rates[toCurrency];
        if (!rate) {
            message.channel.send('Invalid currency code.');
            return;
        }
        const convertedAmount = amount * rate;
        message.channel.send(`${amount} ${fromCurrency} is ${convertedAmount.toFixed(2)} ${toCurrency}`);
    } catch (error) {
        message.channel.send('Error fetching exchange rate.');
        console.error(error);
    }
}

function sendHelpMessage(message) {
    const helpMessage = `
**Bot Commands** 📜
\`!remindme <minutes> <message>\` - Sets a reminder.
\`!fact\` - Sends a random fun fact.
\`!quote\` - Sends a random motivational quote.
\`!convert <amount> <from_currency> <to_currency>\` - Converts currency.
\`!help\` - Displays this help message.
    `;
    message.channel.send(helpMessage);
}

client.login(process.env.DISCORD_BOT_TOKEN);
