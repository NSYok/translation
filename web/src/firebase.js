import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc, onSnapshot } from "firebase/firestore";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Collection: 'gameData', Document: 'main'
const DATA_DOC = doc(db, "gameData", "main");

export function subscribeToGameData(callback) {
  return onSnapshot(DATA_DOC, (docSnap) => {
    if (docSnap.exists()) {
      callback(docSnap.data());
    }
  }, (error) => {
    console.error("Firebase subscription error:", error);
  });
}

export async function fetchGameData() {
  try {
    const docSnap = await getDoc(DATA_DOC);
    if (docSnap.exists()) {
      return docSnap.data();
    } else {
      console.warn("No data found in Firebase, falling back to local data.json");
      return null;
    }
  } catch (error) {
    console.error("Error fetching from Firebase:", error);
    return null;
  }
}

export async function saveGameData(localData) {
  try {
    // 1. Fetch latest data from cloud to avoid overwriting others' work
    const docSnap = await getDoc(DATA_DOC);
    let cloudData = docSnap.exists() ? docSnap.data() : { Single: {}, Sets: {} };

    // 2. Perform Deep Merge (Local data takes priority for specific items changed)
    const mergedData = {
      Single: { ...(cloudData.Single || {}), ...(localData.Single || {}) },
      Sets: { ...(cloudData.Sets || {}), ...(localData.Sets || {}) }
    };

    // 3. Remove any potential empty keys that Firestore hates
    if (mergedData.Single[""]) delete mergedData.Single[""];
    if (mergedData.Sets[""]) delete mergedData.Sets[""];

    // 4. Save merged result
    await setDoc(DATA_DOC, mergedData);
    return true;
  } catch (error) {
    console.error("Error saving to Firebase:", error);
    throw error;
  }
}
