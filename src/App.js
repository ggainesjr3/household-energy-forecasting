import React, { useEffect, useState } from 'react';
import { initializeApp } from "firebase/app";
import { getFirestore, doc, onSnapshot } from "firebase/firestore";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Line } from 'recharts';

// --- CONFIG ---
const firebaseConfig = {
  projectId: "friday-75f5a",
  authDomain: "friday-75f5a.firebaseapp.com",
  // Ensure you add your apiKey here from Firebase Console!
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // 1. We listen to 'forecasts' collection, 'latest' document
    const unsub = onSnapshot(doc(db, "forecasts", "latest"), (doc) => {
      if (doc.exists()) {
        const firestoreData = doc.data().data;
        console.log("Data Received:", firestoreData); // Check your browser console!
        setData(firestoreData);
      }
    });
    return () => unsub();
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-emerald-400">SmartGrid Intelligence</h1>
        <p className="text-slate-400">Real-time XGBoost Energy Forecasting</p>
      </header>

      <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-2xl">
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="colorPred" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              {/* UPDATED: dataKey="hour" matches your Firestore structure */}
              <XAxis dataKey="hour" stroke="#94a3b8" fontSize={12} label={{ value: 'Hour (Next 48h)', position: 'insideBottom', offset: -5, fill: '#94a3b8' }} />
              <YAxis stroke="#94a3b8" fontSize={12} unit="kW" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
              
              {/* Predictions Line */}
              <Area type="monotone" dataKey="predicted" stroke="#10b981" fillOpacity={1} fill="url(#colorPred)" strokeWidth={3} name="XGBoost Prediction" />
              
              {/* Actual Usage Line (Dashed) */}
              <Line type="monotone" dataKey="actual" stroke="#6366f1" strokeWidth={2} dot={false} strokeDasharray="5 5" name="Actual Usage" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default App;