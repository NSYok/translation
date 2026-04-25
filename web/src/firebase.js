import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc, updateDoc } from "firebase/firestore";

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

export async function saveGameData(data) {
  try {
    await setDoc(DATA_DOC, data);
    return true;
  } catch (error) {
    console.error("Error saving to Firebase:", error);
    throw error;
  }
}
