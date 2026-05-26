import React, { useState, useEffect } from 'react';
import { Activity, ShieldAlert, AlertTriangle, CheckCircle, Cpu, Radio, Terminal, Server, PlusCircle, Check, HelpCircle } from 'lucide-react';

export default function GatiPathModule() {
  const [fleetData, setFleetData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('hardware'); // Default to connection guide first!
  const [testTrackId, setTestTrackId] = useState('TRK-01-MUMBAI');
  const [simulationActive, setSimulationActive] = useState(false);

  // Poll whatever devices are currently registered in the backend memory map
  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const response = await fetch('http://localhost:8000/gati-path/fleet/summary?tracking_id=ALL');
        if (!response.ok) throw new Error('Hardware Gateway Connection Loss.');
        const data = await response.json();
        
        // Filter out empty mock entries so we only show devices actively broadcasting
        const activeDevices = Object.fromEntries(
          Object.entries(data).filter(([_, details]) => details.destination)
        );

        setFleetData(activeDevices);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 1000); 
    return () => clearInterval(interval);
  }, []);

  const getAlertConfig = (insight = "") => {
    if (insight.includes("CRITICAL") || insight.includes("SAFETY WARNING") || insight.includes("TRAFFIC")) {
      return { border: 'border-rose-500/30', bg: 'bg-rose-950/20 text-rose-300', icon: <ShieldAlert className="w-4 h-4 text-rose-400 shrink-0" /> };
    }
    if (insight.includes("FINANCIAL") || insight.includes("ENVIRONMENTAL") || insight.includes("DETOUR")) {
      return { border: 'border-amber-500/30', bg: 'bg-amber-950/20 text-amber-300', icon: <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" /> };
    }
    return { border: 'border-emerald-500/30', bg: 'bg-emerald-950/20 text-emerald-300', icon: <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" /> };
  };

  return (
    <div className="space-y-6">
      {/* Module Title Banner */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-1.5 bg-sky-500/10 text-sky-400 rounded-md font-mono text-xs font-bold">MODULE 01</span>
            <h2 className="text-xl font-bold text-white tracking-tight">Gati-Path Workspace</h2>
          </div>
          <p className="text-gray-400 text-xs mt-1">
            Dynamic Gateway Aggregator. Hardware streams configure instantly on incoming transmission handshake packets.
          </p>
        </div>
        
        {/* Navigation Tabs */}
        <div className="flex bg-gray-950 p-1 rounded-lg border border-gray-800 self-start md:set-center font-mono text-xs">
          <button
            onClick={() => setActiveTab('hardware')}
            className={`px-3 py-1.5 rounded-md font-medium transition-all ${activeTab === 'hardware' ? 'bg-gray-800 text-sky-400 border border-gray-700' : 'text-gray-400 hover:text-white'}`}
          >
            1. Setup & Integration
          </button>
          <button
            onClick={() => setActiveTab('monitor')}
            className={`px-3 py-1.5 rounded-md font-medium transition-all relative ${activeTab === 'monitor' ? 'bg-gray-800 text-sky-400 border border-gray-700' : 'text-gray-400 hover:text-white'}`}
          >
            2. Console Monitor
            {fleetData && Object.keys(fleetData).length > 0 && (
              <span className="absolute -top-1 -right-1 w-2 h-2 bg-emerald-500 rounded-full animate-ping" />
            )}
          </button>
        </div>
      </div>

      {activeTab === 'hardware' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Setup Instructions */}
          <div className="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-5">
            <div className="flex items-center gap-2 text-gray-200 font-bold text-sm border-b border-gray-850 pb-3">
              <Cpu className="w-4 h-4 text-sky-400" />
              How to Link Your Physical Vehicles / Devices
            </div>
            
            <p className="text-xs text-gray-400 leading-relaxed">
              This system does not store or expect static truck configurations. To view a vehicle, config your field unit to deploy an initial HTTP data frame payload packet into our central processing node. The system will register your asset instantly.
            </p>

            <div className="space-y-2">
              <label className="text-[10px] font-mono uppercase tracking-wider text-gray-500 block">Gateway Network Target URI</label>
              <div className="bg-gray-950 font-mono text-xs p-3 rounded-lg border border-gray-850 text-gray-300 select-all">
                <span className="text-emerald-400 font-bold mr-2">POST</span> http://127.0.0.1:8000/gati-path/iot-ping
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-[10px] font-mono uppercase tracking-wider text-gray-500 block">Required Frame Payload Structure (JSON)</label>
              <pre className="bg-gray-950 font-mono text-xs p-4 rounded-lg border border-gray-850 overflow-x-auto text-amber-400">
{`{
  "tracking_id": "YOUR_CUSTOM_VEHICLE_ID",  // e.g., "MH-12-XYZ-45"
  "lat": 19.456, 
  "lng": 72.571,
  "current_fuel_liters": 150.5,
  "cargo_load_kg": 2500.0,
  "hours_driven_without_rest": 2.5
}`}
              </pre>
            </div>
          </div>

          {/* Interactive Tester Box */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 flex flex-col justify-between space-y-4">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-gray-200 font-bold text-sm">
                <Terminal className="w-4 h-4 text-sky-400" />
                Live Node Emulator Setup
              </div>
              <p className="text-[11px] text-gray-400 leading-relaxed">
                Want to see the data link activate dynamically without configuring real microcontroller boards right now? Declare a custom ID identifier below to mimic an inbound operational vehicle feed.
              </p>

              <div className="space-y-1.5 pt-2">
                <label className="text-[10px] font-mono uppercase tracking-wider text-gray-500 block">Assign Custom Hardware Name ID</label>
                <input 
                  type="text" 
                  value={testTrackId}
                  onChange={(e) => setTestTrackId(e.target.value.toUpperCase())}
                  placeholder="e.g. TRK-DELTA-9"
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-xs font-mono text-sky-400 focus:outline-none focus:border-sky-500 transition-colors"
                />
              </div>
            </div>

            <div className="bg-gray-950 p-4 rounded-lg border border-gray-850 space-y-3">
              <div className="flex justify-between items-center text-[11px]">
                <span className="text-gray-500 font-mono">Stream Connection Status:</span>
                {fleetData && fleetData[testTrackId] ? (
                  <span className="text-emerald-400 font-bold flex items-center gap-1">● ONLINE</span>
                ) : (
                  <span className="text-gray-600 font-bold">○ DISCONNECTED</span>
                )}
              </div>

              {fleetData && fleetData[testTrackId] ? (
                <div className="p-2.5 bg-emerald-950/10 border border-emerald-900/30 text-emerald-400 text-[11px] rounded flex gap-1.5 items-start">
                  <Check className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>Success! Device <b className="font-mono">{testTrackId}</b> registered. Click into the Console Monitor tab to watch it trace.</span>
                </div>
              ) : (
                <div className="p-2.5 bg-gray-900 border border-gray-800 text-gray-400 text-[11px] rounded flex gap-1.5 items-start">
                  <HelpCircle className="w-3.5 h-3.5 mt-0.5 shrink-0 text-gray-500" />
                  <span>Awaiting initial handshake ping packet configuration...</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'monitor' && (
        <>
          {error && (
            <div className="p-4 bg-rose-950/20 border border-rose-900/40 text-rose-400 text-xs rounded-xl flex items-center gap-2 font-mono">
              <Radio className="w-4 h-4 animate-pulse" />
              Offline: Core FastAPI App network stream unavailable.
            </div>
          )}

          {/* Empty State - Triggered when NO hardware is talking to the app */}
          {fleetData && Object.keys(fleetData).length === 0 && (
            <div className="border border-dashed border-gray-800 rounded-xl p-12 text-center max-w-xl mx-auto space-y-4 my-8">
              <div className="w-10 h-10 bg-gray-900 rounded-full flex items-center justify-center mx-auto border border-gray-800 text-gray-500">
                🛰️
              </div>
              <div className="space-y-1">
                <h3 className="text-sm font-bold text-gray-300">No Active Hardware Feeds Found</h3>
                <p className="text-xs text-gray-500 leading-relaxed max-w-sm mx-auto">
                  The dashboard is completely empty because no IoT devices have registered with the platform yet. Return to the Setup tab to configure an initial deployment line.
                </p>
              </div>
              <button 
                onClick={() => setActiveTab('hardware')}
                className="text-[11px] font-mono bg-sky-500 hover:bg-sky-600 text-white px-3 py-1.5 rounded-lg font-bold transition-all"
              >
                Go to Connection Manuals
              </button>
            </div>
          )}

          {/* Dynamic Grid Layout */}
          {fleetData && Object.keys(fleetData).length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(fleetData).map(([id, d]) => {
                const uiMeta = getAlertConfig(d.insight);

                return (
                  <div key={id} className="bg-gray-900 border border-gray-800 rounded-xl p-5 flex flex-col justify-between space-y-4 shadow-sm hover:border-gray-700 transition-colors animate-fadeIn">
                    {/* Header Row */}
                    <div className="flex justify-between items-center border-b border-gray-850 pb-3">
                      <span className="font-bold text-gray-200 tracking-wide text-sm flex items-center gap-2 font-mono">
                        <Activity className="w-3.5 h-3.5 text-emerald-400 animate-pulse-subtle" />
                        {id}
                      </span>
                      <span className="font-mono text-[10px] bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded border border-emerald-500/20 tracking-wider font-bold">
                        STREAM_ACTIVE
                      </span>
                    </div>

                    {/* Variance Window */}
                    <div>
                      <div className="text-2xl font-black text-rose-500 tracking-tight font-mono">
                        +{d.delay_minutes} <span className="text-[10px] font-bold font-sans text-gray-500 uppercase tracking-wider">Mins Variance</span>
                      </div>
                    </div>

                    {/* Operational Telemetry */}
                    <div className="space-y-1.5 font-mono text-[11px]">
                      <div className="bg-gray-950 p-2 rounded border border-gray-850 flex justify-between">
                        <span className="text-gray-500">Manifest Route Target</span>
                        <span className="font-bold text-gray-300 max-w-[170px] truncate">{d.destination} ({d.distance_left} km)</span>
                      </div>

                      <div className="bg-gray-950 p-2 rounded border border-gray-850 flex justify-between">
                        <span className="text-gray-500">Infrastructure Layer</span>
                        <span className="font-semibold text-gray-300">{d.traffic} / {d.weather}</span>
                      </div>

                      <div className="bg-gray-950 p-2 rounded border border-gray-850 flex justify-between">
                        <span className="text-gray-500">Hardware Frame Log</span>
                        <span className="text-gray-300">{d.hours}h driven | {d.load}kg</span>
                      </div>

                      <div className="bg-gray-950 p-2 rounded border border-gray-850 flex justify-between">
                        <span className="text-gray-500">Loss Vector Burn</span>
                        <span className="font-bold text-amber-400">₹{d.loss_inr} <span className="text-[9px] text-gray-500 font-normal">({d.wasted_l}L)</span></span>
                      </div>

                      <div className="bg-gray-950 p-2 rounded border border-gray-850 flex justify-between">
                        <span className="text-gray-500">AI Risk Matrix Weight</span>
                        <span className="font-bold text-red-400">{d.probability} <span className="text-[9px] text-gray-500 font-normal">[{d.factor}]</span></span>
                      </div>
                    </div>

                    {/* Diagnostic AI Alert Context */}
                    <div className={`p-3 rounded-lg text-xs leading-relaxed border flex gap-2 items-start ${uiMeta.border} ${uiMeta.bg}`}>
                      {uiMeta.icon}
                      <span>{d.insight}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}
    </div>
  );
}