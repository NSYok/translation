import { initializeApp } from "firebase/app";
import { getFirestore, doc, setDoc } from "firebase/firestore";
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current dir
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env manual parsing
const envPath = path.resolve(__dirname, '.env');
const envContent = fs.readFileSync(envPath, 'utf-8');
const env = {};
envContent.split('\n').forEach(line => {
  const [key, value] = line.split('=');
  if (key && value) env[key.trim()] = value.trim();
});

const firebaseConfig = {
  apiKey: env.VITE_FIREBASE_API_KEY,
  authDomain: env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: env.VITE_FIREBASE_APP_ID
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function upload() {
  console.log("🚀 Reading data.json...");
  const dataPath = path.resolve(__dirname, 'public', 'data.json');
  const data = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));

  // Cleanup empty keys
  if (data.Single && data.Single[""]) delete data.Single[""];
  if (data.Sets && data.Sets[""]) delete data.Sets[""];

  console.log("📡 Uploading to Firebase Firestore...");
  try {
    await setDoc(doc(db, "gameData", "main"), data);
    console.log("✅ SUCCESS! Data uploaded to collection 'gameData', document 'main'");
    process.exit(0);
  } catch (error) {
    console.error("❌ FAILED to upload:", error);
    process.exit(1);
  }
}

upload();
