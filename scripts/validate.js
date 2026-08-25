const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const required = [
  'public_html/index.html',
  'public_html/assets/css/site.css',
  'public_html/assets/js/app.js',
  'public_html/assets/data/config.json',
  'public_html/assets/data/directory.json',
  'public_html/assets/data/events.json',
  'public_html/assets/data/social.json'
];

let ok = true;
for (const file of required) {
  const full = path.join(root, file);
  if (!fs.existsSync(full)) {
    console.error(`Missing required file: ${file}`);
    ok = false;
  }
}

function readJson(file) {
  const full = path.join(root, file);
  try { return JSON.parse(fs.readFileSync(full, 'utf8')); }
  catch (error) { console.error(`Invalid JSON: ${file}\n${error.message}`); ok = false; return null; }
}

const config = readJson('public_html/assets/data/config.json');
const directory = readJson('public_html/assets/data/directory.json');
const events = readJson('public_html/assets/data/events.json');
const social = readJson('public_html/assets/data/social.json');

if (config && (!Array.isArray(config.towns) || config.towns.length === 0)) { console.error('config.towns must contain at least one town'); ok = false; }
if (directory && (!Array.isArray(directory.entries) || directory.entries.length === 0)) { console.error('directory.entries must contain at least one entry'); ok = false; }
if (events && (!Array.isArray(events.events) || events.events.length === 0)) { console.error('events.events must contain at least one event'); ok = false; }
if (social && (!Array.isArray(social.posts) || social.posts.length === 0)) { console.error('social.posts must contain at least one post'); ok = false; }

if (directory) {
  for (const entry of directory.entries) {
    for (const field of ['name', 'town', 'postcode', 'category', 'lat', 'lng', 'description']) {
      if (entry[field] === undefined || entry[field] === '') { console.error(`Directory entry missing ${field}: ${entry.name || 'unknown'}`); ok = false; }
    }
  }
}

if (social) {
  for (const post of social.posts) {
    if (!post.caption || post.caption.length < 60) { console.error(`Social post caption too short: ${post.title}`); ok = false; }
    if (!Array.isArray(post.hashtags) || post.hashtags.length < 3) { console.error(`Social post needs at least 3 hashtags: ${post.title}`); ok = false; }
  }
}

if (!ok) process.exit(1);
console.log('PostcodeLive validation passed.');
