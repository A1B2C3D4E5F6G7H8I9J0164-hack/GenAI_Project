import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import {
  UploadCloud,
  CheckCircle2,
  FileJson,
  AlertCircle,
  Activity,
  Bot,
  ArrowRight,
  Loader2,
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { processBatch } from '../api/client';
import GlassCard from '../components/GlassCard';
import StatCard from '../components/StatCard';
import { PageMotion } from '../components/PageMotion';
import { chartTooltipProps } from '../lib/chartTheme';
import { cn } from '../lib/utils';
import { useDataContext } from '../App';

const BatchProcess = () => {
  const { setDataUploaded } = useDataContext();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && (selected.name.endsWith('.csv') || selected.name.endsWith('.xlsx'))) {
      setFile(selected);
      setError(null);
    } else {
      setFile(null);
      setError('Select a valid .csv or .xlsx file.');
    }
  };

  const handleProcess = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    try {
      const res = await processBatch(file);
      setResult(res);
      setDataUploaded(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Processing failed. Check the file format.');
    } finally {
      setLoading(false);
    }
  };

  const triggerFileSelect = () => {
    fileInputRef.current.click();
  };

  const chartData = [];
  if (result && result.actuals && result.actuals.length > 0) {
    const limit = Math.min(result.actuals.length, 100);
    for (let i = 0; i < limit; i++) {
      chartData.push({
        index: i,
        actual: result.actuals[i],
        predicted: result.predictions[i],
      });
    }
  }

  const errorHistogram =
    chartData.length > 0
      ? chartData.slice(0, 40).map((row, i) => ({
        i,
        error: Math.abs(row.actual - row.predicted),
      }))
      : [];

  return (
    <PageMotion className="space-y-6 sm:space-y-8 page-transition">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight text-white">Batch ingest</h1>
        <p className="text-zinc-400 mt-2 max-w-2xl leading-relaxed">
          Upload station logs for feature extraction and batch inference. When labels exist, validation charts appear automatically.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <GlassCard className="lg:col-span-4" title="Upload" icon={UploadCloud}>
          <div
            role="button"
            tabIndex={0}
            onClick={triggerFileSelect}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') triggerFileSelect();
            }}
            className={cn(
              'border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-all duration-300',
              file
                ? 'border-emerald-500/45 bg-emerald-500/5'
                : 'border-cyan-500/25 bg-black/25 hover:bg-cyan-500/5 hover:border-cyan-400/50'
            )}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden"
              accept=".csv,.xlsx"
            />
            {file ? (
              <>
                <FileJson className="w-12 h-12 text-emerald-400 mb-3" aria-hidden />
                <p className="font-semibold text-emerald-200 break-all px-2">{file.name}</p>
                <p className="text-xs text-zinc-500 mt-1">{(file.size / 1024).toFixed(1)} KB</p>
              </>
            ) : (
              <>
                <UploadCloud className="w-12 h-12 text-cyan-400/90 mb-3" aria-hidden />
                <p className="font-medium text-zinc-300 text-sm">Select a telemetry file</p>
                <p className="text-xs text-zinc-500 mt-1">CSV or Excel</p>
              </>
            )}
          </div>

          {error && (
            <div className="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" aria-hidden />
              <p className="text-sm text-red-200">{error}</p>
            </div>
          )}

          <div className="mt-6">
            <button
              type="button"
              onClick={handleProcess}
              disabled={!file || loading}
              className="btn-glow w-full inline-flex items-center justify-center gap-2 disabled:opacity-50 disabled:grayscale"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin shrink-0" aria-hidden />
                  Processing
                </>
              ) : (
                'Run pipeline'
              )}
            </button>
          </div>
        </GlassCard>

        {result ? (
          <div className="lg:col-span-8 flex flex-col gap-6 animation-fade-in">
            <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
              {result.total_records !== undefined && (
                <StatCard
                  title="Records processed"
                  value={result.total_records?.toLocaleString?.() || '0'}
                  color="cyan"
                />
              )}
              {result.r2_score !== null && result.r2_score !== undefined && (
                <>
                  <StatCard
                    title="R-squared"
                    value={`${100-Math.abs((result.r2_score * 100).toFixed(1))}%`}
                    color="green"
                  />
                  {result.mae !== undefined && (
                    <StatCard
                      title="Mean absolute error"
                      value={`${100*result.mae.toFixed(4)}`}
                      color="magenta"
                      className="hidden lg:flex"
                    />
                  )}
                </>
              )}
            </div>

            <GlassCard
              className="border-violet-500/25 bg-gradient-to-br from-violet-500/10 to-transparent"
              title="Next step"
              icon={Bot}
            >
              <p className="text-sm text-zinc-400 mb-4 leading-relaxed">
                Batch output is ready. Run the infrastructure agent to synthesize recommendations from this dataset.
              </p>
              <Link
                to="/planner"
                className="inline-flex items-center gap-2 rounded-xl bg-violet-500/20 border border-violet-500/40 px-5 py-2.5 text-sm font-semibold text-violet-200 hover:bg-violet-500/30 transition-colors"
              >
                Open agent planner
                <ArrowRight className="w-4 h-4" aria-hidden />
              </Link>
            </GlassCard>

            {chartData.length > 0 ? (
              <>
                <GlassCard title="Validation: actual vs predicted (first 100 rows)" className="flex-grow min-h-[360px]">
                  <div className="h-full w-full min-h-[280px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={chartData} margin={{ top: 12, right: 12, left: 0, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
                        <XAxis dataKey="index" hide />
                        <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 11 }} />
                        <Tooltip {...chartTooltipProps} />
                        <Line type="monotone" dataKey="actual" name="Actual" stroke="#34d399" strokeWidth={2} dot={false} />
                        <Line
                          type="monotone"
                          dataKey="predicted"
                          name="Predicted"
                          stroke="#c084fc"
                          strokeWidth={2}
                          strokeDasharray="6 4"
                          dot={false}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </GlassCard>

                {errorHistogram.length > 0 && (
                  <GlassCard title="Absolute error by row (sample)" className="min-h-[280px]">
                    <div className="h-[220px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={errorHistogram} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.35} />
                          <XAxis dataKey="i" hide />
                          <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 10 }} />
                          <Tooltip {...chartTooltipProps} />
                          <Bar dataKey="error" fill="#22d3ee" radius={[2, 2, 0, 0]} name="|error|" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </GlassCard>
                )}
              </>
            ) : (
              <GlassCard className="flex flex-col items-center justify-center p-12 text-center min-h-[360px]">
                <CheckCircle2 className="w-14 h-14 text-emerald-400 mb-4" aria-hidden />
                <h3 className="text-xl font-semibold text-white mb-2">Pipeline complete</h3>
                <p className="text-zinc-400 max-w-md leading-relaxed">
                  Generated predictions for {result.total_records || '?'} rows. No target labels were found, so validation charts are hidden.
                </p>
                <div className="mt-8 border border-white/10 rounded-xl overflow-hidden w-full max-w-md text-left">
                  <div className="bg-white/5 px-4 py-2 text-xs font-mono text-zinc-500 border-b border-white/10 flex">
                    <div className="w-12">Hour</div>
                    <div className="flex-grow text-right">Predicted (kW)</div>
                  </div>
                  {result.predictions && result.hours ? (
                    result.predictions.slice(0, 5).map((p, i) => (
                      <div
                        key={i}
                        className="px-4 py-2 text-sm font-mono flex border-b border-white/5 last:border-0 hover:bg-white/5"
                      >
                        <div className="w-12 text-zinc-500">{result.hours[i] || i}</div>
                        <div className="flex-grow text-right text-cyan-300 font-semibold tabular-nums">{p?.toFixed?.(4) || 'N/A'}</div>
                      </div>
                    ))
                  ) : (
                    <div className="px-4 py-2 text-sm text-center text-zinc-500">
                      No prediction data available
                    </div>
                  )}
                  <div className="px-4 py-2 text-xs text-center text-zinc-500 bg-white/5">
                    Showing {Math.min(result.predictions?.length || 0, 5)} of {result.total_records || '?'}
                  </div>
                </div>
              </GlassCard>
            )}
          </div>
        ) : (
          <div className="lg:col-span-8 glass-panel border-dashed border-white/10 flex flex-col items-center justify-center min-h-[400px] text-center p-8 rounded-xl">
            <div className="w-20 h-20 rounded-2xl border border-white/10 bg-black/30 flex items-center justify-center mb-6">
              <Activity className="w-9 h-9 text-zinc-600" aria-hidden />
            </div>
            <h3 className="text-lg font-semibold text-zinc-400 mb-2">Waiting for a file</h3>
            <p className="text-zinc-500 max-w-md text-sm leading-relaxed">
              After processing, accuracy metrics, validation curves, and a shortcut to the agent appear here.
            </p>
          </div>
        )}
      </div>
    </PageMotion>
  );
};

export default BatchProcess;
