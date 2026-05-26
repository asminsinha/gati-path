import React from 'react';

export default function App() {
  // Enterprise Module Distribution Manifest containing real individual link hooks
  const systemModules = [
    {
      id: 'gati-path',
      title: 'Gati-Path Engine Terminal',
      url: 'http://127.0.0.1:8000/gati-path/dashboard', // Standalone project webpage link
      folder: 'services/gati_path',
      icon: '🗺️',
      description: 'Geospatial logistics platform aggregating structural transit network metrics, real-time Open-Meteo vectors, and dynamic IoT tracking payloads.',
      ready: true,
    },
    {
      id: 'dhan-sanchay',
      title: 'Dhan-Sanchay Treasury',
      url: 'http://127.0.0.1:8001/dhan-sanchay/dashboard',
      folder: 'services/dhan_sanchay',
      icon: '📈',
      description: 'Financial forecasting terminal, risk scoring configurations, and micro-transaction validation layers.',
      ready: false,
    },
    {
      id: 'jan-shakti',
      title: 'Jan-Shakti Portal',
      url: 'http://127.0.0.1:8002/jan-shakti/dashboard',
      folder: 'services/jan_shakti',
      icon: '👥',
      description: 'Resource balancing grid, biometric identification verification handlers, and field utility task distribution protocols.',
      ready: false,
    },
    {
      id: 'rakshak-ai',
      title: 'Rakshak-AI Guardian',
      url: 'http://127.0.0.1:8003/rakshak-ai/dashboard',
      folder: 'services/rakshak_ai',
      icon: '🛡️',
      description: 'Threat mitigation matrix, automated safety anomaly override routines, and deep security pattern matching.',
      ready: false,
    }
  ];

  const handleLaunchWorkspace = (url) => {
    // Open the separate individual webpage instance in a new tab
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-950 text-gray-200">
      <header className="bg-gray-900/50 backdrop-blur-md border-b border-gray-800 px-6 py-4 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2 select-none">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-ping" />
            <h1 className="text-sm font-black tracking-wider text-white font-mono uppercase">
              VITARAI // DISTRIBUTED_WORKSPACE_ROUTER
            </h1>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-8">
        <div className="max-w-xl py-4">
          <h2 className="text-2xl font-bold text-white tracking-tight">Cluster Node Partition Registry</h2>
          <p className="text-gray-400 text-xs mt-1">
            Initialize an isolated standalone system project node by launching its corresponding gateway link below.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {systemModules.map((mod) => (
            <div
              key={mod.id}
              onClick={() => mod.ready && handleLaunchWorkspace(mod.url)}
              className={`border rounded-xl p-6 flex flex-col justify-between transition-all relative overflow-hidden group ${
                mod.ready 
                  ? 'bg-gray-900/60 border-gray-800 hover:border-sky-500/40 cursor-pointer shadow-sm hover:bg-gray-900/90' 
                  : 'bg-gray-950/20 border-gray-900 opacity-40 cursor-not-allowed select-none'
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="text-2xl p-2 bg-gray-950 rounded-lg border border-gray-850">
                    {mod.icon}
                  </div>
                  <span className="font-mono text-[9px] font-bold tracking-widest uppercase px-2 py-0.5 rounded border bg-gray-950 text-gray-500 border-gray-850">
                    {mod.ready ? 'ONLINE_LINK' : 'STUB_OFFLINE'}
                  </span>
                </div>
                
                <div>
                  <h3 className="text-sm font-bold text-gray-200 group-hover:text-sky-400 transition-colors">
                    {mod.title}
                  </h3>
                  <code className="text-[10px] text-gray-400 block font-mono mt-0.5">{mod.url}</code>
                </div>

                <p className="text-gray-400 text-xs leading-relaxed pt-1">
                  {mod.description}
                </p>
              </div>
              
              {mod.ready && (
                <div className="mt-6 font-mono text-[10px] text-sky-500 text-right font-bold opacity-0 group-hover:opacity-100 transition-opacity">
                  LAUNCH STANDALONE APP ➔
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}