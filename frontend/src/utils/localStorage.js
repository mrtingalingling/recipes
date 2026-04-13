// Fallback logic for SQLite, IndexedDB, RxDB
import Dexie from 'dexie';
import { createRxDatabase, addRxPlugin } from 'rxdb';

// SQLite (via sql.js or similar)
let sqliteAvailable = false;
let db;
try {
  // Assume sql.js is loaded and available
  db = new window.SQL.Database();
  sqliteAvailable = true;
} catch (e) {
  sqliteAvailable = false;
}

// IndexedDB fallback
const dexieDB = new Dexie('recipes');
dexieDB.version(1).stores({
  user_profile: '++id,budget,household_size,dietary_preferences,cooking_time',
  store_deals: '++id,store_name,product_name,price,validity_start,validity_end,geo_location'
});

// RxDB fallback
addRxPlugin(require('pouchdb-adapter-idb'));
let rxdb;
async function initRxDB() {
  rxdb = await createRxDatabase({
    name: 'recipes',
    adapter: 'idb',
    multiInstance: false
  });
  await rxdb.collection({
    name: 'user_profile',
    schema: {
      title: 'user profile schema',
      version: 0,
      type: 'object',
      properties: {
        budget: { type: 'number' },
        household_size: { type: 'number' },
        dietary_preferences: { type: 'string' },
        cooking_time: { type: 'number' }
      }
    }
  });
}

export async function saveUserProfile(profile) {
  if (sqliteAvailable) {
    // Save to SQLite
    db.run('INSERT INTO user_profile (budget, household_size, dietary_preferences, cooking_time) VALUES (?, ?, ?, ?)', [profile.budget, profile.household_size, profile.dietary_preferences, profile.cooking_time]);
    return true;
  }
  try {
    await dexieDB.user_profile.put(profile);
    return true;
  } catch (e) {
    if (!rxdb) await initRxDB();
    await rxdb.user_profile.insert(profile);
    return true;
  }
}

export async function getUserProfile() {
  if (sqliteAvailable) {
    const res = db.exec('SELECT * FROM user_profile LIMIT 1');
    return res[0]?.values[0] || null;
  }
  try {
    const profile = await dexieDB.user_profile.toArray();
    return profile[0] || null;
  } catch (e) {
    if (!rxdb) await initRxDB();
    const docs = await rxdb.user_profile.find().exec();
    return docs[0] || null;
  }
}
