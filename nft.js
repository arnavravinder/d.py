const { Client, Intents } = require('discord.js');
const fs = require('fs');
require('dotenv').config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

let playlists = {};

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    loadPlaylists();
});

client.on('messageCreate', message => {
    if (message.author.bot) return;

    if (message.content.toLowerCase().startsWith('!createplaylist')) {
        createPlaylist(message);
    }

    if (message.content.toLowerCase().startsWith('!addsong')) {
        addSongToPlaylist(message);
    }

    if (message.content.toLowerCase().startsWith('!removesong')) {
        removeSongFromPlaylist(message);
    }

    if (message.content.toLowerCase().startsWith('!viewplaylist')) {
        viewPlaylist(message);
    }

    if (message.content.toLowerCase().startsWith('!deleteplaylist')) {
        deletePlaylist(message);
    }

    if (message.content.toLowerCase() === '!listplaylists') {
        listPlaylists(message);
    }

    if (message.content.toLowerCase() === '!help') {
        sendHelpMessage(message);
    }
});

function loadPlaylists() {
    if (fs.existsSync('playlists.json')) {
        const data = fs.readFileSync('playlists.json');
        playlists = JSON.parse(data);
    }
}

function savePlaylists() {
    fs.writeFileSync('playlists.json', JSON.stringify(playlists, null, 2));
}

function createPlaylist(message) {
    const args = message.content.split(' ').slice(1);
    const playlistName = args.join(' ');

    if (!playlistName) {
        message.channel.send('Please provide a name for the playlist.');
        return;
    }

    if (playlists[playlistName]) {
        message.channel.send('A playlist with this name already exists.');
        return;
    }

    playlists[playlistName] = [];
    savePlaylists();
    message.channel.send(`Playlist "${playlistName}" created.`);
}

function addSongToPlaylist(message) {
    const args = message.content.split(' ').slice(1);
    const playlistName = args[0];
    const song = args.slice(1).join(' ');

    if (!playlistName || !song) {
        message.channel.send('Please provide a playlist name and a song to add.');
        return;
    }

    if (!playlists[playlistName]) {
        message.channel.send('Playlist not found.');
        return;
    }

    playlists[playlistName].push(song);
    savePlaylists();
    message.channel.send(`Song added to playlist "${playlistName}".`);
}

function removeSongFromPlaylist(message) {
    const args = message.content.split(' ').slice(1);
    const playlistName = args[0];
    const song = args.slice(1).join(' ');

    if (!playlistName || !song) {
        message.channel.send('Please provide a playlist name and a song to remove.');
        return;
    }

    if (!playlists[playlistName]) {
        message.channel.send('Playlist not found.');
        return;
    }

    const songIndex = playlists[playlistName].indexOf(song);
    if (songIndex === -1) {
        message.channel.send('Song not found in the playlist.');
        return;
    }

    playlists[playlistName].splice(songIndex, 1);
    savePlaylists();
    message.channel.send(`Song removed from playlist "${playlistName}".`);
}

function viewPlaylist(message) {
    const args = message.content.split(' ').slice(1);
    const playlistName = args.join(' ');

    if (!playlistName) {
        message.channel.send('Please provide a playlist name.');
        return;
    }

    if (!playlists[playlistName]) {
        message.channel.send('Playlist not found.');
        return;
    }

    const playlist = playlists[playlistName];
    if (playlist.length === 0) {
        message.channel.send(`Playlist "${playlistName}" is empty.`);
        return;
    }

    const songList = playlist.map((song, index) => `${index + 1}. ${song}`).join('\n');
    message.channel.send(`**${playlistName}**\n${songList}`);
}

function deletePlaylist(message) {
    const args = message.content.split(' ').slice(1);
    const playlistName = args.join(' ');

    if (!playlistName) {
        message.channel.send('Please provide a playlist name.');
        return;
    }

    if (!playlists[playlistName]) {
        message.channel.send('Playlist not found.');
        return;
    }

    delete playlists[playlistName];
    savePlaylists();
    message.channel.send(`Playlist "${playlistName}" deleted.`);
}

function listPlaylists(message) {
    if (Object.keys(playlists).length === 0) {
        message.channel.send('No playlists found.');
        return;
    }

    const playlistNames = Object.keys(playlists).join('\n');
    message.channel.send(`**Playlists**\n${playlistNames}`);
}

function sendHelpMessage(message) {
    const helpMessage = `
**Playlist Bot Commands** 📜
\`!createplaylist <name>\` - Creates a new playlist.
\`!addsong <playlist> <song>\` - Adds a song to a playlist.
\`!removesong <playlist> <song>\` - Removes a song from a playlist.
\`!viewplaylist <name>\` - Displays the songs in a playlist.
\`!deleteplaylist <name>\` - Deletes a playlist.
\`!listplaylists\` - Lists all playlists.
\`!help\` - Displays this help message.
    `;
    message.channel.send(helpMessage);
}

client.login(process.env.DISCORD_BOT_TOKEN);
