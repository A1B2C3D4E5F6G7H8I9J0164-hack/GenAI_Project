import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  ReferenceDot,
  LineChart,
  Line,
} from 'recharts';
import { Target, Zap, AlertTriangle, Loader2, ArrowRight } from 'lucide-react';
import GlassCard from '../components/GlassCard';
import { PageMotion } from '../components/PageMotion';
import { predictSingle } from '../api/client';
import { useDataContext } from '../App';
import { cn } from '../lib/utils';

const InputField = ({ label, value, onChange, type = 'number', step = '0.0001', min, max }) => (
  <div className="flex flex-col gap-1.5">
    <label className="text-sm font-medium text-zinc-400">{label}</label>
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(type === 'number' ? Number(e.target.value) : e.target.value)}
      step={step}
      min={min}
      max={max}
      className={cn(
        'bg-black/40 border border-white/10 rounded-md px-3 py-2 text-white outline-none transition-colors focus:border-cyan-500/50',
        type === 'range' && 'p-0 h-2 bg-zinc-800 rounded-lg appearance-none cursor-pointer'
      )}
    />
    {type === 'range' && (
      <div className="text-right text-xs text-cyan-400 font-mono mt-1 tabular-nums">{value}</div>
    )}
  </div>
);

const Predict = () => {
  const { dataUploaded } = useDataContext();
  const [params, setParams] = useState({
    hour: 12,
    day: 0,
    lag1: 0.15,
    lag2: 0.145,
    lag3: 0.14,
    rolling3: 0.148,
    rolling6: 0.146,
    std3: 0.01,
    price: 0.12,
    stability: 1.0,
    ev_count: 5,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await predictSingle(params);
      // Handle both response formats (prediction or predicted_demand_kw)
      const prediction = res?.prediction ?? res?.predicted_demand_kw ?? null;
      setResult(prediction);
      if (!prediction && prediction !== 0) {
        setError('No prediction value received from API');
      }
    } catch (err) {
      setError('Inference failed. Check that the API is reachable.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const chartData = Array.from({ length: 24 }, (_, i) => ({
    hour: i,
    demand: 0.15 + 0.1 * Math.sin(((i - 6) * Math.PI) / 12),
  }));

  const currentY = result ?? (0.15 + 0.1 * Math.sin(((params.hour - 6) * Math.PI) / 12));

  const residualData = chartData.map((row) => ({
    ...row,
    residual: row.demand - currentY * 0.15,
  }));

  // removed dataUploaded gate

  return (
    <PageMotion className="space-y-6 sm:space-y-8 page-transition">
      <div>
        <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-white">Single-point inference</h1>
        <p className="text-zinc-400 mt-2 max-w-2xl leading-relaxed">
          Feed engineered features into the deployed regressor. The chart below highlights your selected hour against a synthetic daily profile for context.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <GlassCard title="Parameters" icon={Target} className="lg:col-span-4 lg:row-span-2">
          <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
            <div className="space-y-4 pb-4 border-b border-white/5">
              <InputField
                label="Hour of day (0 to 23)"
                type="range"
                min="0"
                max="23"
                step="1"
                value={params.hour}
                onChange={(v) => setParams({ ...params, hour: v })}
              />
              <InputField
                label="Day of week (0 = Monday)"
                type="range"
                min="0"
                max="6"
                step="1"
                value={params.day}
                onChange={(v) => setParams({ ...params, day: v })}
              />
              <InputField
                label="Charging EVs"
                type="range"
                min="0"
                max="50"
                step="1"
                value={params.ev_count}
                onChange={(v) => setParams({ ...params, ev_count: v })}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <InputField label="Lag 1 (kW)" value={params.lag1} onChange={(v) => setParams({ ...params, lag1: v })} />
              <InputField label="Lag 2 (kW)" value={params.lag2} onChange={(v) => setParams({ ...params, lag2: v })} />
              <InputField label="Lag 3 (kW)" value={params.lag3} onChange={(v) => setParams({ ...params, lag3: v })} />
              <InputField label="Rolling 3h" value={params.rolling3} onChange={(v) => setParams({ ...params, rolling3: v })} />
              <InputField label="Rolling 6h" value={params.rolling6} onChange={(v) => setParams({ ...params, rolling6: v })} />
              <InputField label="Std dev 3h" value={params.std3} onChange={(v) => setParams({ ...params, std3: v })} />
              <InputField label="Price ($/kWh)" value={params.price} onChange={(v) => setParams({ ...params, price: v })} />
              <InputField label="Grid stability" value={params.stability} onChange={(v) => setParams({ ...params, stability: v })} />
            </div>
          </div>

          <div className="mt-6">
            <button
              type="button"
              onClick={handlePredict}
              disabled={loading}
              className="btn-glow w-full inline-flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin shrink-0" aria-hidden />
                  Running inference
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 shrink-0" aria-hidden />
                  Run inference
                </>
              )}
            </button>
            {error && <p className="text-red-400 text-xs mt-3 text-center">{error}</p>}
          </div>
        </GlassCard>

        <GlassCard className="lg:col-span-8 flex flex-col items-center justify-center min-h-[200px]" title="Predicted demand">
          <p className="text-zinc-500 text-xs font-medium uppercase tracking-wider mb-3">Target load</p>
          <div className="flex items-baseline justify-center gap-2">
            {result !== null && result !== undefined && typeof result === 'number' ? (
              <>
                <span className="text-5xl sm:text-6xl font-bold tabular-nums bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-violet-400">
                  {(result).toFixed(4)}
                </span>
                <span className="text-xl text-zinc-500 font-medium">kW</span>
              </>
            ) : (
              <>
                <span className="text-5xl sm:text-6xl font-bold text-zinc-700 tabular-nums">—.———</span>
                <span className="text-xl text-zinc-600 font-medium">kW</span>
              </>
            )}
          </div>
        </GlassCard>

        <GlassCard title="Daily profile context" className="lg:col-span-8 min-h-[340px]">
          <div className="h-full w-full min-h-[260px] relative">
            {chartData && chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={chartData} margin={{ top: 16, right: 16, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorDemandPred" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#c084fc" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#c084fc" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
                  <XAxis dataKey="hour" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 11 }} />
                  <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 11 }} domain={[0.05, 0.3]} />
                  <Area
                    type="monotone"
                    dataKey="demand"
                    stroke="#c084fc"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorDemandPred)"
                  />
                  <ReferenceDot x={params.hour} y={currentY} r={8} fill="#22d3ee" stroke="#fff" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[280px] text-zinc-500">No data</div>
            )}
          </div>
        </GlassCard>

        <GlassCard title="Residual vs profile (illustrative)" className="lg:col-span-12 min-h-[280px]">
          <div className="h-[240px] w-full relative">
            {residualData && residualData.length > 0 ? (
              <ResponsiveContainer width="100%" height={240}>
                <LineChart data={residualData} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.35} />
                  <XAxis dataKey="hour" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 11 }} />
                  <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 11 }} />
                  <Line type="monotone" dataKey="residual" stroke="#34d399" strokeWidth={2} dot={false} name="Residual" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[240px] text-zinc-500">No data</div>
            )}
          </div>
          <p className="text-xs text-zinc-500 mt-2">
            Illustrative offset series for comparing the selected hour against the reference curve.
          </p>
        </GlassCard>
      </div>
    </PageMotion>
  );
};

export default Predict;
