import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc, updateDoc } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyCfpsfrqz27vR702HzPUxDdSflreOsib9s",
  authDomain: "coa-database-by-nsyok.firebaseapp.com",
  projectId: "coa-database-by-nsyok",
  storageBucket: "coa-database-by-nsyok.firebasestorage.app",
  messagingSenderId: "776176055557",
  appId: "1:776176055557:web:7bda2e8ff7fa0b7bdeb36c"
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
