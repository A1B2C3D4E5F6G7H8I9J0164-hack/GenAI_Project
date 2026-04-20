import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  LineChart,
  Line,
  BarChart,
  Bar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import {
  Activity,
  Zap,
  TrendingUp,
  AlertTriangle,
  Cloud,
  ArrowRight,
} from 'lucide-react';
import StatCard from '../components/StatCard';
import GlassCard from '../components/GlassCard';
import LoadingSpinner from '../components/LoadingSpinner';
import Logo from '../components/Logo';
import { PageMotion, Stagger, StaggerItem } from '../components/PageMotion';
import { chartTooltipProps } from '../lib/chartTheme';
import { getSampleData } from '../api/client';
import { useDataContext } from '../App';

const PIE_COLORS = ['#22d3ee', '#a855f7', '#34d399', '#f472b6', '#fbbf24', '#60a5fa', '#fb923c'];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-lg border border-cyan-500/35 bg-[rgba(9,9,14,0.97)] px-3 py-2 shadow-2xl shadow-black/60 backdrop-blur-sm">
        <p className="text-zinc-400 text-xs mb-1">Hour {label}:00</p>
        <p className="text-cyan-300 font-semibold text-base tabular-nums">{payload[0].value.toFixed(4)} kW</p>
      </div>
    );
  }
  return null;
};

const UploadPrompt = () => {
  return (
    <div className="flex flex-col items-center justify-center py-16 sm:py-24 page-transition">
      <div className="relative w-full max-w-lg">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/15 to-violet-500/15 rounded-2xl blur-2xl" />
        <div className="relative glass-panel border-cyan-500/25 p-10 sm:p-12 rounded-2xl">
          <div className="flex justify-center mb-6">
            <div className="rounded-2xl border border-cyan-500/30 bg-cyan-500/10 p-4">
              <Cloud className="w-12 h-12 text-cyan-400" aria-hidden />
            </div>
          </div>
          <h2 className="text-2xl font-semibold text-center text-white mb-3">Connect your telemetry</h2>
          <p className="text-zinc-400 text-center mb-8 leading-relaxed">
            Upload EV charging station data to unlock demand curves, validation charts, and agent-driven infrastructure planning.
          </p>
          <div className="flex flex-col gap-3 items-center">
            <Link
              to="/batch"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-cyan-500 text-zinc-950 font-semibold text-sm hover:bg-cyan-400 transition-colors w-full sm:w-auto"
            >
              Go to ingest
              <ArrowRight className="w-4 h-4" aria-hidden />
            </Link>
            <p className="text-zinc-500 text-sm text-center">
              CSV or Excel with time and demand columns
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const { dataUploaded } = useDataContext();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getSampleData();
        setData(result);
        // eslint-disable-next-line no-unused-vars
      } catch (err) {
        setError('Failed to connect to the API. Start the backend server and try again.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const peakHourBars = useMemo(() => {
    if (!data?.hourly_demand?.length) return [];
    return [...data.hourly_demand]
      .sort((a, b) => b.demand - a.demand)
      .slice(0, 8)
      .map((row, i) => ({
        name: `${row.hour}h`,
        demand: row.demand,
        rank: i + 1,
      }));
  }, [data]);

  const radarModelHealth = useMemo(() => {
    if (!data?.summary) return [];
    const { summary, hourly_demand } = data;
    const vol = hourly_demand?.length
      ? Math.min(
        100,
        Math.sqrt(
          hourly_demand.reduce((s, h) => s + Math.pow(h.demand - summary.avg_demand, 2), 0) /
          hourly_demand.length
        ) * 400
      )
      : 40;
    const headroom = summary.max_demand > 0.4 ? 55 : 88;
    const coverage = Math.min(100, (summary.total_records / 150) * 18);
    return [
      { metric: 'Dataset depth', value: Math.round(coverage), fullMark: 100 },
      { metric: 'Peak exposure', value: Math.round(Math.min(100, summary.max_demand * 180)), fullMark: 100 },
      { metric: 'Load stability', value: Math.round(100 - vol), fullMark: 100 },
      { metric: 'Grid headroom', value: Math.round(headroom), fullMark: 100 },
      { metric: 'Avg utilization', value: Math.round(Math.min(100, summary.avg_demand * 220)), fullMark: 100 },
    ];
  }, [data]);

  const pieWeekShare = useMemo(() => {
    if (!data?.day_of_week?.length) return [];
    const total = data.day_of_week.reduce((s, d) => s + (d.demand || 0), 0) || 1;
    return data.day_of_week.map((d) => ({
      name: d.day,
      value: Math.round(((d.demand || 0) / total) * 1000) / 10,
    }));
  }, [data]);

  if (loading) return <LoadingSpinner message="Loading analytics" />;

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center page-transition">
        <div className="rounded-2xl border border-red-500/25 bg-red-500/10 p-4 mb-6">
          <AlertTriangle className="w-12 h-12 text-red-400" aria-hidden />
        </div>
        <h2 className="text-2xl font-semibold text-white mb-2">Connection error</h2>
        <p className="text-zinc-400 max-w-md leading-relaxed">{error}</p>
      </div>
    );
  }

  // Safely extract data with fallbacks
  const summary = data?.summary || { avg_demand: 0, max_demand: 0, total_records: 0 };
  const hourly_demand = data?.hourly_demand || [];
  const price_vs_demand = data?.price_vs_demand || [];
  const day_of_week = data?.day_of_week || [];

  return (
    <PageMotion className="space-y-6 sm:space-y-8 page-transition">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start gap-4 min-w-0">
          <Logo size="md" className="shrink-0" />
          <div className="min-w-0">
            <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight text-white">
              Operations Overview
            </h1>
            <p className="text-zinc-400 mt-2 max-w-2xl leading-relaxed">
              Model health, demand shape, and correlation signals from your latest dataset processing.
            </p>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-300">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" aria-hidden />
            Live dataset
          </span>
          <Link
            to="/predict"
            className="inline-flex items-center gap-1.5 rounded-full border border-white/10 px-3 py-1.5 text-xs font-medium text-zinc-300 hover:bg-white/5 transition-colors"
          >
            Inference
            <ArrowRight className="h-3.5 w-3.5" aria-hidden />
          </Link>
        </div>
      </div>

      <GlassCard title="Data Pipeline" icon={Activity} className="bg-zinc-950/40 border-cyan-500/15">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm text-zinc-400">
              Upload station files in CSV, JSON, or Parquet format. Batch processing runs feature extraction and model inference automatically.
            </p>
          </div>
          <Link
            to="/batch"
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-cyan-500/40 bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-300 hover:bg-cyan-500/20 transition-colors shrink-0"
          >
            Go to ingest
            <ArrowRight className="h-4 w-4" aria-hidden />
          </Link>
        </div>
      </GlassCard>

      <Stagger className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <StaggerItem>
          <StatCard
            title="Average Base Demand"
            value={`${summary.avg_demand.toFixed(3)} kW`}
            icon={Activity}
            color="cyan"
          />
        </StaggerItem>
        <StaggerItem>
          <StatCard
            title="Peak Observed Load"
            value={`${summary.max_demand.toFixed(3)} kW`}
            icon={Zap}
            color="magenta"
          />
        </StaggerItem>
        <StaggerItem>
          <StatCard
            title="Active Model"
            value="Ensemble"
            icon={TrendingUp}
            color="green"
            subtitle="HGB + Gradient Boosting"
          />
        </StaggerItem>
        <StaggerItem>
          <StatCard
            title="Grid Stress"
            value={summary.max_demand > 0.4 ? 'Elevated' : 'Nominal'}
            icon={AlertTriangle}
            color={summary.max_demand > 0.4 ? 'orange' : 'cyan'}
          />
        </StaggerItem>
      </Stagger>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <GlassCard title="Average Daily Load Profile" className="lg:col-span-2 min-h-[380px]">
          <div className="h-full w-full min-h-[300px]">
            {hourly_demand && hourly_demand.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={hourly_demand}>
                  <defs>
                    <linearGradient id="colorDemand" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                  <XAxis dataKey="hour" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey="demand"
                    stroke="#22d3ee"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorDemand)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : null}
          </div>
        </GlassCard>

        <GlassCard title="Model Health Radar" className="min-h-[380px]">
          {radarModelHealth.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={radarModelHealth} cx="50%" cy="50%" outerRadius="75%">
                <PolarGrid stroke="#374151" />
                <PolarAngleAxis dataKey="metric" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar
                  name="Score"
                  dataKey="value"
                  stroke="#a855f7"
                  fill="#a855f7"
                  fillOpacity={0.25}
                  strokeWidth={2}
                />
                <Tooltip {...chartTooltipProps} />
              </RadarChart>
            </ResponsiveContainer>
          ) : null}
          <p className="text-xs text-zinc-500 mt-2">
            Composite view derived from record count, peaks, and variability in the hourly series.
          </p>
        </GlassCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard title="Top Hours by Demand" className="min-h-[320px]">
          {peakHourBars.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={peakHourBars} layout="vertical" margin={{ left: 8, right: 16 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                <XAxis type="number" stroke="#9ca3af" />
                <YAxis dataKey="name" type="category" stroke="#9ca3af" width={48} />
                <Tooltip {...chartTooltipProps} />
                <Bar dataKey="demand" fill="#22d3ee" radius={[0, 4, 4, 0]} name="Demand (kW)" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-zinc-500">No hourly data to rank.</p>
          )}
        </GlassCard>

        <GlassCard title="Weekly Load Share" className="min-h-[320px]">
          {pieWeekShare.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={pieWeekShare}
                  cx="50%"
                  cy="50%"
                  innerRadius={56}
                  outerRadius={96}
                  paddingAngle={2}
                  dataKey="value"
                  nameKey="name"
                  label={false}
                >
                  {pieWeekShare.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip {...chartTooltipProps} />
                <Legend wrapperStyle={{ fontSize: 12, paddingTop: 8 }} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-zinc-500">Day-of-week breakdown unavailable.</p>
          )}
        </GlassCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <GlassCard title="Day-of-Week Pattern" className="min-h-[320px]">
          {day_of_week && day_of_week.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={day_of_week}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                <XAxis dataKey="day" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip {...chartTooltipProps} />
                <Line
                  type="monotone"
                  dataKey="demand"
                  stroke="#e879f9"
                  strokeWidth={2}
                  dot={{ fill: '#e879f9', r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : null}
        </GlassCard>

        <GlassCard title="Price vs Demand" className="col-span-1 lg:col-span-2 min-h-[320px]">
          {price_vs_demand && price_vs_demand.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <ScatterChart margin={{ top: 12, right: 12, bottom: 12, left: 12 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                <XAxis dataKey="price" stroke="#9ca3af" type="number" name="Price" />
                <YAxis dataKey="demand" stroke="#9ca3af" type="number" name="Demand" />
                <Tooltip
                  {...chartTooltipProps}
                  cursor={{ strokeDasharray: '3 3', stroke: 'rgba(34,211,238,0.45)' }}
                />
                <Scatter name="Observations" data={price_vs_demand} fill="#34d399" fillOpacity={0.65} />
              </ScatterChart>
            </ResponsiveContainer>
          ) : null}
        </GlassCard>
      </div>

      <GlassCard title="Pipeline Status" className="bg-zinc-950/30 border-cyan-500/15">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/25 text-center">
            <p className="text-cyan-300 font-semibold text-2xl tabular-nums">
              {summary?.total_records ? Number(summary.total_records).toLocaleString() : '0'}
            </p>
            <p className="text-zinc-500 text-xs mt-1">Records processed</p>
          </div>
          <div className="p-4 rounded-xl bg-violet-500/10 border border-violet-500/25 text-center">
            <p className="text-violet-300 font-semibold text-2xl">Ensemble</p>
            <p className="text-zinc-500 text-xs mt-1">HGB + GBR</p>
          </div>
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-center">
            <p className="text-emerald-300 font-semibold text-2xl">Ready</p>
            <p className="text-zinc-500 text-xs mt-1">Inference queue</p>
          </div>
        </div>
      </GlassCard>
    </PageMotion>
  );
};

export default Dashboard;
