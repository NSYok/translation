import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc, onSnapshot, updateDoc, deleteField } from "firebase/firestore";

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

// Used for bulk uploads (like importing JSON file)
export async function saveGameData(data) {
  try {
    if (data.Single && data.Single[""]) delete data.Single[""];
    if (data.Sets && data.Sets[""]) delete data.Sets[""];
    await setDoc(DATA_DOC, data);
    return true;
  } catch (error) {
    console.error("Error saving to Firebase:", error);
    throw error;
  }
}

// Granular updates to prevent "last man wins" overwrites
export async function saveSingleItem(oldName, newName, stats) {
  const updates = {};
  if (oldName && oldName !== newName) {
    updates[`Single.${oldName}`] = deleteField();
  }
  updates[`Single.${newName}`] = stats;
  return updateDoc(DATA_DOC, updates);
}

export async function deleteSingleItem(name) {
  return updateDoc(DATA_DOC, {
    [`Single.${name}`]: deleteField()
  });
}

export async function saveSetItem(oldName, newName, tiers) {
  const updates = {};
  if (oldName && oldName !== newName) {
    updates[`Sets.${oldName}`] = deleteField();
  }
  updates[`Sets.${newName}`] = tiers;
  return updateDoc(DATA_DOC, updates);
}

export async function deleteSetItem(name) {
  return updateDoc(DATA_DOC, {
    [`Sets.${name}`]: deleteField()
  });
}
