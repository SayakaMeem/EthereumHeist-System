"use client";

import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

const API_BASE = "http://127.0.0.1:8000";

type CsvResponse = {
  file_name: string;
  rows: number;
  columns: string[];
  preview: Record<string, any>[];
};

type GraphResponse = {
  file_name: string;
  node_count: number;
  edge_count: number;
  nodes: {
    id: string;
    label: string;
    layer: number;
    role: string;
  }[];
  edges: {
    id: string;
    source: string;
    target: string;
    transaction_type: string;
    amount: string;
    label: string;
  }[];
};

type HeistLabelResponse = {
  file_name: string;
  rows: number;
  columns: string[];
  preview: Record<string, any>[];
};

export default function Page() {
  const [address, setAddress] = useState(
    "0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23"
  );

  const [maxDepth, setMaxDepth] = useState(1);
  const [maxAddresses, setMaxAddresses] = useState(1);
  const [crawlMissing, setCrawlMissing] = useState(false);

  const [summary, setSummary] = useState<any>(null);
  const [layers, setLayers] = useState<CsvResponse | null>(null);
  const [edges, setEdges] = useState<CsvResponse | null>(null);
  const [graph, setGraph] = useState<GraphResponse | null>(null);
  const [serviceResult, setServiceResult] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);

  const [heistLabels, setHeistLabels] = useState<Record<string, any>[]>([]);
  const [selectedLabelIndex, setSelectedLabelIndex] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [experimentLimit, setExperimentLimit] = useState(3);
  const [experimentMaxDepth, setExperimentMaxDepth] = useState(1);
  const [experimentMaxAddresses, setExperimentMaxAddresses] = useState(1);
  const [experimentCrawlMissing, setExperimentCrawlMissing] = useState(false);
  const [experimentResult, setExperimentResult] = useState<any>(null);
  const [experimentCsv, setExperimentCsv] = useState<CsvResponse | null>(null);
  const [experimentLoading, setExperimentLoading] = useState(false);
  const [experimentError, setExperimentError] = useState("");

  function getFileName(path: string) {
    return path?.split("\\").pop()?.split("/").pop() || path;
  }

  function findAddressFromRow(row: Record<string, any>) {
    const keys = Object.keys(row);

    const addressKey =
      keys.find((key) => key.toLowerCase().includes("address")) ||
      keys.find((key) => key.toLowerCase().includes("account")) ||
      keys.find((key) => key.toLowerCase().includes("wallet"));

    if (addressKey) {
      return String(row[addressKey] ?? "").trim();
    }

    for (const key of keys) {
      const value = String(row[key] ?? "").trim();

      if (value.startsWith("0x") && value.length >= 40) {
        return value;
      }
    }

    return "";
  }

  function getLabelText(row: Record<string, any>) {
    const keys = Object.keys(row);

    const labelKey =
      keys.find((key) => key.toLowerCase().includes("heist")) ||
      keys.find((key) => key.toLowerCase().includes("event")) ||
      keys.find((key) => key.toLowerCase().includes("name")) ||
      keys.find((key) => key.toLowerCase().includes("label"));

    if (labelKey) {
      return String(row[labelKey] ?? "").trim();
    }

    return findAddressFromRow(row);
  }

  useEffect(() => {
    async function loadHeistLabels() {
      try {
        const res = await fetch(`${API_BASE}/heist-labels`);

        if (!res.ok) {
          return;
        }

        const data: HeistLabelResponse = await res.json();

        if (data.preview && data.preview.length > 0) {
          setHeistLabels(data.preview);
        }
      } catch {
        console.log("Failed to load heist labels");
      }
    }

    loadHeistLabels();
  }, []);

  async function runTracking() {
    try {
      setLoading(true);
      setError("");
      setSummary(null);
      setLayers(null);
      setEdges(null);
      setGraph(null);
      setServiceResult(null);
      setStats(null);

      const trackingUrl =
        `${API_BASE}/track/multi-hop/${address}` +
        `?max_depth=${maxDepth}` +
        `&max_addresses_per_layer=${maxAddresses}` +
        `&beta=0.01` +
        `&omega=1000` +
        `&crawl_missing=${crawlMissing}`;

      const trackingRes = await fetch(trackingUrl);

      if (!trackingRes.ok) {
        throw new Error("Tracking request failed. Check backend terminal.");
      }

      const trackingSummary = await trackingRes.json();

      if (trackingSummary.error) {
        throw new Error(trackingSummary.error);
      }

      setSummary(trackingSummary);

      const layersFile = getFileName(trackingSummary.layers_file || "");
      const edgesFile = getFileName(trackingSummary.edges_file || "");

      if (layersFile) {
        const layersRes = await fetch(
          `${API_BASE}/tracking/csv/${encodeURIComponent(layersFile)}`
        );

        if (layersRes.ok) {
          setLayers(await layersRes.json());
        }
      }

      if (edgesFile) {
        const edgesRes = await fetch(
          `${API_BASE}/tracking/csv/${encodeURIComponent(edgesFile)}`
        );

        if (edgesRes.ok) {
          setEdges(await edgesRes.json());
        }
      }

      if ((trackingSummary.tracked_edge_count ?? 0) > 0 && edgesFile) {
        const serviceRes = await fetch(
          `${API_BASE}/tracking/enrich-service/${encodeURIComponent(edgesFile)}`
        );

        if (serviceRes.ok) {
          setServiceResult(await serviceRes.json());
        } else {
          setServiceResult({
            total_edges: trackingSummary.tracked_edge_count ?? 0,
            matched_service_provider_edges: 0,
            unique_service_providers: 0,
            matched_preview: [],
          });
        }

        const statsRes = await fetch(
          `${API_BASE}/tracking/stats/${encodeURIComponent(edgesFile)}`
        );

        if (statsRes.ok) {
          setStats(await statsRes.json());
        }

        const graphRes = await fetch(
          `${API_BASE}/graph/tracking/${encodeURIComponent(edgesFile)}?limit=30`
        );

        if (graphRes.ok) {
          setGraph(await graphRes.json());
        }
      } else {
        setServiceResult({
          total_edges: 0,
          matched_service_provider_edges: 0,
          unique_service_providers: 0,
          matched_preview: [],
          output_file: "",
        });

        setStats({
          total_edges: 0,
          transaction_type_counts: {},
          label_counts: {},
          matched_service_edges: 0,
          unmatched_service_edges: 0,
          unique_service_providers: 0,
        });

        setGraph({
          file_name: edgesFile,
          node_count: 0,
          edge_count: 0,
          nodes: [],
          edges: [],
        });
      }
    } catch (err: any) {
      setError(err.message || "Unknown error occurred");
    } finally {
      setLoading(false);
    }
  }

  async function runExperiment() {
    try {
      setExperimentLoading(true);
      setExperimentError("");
      setExperimentResult(null);
      setExperimentCsv(null);

      const experimentUrl =
        `${API_BASE}/experiment/run` +
        `?limit=${experimentLimit}` +
        `&max_depth=${experimentMaxDepth}` +
        `&max_addresses_per_layer=${experimentMaxAddresses}` +
        `&crawl_missing=${experimentCrawlMissing}`;

      const experimentRes = await fetch(experimentUrl);

      if (!experimentRes.ok) {
        throw new Error("Experiment request failed. Check backend terminal.");
      }

      const experimentData = await experimentRes.json();

      if (experimentData.error) {
        throw new Error(experimentData.error);
      }

      setExperimentResult(experimentData);

      const csvRes = await fetch(`${API_BASE}/experiment/csv/experiment_result.csv`);

      if (csvRes.ok) {
        setExperimentCsv(await csvRes.json());
      }
    } catch (err: any) {
      setExperimentError(err.message || "Unknown experiment error occurred");
    } finally {
      setExperimentLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-black text-white p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-3">
          EthereumHeist AML System
        </h1>

        <p className="text-gray-400 mb-8">
          XBlockFlow-inspired multihop TPP tracking system using local CPU and
          Etherscan API.
        </p>

        <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Run Multihop Tracking</h2>

          <label className="block text-sm text-gray-400 mb-2">
            Select Heist / Placement Address
          </label>

          <select
            value={selectedLabelIndex}
            onChange={(e) => {
              const index = e.target.value;
              setSelectedLabelIndex(index);

              if (index !== "") {
                const selectedRow = heistLabels[Number(index)];
                const selectedAddress = findAddressFromRow(selectedRow);

                if (selectedAddress) {
                  setAddress(selectedAddress);
                }
              }
            }}
            className="w-full rounded-lg bg-black border border-gray-700 p-3 text-white mb-5"
          >
            <option value="">Manual address input</option>

            {heistLabels.map((row, index) => {
              const rowAddress = findAddressFromRow(row);
              const labelText = getLabelText(row);

              return (
                <option key={index} value={index}>
                  {labelText} - {rowAddress}
                </option>
              );
            })}
          </select>

          <label className="block text-sm text-gray-400 mb-2">
            Heist / Placement Address
          </label>

          <input
            value={address}
            onChange={(e) => {
              setAddress(e.target.value);
              setSelectedLabelIndex("");
            }}
            className="w-full rounded-lg bg-black border border-gray-700 p-3 text-green-400 mb-5"
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <div>
              <label className="block text-sm text-gray-400 mb-2">
                Max Depth
              </label>
              <input
                type="number"
                value={maxDepth}
                onChange={(e) => setMaxDepth(Number(e.target.value))}
                className="w-full rounded-lg bg-black border border-gray-700 p-3"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">
                Max Addresses Per Layer
              </label>
              <input
                type="number"
                value={maxAddresses}
                onChange={(e) => setMaxAddresses(Number(e.target.value))}
                className="w-full rounded-lg bg-black border border-gray-700 p-3"
              />
            </div>
          </div>

          <label className="flex items-center gap-3 text-sm text-gray-300 mb-5">
            <input
              type="checkbox"
              checked={crawlMissing}
              onChange={(e) => setCrawlMissing(e.target.checked)}
            />
            Auto crawl missing address from Etherscan
          </label>

          <button
            onClick={runTracking}
            disabled={loading}
            className="rounded-lg bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-6 py-3 font-semibold"
          >
            {loading ? "Running Tracking..." : "Run Tracking"}
          </button>

          <p className="text-yellow-400 text-sm mt-4">
            Recommended first test: max depth = 1, max addresses = 1, auto crawl unchecked.
          </p>
        </section>

        {error && (
          <div className="mb-6 rounded-xl border border-red-700 bg-red-950 p-4 text-red-300">
            Error: {error}
          </div>
        )}

        <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Batch Experiment Mode</h2>

          <p className="text-gray-400 mb-5">
            Run multiple heist addresses and create a thesis-style comparison table.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-5">
            <div>
              <label className="block text-sm text-gray-400 mb-2">
                Number of Heist Addresses
              </label>
              <input
                type="number"
                value={experimentLimit}
                onChange={(e) => setExperimentLimit(Number(e.target.value))}
                className="w-full rounded-lg bg-black border border-gray-700 p-3"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">
                Experiment Max Depth
              </label>
              <input
                type="number"
                value={experimentMaxDepth}
                onChange={(e) => setExperimentMaxDepth(Number(e.target.value))}
                className="w-full rounded-lg bg-black border border-gray-700 p-3"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">
                Experiment Max Addresses
              </label>
              <input
                type="number"
                value={experimentMaxAddresses}
                onChange={(e) =>
                  setExperimentMaxAddresses(Number(e.target.value))
                }
                className="w-full rounded-lg bg-black border border-gray-700 p-3"
              />
            </div>
          </div>

          <label className="flex items-center gap-3 text-sm text-gray-300 mb-5">
            <input
              type="checkbox"
              checked={experimentCrawlMissing}
              onChange={(e) => setExperimentCrawlMissing(e.target.checked)}
            />
            Crawl missing addresses during experiment
          </label>

          <button
            onClick={runExperiment}
            disabled={experimentLoading}
            className="rounded-lg bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 px-6 py-3 font-semibold"
          >
            {experimentLoading ? "Running Experiment..." : "Run Batch Experiment"}
          </button>

          <p className="text-yellow-400 text-sm mt-4">
            Fast test: limit = 3, max depth = 1, max addresses = 1, crawl unchecked.
          </p>
        </section>

        {experimentError && (
          <div className="mb-6 rounded-xl border border-red-700 bg-red-950 p-4 text-red-300">
            Experiment Error: {experimentError}
          </div>
        )}

        {experimentResult && (
          <>
            <section className="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8">
              <InfoCard
                title="Total Experiments"
                value={experimentResult.total_experiments}
                color="text-blue-400"
              />

              <InfoCard
                title="Successful Runs"
                value={experimentResult.successful_runs}
                color="text-green-400"
              />

              <InfoCard
                title="Failed Runs"
                value={experimentResult.failed_runs}
                color="text-red-400"
              />

              <InfoCard
                title="Total Tracked Edges"
                value={experimentResult.total_tracked_edges ?? 0}
                color="text-yellow-400"
              />

              <InfoCard
                title="Average Tracked Edges"
                value={experimentResult.average_tracked_edges ?? 0}
                color="text-orange-400"
              />

              <InfoCard
                title="Max Tracked Edges"
                value={experimentResult.max_tracked_edges ?? 0}
                color="text-purple-400"
              />

              <InfoCard
                title="Total Layer Addresses"
                value={experimentResult.total_layer_addresses ?? 0}
                color="text-cyan-400"
              />

              <InfoCard
                title="Total Service Matches"
                value={experimentResult.total_service_matches ?? 0}
                color="text-pink-400"
              />
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4">
                Experiment Comparison Chart
              </h2>

              <ExperimentCharts data={experimentCsv} />
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4">
                Experiment Result Table
              </h2>

              <div className="mb-5">
                <button
                  onClick={() => downloadExperimentCsv(experimentCsv)}
                  className="rounded-lg bg-cyan-600 hover:bg-cyan-700 px-5 py-3 font-semibold"
                >
                  Download Experiment CSV
                </button>
              </div>

              <DataTable data={experimentCsv} />
            </section>
          </>
        )}

        {summary && (
          <>
            <section className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
              <InfoCard
                title="Visited Addresses"
                value={summary.visited_address_count}
                color="text-blue-400"
              />

              <InfoCard
                title="Tracked Edges"
                value={summary.tracked_edge_count}
                color="text-yellow-400"
              />

              <InfoCard
                title="Layer Addresses"
                value={summary.layer_address_count}
                color="text-green-400"
              />

              <InfoCard
                title="Max Depth"
                value={summary.max_depth}
                color="text-purple-400"
              />

              <InfoCard
                title="Matched Service Edges"
                value={
                  stats?.matched_service_edges ??
                  serviceResult?.matched_service_provider_edges ??
                  0
                }
                color="text-red-400"
              />

              <InfoCard
                title="Unique Services"
                value={
                  stats?.unique_service_providers ??
                  serviceResult?.unique_service_providers ??
                  0
                }
                color="text-pink-400"
              />
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4">
                Result Dashboard
              </h2>

              <ResultCharts
                summary={summary}
                edges={edges}
                serviceResult={serviceResult}
                stats={stats}
              />
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4">Tracking Summary</h2>
              <pre className="bg-black border border-gray-700 rounded-lg p-4 text-green-400 overflow-x-auto text-sm">
                {JSON.stringify(summary, null, 2)}
              </pre>
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4">Export Results</h2>
              <ExportButtons summary={summary} serviceResult={serviceResult} />
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4">
                Transaction Flow Graph
              </h2>
              <TrackingGraph graph={graph} />
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4">
                Service Provider Matching
              </h2>
              <ServiceProviderResult result={serviceResult} />
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4">
                Layering Address Table
              </h2>
              <DataTable data={layers} />
            </section>

            <section className="rounded-xl border border-gray-700 bg-gray-900 p-6">
              <h2 className="text-2xl font-semibold mb-4">
                Transaction Edge Table
              </h2>
              <DataTable data={edges} />
            </section>
          </>
        )}
      </div>
    </main>
  );
}

function InfoCard({
  title,
  value,
  color,
}: {
  title: string;
  value: any;
  color: string;
}) {
  return (
    <div className="rounded-xl border border-gray-700 bg-gray-900 p-5">
      <h2 className="text-sm text-gray-400 mb-2">{title}</h2>
      <p className={`text-2xl font-bold ${color}`}>{value ?? "..."}</p>
    </div>
  );
}

function downloadExperimentCsv(data: CsvResponse | null) {
  if (!data || !data.preview || data.preview.length === 0) {
    return;
  }

  const columns = data.columns;

  const escapeCsv = (value: any) => {
    const text = String(value ?? "");
    return `"${text.replace(/"/g, '""')}"`;
  };

  const csvRows = [
    columns.map(escapeCsv).join(","),
    ...data.preview.map((row) =>
      columns.map((col) => escapeCsv(row[col])).join(",")
    ),
  ];

  const csvContent = csvRows.join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "experiment_result.csv";
  link.click();

  URL.revokeObjectURL(url);
}

function ExperimentCharts({ data }: { data: CsvResponse | null }) {
  if (!data || !data.preview || data.preview.length === 0) {
    return <p className="text-yellow-400">No experiment chart data found.</p>;
  }

  const chartData = data.preview.map((row, index) => {
    const label =
      String(row.heist_label ?? "").trim() ||
      String(row.address ?? "").slice(0, 10) ||
      `Run ${index + 1}`;

    return {
      name: label.length > 12 ? label.slice(0, 12) + "..." : label,
      tracked_edges: Number(row.tracked_edge_count ?? 0),
      layer_addresses: Number(row.layer_address_count ?? 0),
      service_matches: Number(row.matched_service_provider_edges ?? 0),
    };
  });

  return (
    <div className="rounded-xl border border-gray-700 bg-black p-5">
      <h3 className="text-lg font-semibold mb-4">
        Heist-wise Tracking Comparison
      </h3>

      <div className="h-96">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <XAxis dataKey="name" stroke="#cbd5e1" />
            <YAxis stroke="#cbd5e1" allowDecimals={false} />
            <Tooltip />
            <Legend />
            <Bar dataKey="tracked_edges" fill="#eab308" />
            <Bar dataKey="layer_addresses" fill="#22c55e" />
            <Bar dataKey="service_matches" fill="#ef4444" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function ExportButtons({
  summary,
  serviceResult,
}: {
  summary: any;
  serviceResult: any;
}) {
  function getSafeFileName(path: string) {
    return path?.split("\\").pop()?.split("/").pop() || path;
  }

  const edgesFile = getSafeFileName(summary?.edges_file || "");
  const layersFile = getSafeFileName(summary?.layers_file || "");
  const summaryFile = getSafeFileName(summary?.summary_file || "");
  const serviceFile = getSafeFileName(serviceResult?.output_file || "");

  function downloadUrl(fileName: string) {
    return `${API_BASE}/tracking/download/${encodeURIComponent(fileName)}`;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {edgesFile && (
        <a
          href={downloadUrl(edgesFile)}
          className="rounded-lg bg-green-600 hover:bg-green-700 px-5 py-3 text-center font-semibold"
        >
          Download Edges CSV
        </a>
      )}

      {layersFile && (
        <a
          href={downloadUrl(layersFile)}
          className="rounded-lg bg-blue-600 hover:bg-blue-700 px-5 py-3 text-center font-semibold"
        >
          Download Layers CSV
        </a>
      )}

      {summaryFile && (
        <a
          href={downloadUrl(summaryFile)}
          className="rounded-lg bg-purple-600 hover:bg-purple-700 px-5 py-3 text-center font-semibold"
        >
          Download Summary JSON
        </a>
      )}

      {serviceFile && (
        <a
          href={downloadUrl(serviceFile)}
          className="rounded-lg bg-red-600 hover:bg-red-700 px-5 py-3 text-center font-semibold"
        >
          Download Service CSV
        </a>
      )}

      {!edgesFile && !layersFile && !summaryFile && !serviceFile && (
        <p className="text-yellow-400">No export files available yet.</p>
      )}
    </div>
  );
}

function ResultCharts({
  summary,
  edges,
  serviceResult,
  stats,
}: {
  summary: any;
  edges: CsvResponse | null;
  serviceResult: any;
  stats: any;
}) {
  const phaseData = [
    {
      name: "Placement",
      value: 1,
    },
    {
      name: "Layering",
      value: summary?.layer_address_count ?? 0,
    },
    {
      name: "Service Match",
      value:
        stats?.matched_service_edges ??
        serviceResult?.matched_service_provider_edges ??
        0,
    },
  ];

  let transactionTypeData: { name: string; value: number }[] = [];

  if (stats?.transaction_type_counts) {
    transactionTypeData = Object.entries(stats.transaction_type_counts).map(
      ([name, value]) => ({
        name,
        value: Number(value),
      })
    );
  } else if (edges?.preview) {
    const transactionTypeCount: Record<string, number> = {};

    edges.preview.forEach((row) => {
      const txType = String(row.transaction_type ?? "unknown");
      transactionTypeCount[txType] = (transactionTypeCount[txType] || 0) + 1;
    });

    transactionTypeData = Object.entries(transactionTypeCount).map(
      ([name, value]) => ({
        name,
        value,
      })
    );
  }

  const totalEdges =
    stats?.total_edges ??
    serviceResult?.total_edges ??
    summary?.tracked_edge_count ??
    0;

  const matchedEdges =
    stats?.matched_service_edges ??
    serviceResult?.matched_service_provider_edges ??
    0;

  const serviceData = [
    {
      name: "Matched",
      value: matchedEdges,
    },
    {
      name: "Unmatched",
      value: Math.max(totalEdges - matchedEdges, 0),
    },
  ];

  const pieColors = ["#22c55e", "#ef4444", "#38bdf8", "#eab308"];

  return (
    <div>
      {stats && (
        <p className="text-gray-400 mb-5">
          Dashboard uses full CSV data. Total edges:{" "}
          <span className="text-yellow-400">{stats.total_edges}</span>
        </p>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="rounded-xl border border-gray-700 bg-black p-5">
          <h3 className="text-lg font-semibold mb-4">
            Laundering Phase Summary
          </h3>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={phaseData}>
                <XAxis dataKey="name" stroke="#cbd5e1" />
                <YAxis stroke="#cbd5e1" allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="value" fill="#22c55e" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-xl border border-gray-700 bg-black p-5">
          <h3 className="text-lg font-semibold mb-4">
            Transaction Type Distribution
          </h3>

          {transactionTypeData.length > 0 ? (
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={transactionTypeData}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={90}
                    label
                  >
                    {transactionTypeData.map((_, index) => (
                      <Cell
                        key={index}
                        fill={pieColors[index % pieColors.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="text-gray-400">No transaction type data found.</p>
          )}
        </div>

        <div className="rounded-xl border border-gray-700 bg-black p-5">
          <h3 className="text-lg font-semibold mb-4">
            Service Provider Matching
          </h3>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={serviceData}>
                <XAxis dataKey="name" stroke="#cbd5e1" />
                <YAxis stroke="#cbd5e1" allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="value" fill="#ef4444" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

function DataTable({ data }: { data: CsvResponse | null }) {
  if (!data) {
    return <p className="text-gray-400">Loading table...</p>;
  }

  if (!data.preview || data.preview.length === 0) {
    return <p className="text-yellow-400">No rows found.</p>;
  }

  return (
    <div>
      <p className="text-gray-400 mb-3">
        File: <span className="text-green-400">{data.file_name}</span> | Rows:{" "}
        <span className="text-yellow-400">{data.rows}</span>
      </p>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-gray-700 text-left text-gray-300">
              {data.columns.map((col) => (
                <th key={col} className="p-3 whitespace-nowrap">
                  {col}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {data.preview.map((row, index) => (
              <tr key={index} className="border-b border-gray-800">
                {data.columns.map((col) => (
                  <td
                    key={col}
                    className="p-3 text-gray-300 whitespace-nowrap max-w-xs overflow-hidden text-ellipsis"
                  >
                    {String(row[col] ?? "")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ServiceProviderResult({ result }: { result: any }) {
  if (!result) {
    return <p className="text-gray-400">Loading service-provider matching...</p>;
  }

  if (result.error) {
    return <p className="text-red-400">Error: {result.error}</p>;
  }

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
        <div className="rounded-xl border border-gray-700 bg-black p-4">
          <h3 className="text-sm text-gray-400 mb-2">Total Edges</h3>
          <p className="text-2xl font-bold text-yellow-400">
            {result.total_edges ?? 0}
          </p>
        </div>

        <div className="rounded-xl border border-gray-700 bg-black p-4">
          <h3 className="text-sm text-gray-400 mb-2">Matched Service Edges</h3>
          <p className="text-2xl font-bold text-red-400">
            {result.matched_service_provider_edges ?? 0}
          </p>
        </div>

        <div className="rounded-xl border border-gray-700 bg-black p-4">
          <h3 className="text-sm text-gray-400 mb-2">Unique Services</h3>
          <p className="text-2xl font-bold text-pink-400">
            {result.unique_service_providers ?? 0}
          </p>
        </div>
      </div>

      {result.output_file && (
        <p className="text-gray-400 mb-3">
          Output file:{" "}
          <span className="text-green-400 break-all">
            {result.output_file}
          </span>
        </p>
      )}

      {result.matched_preview && result.matched_preview.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-gray-700 text-left text-gray-300">
                {Object.keys(result.matched_preview[0]).map((col) => (
                  <th key={col} className="p-3 whitespace-nowrap">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {result.matched_preview.map((row: any, index: number) => (
                <tr key={index} className="border-b border-gray-800">
                  {Object.keys(result.matched_preview[0]).map((col) => (
                    <td
                      key={col}
                      className="p-3 text-gray-300 whitespace-nowrap max-w-xs overflow-hidden text-ellipsis"
                    >
                      {String(row[col] ?? "")}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-yellow-400">
          No known service-provider address matched in this limited run.
        </p>
      )}
    </div>
  );
}

function TrackingGraph({ graph }: { graph: GraphResponse | null }) {
  if (!graph) {
    return <p className="text-gray-400">Loading graph...</p>;
  }

  if (!graph.nodes || graph.nodes.length === 0) {
    return <p className="text-yellow-400">No graph data found.</p>;
  }

  const width = 1100;
  const height = Math.max(500, graph.nodes.length * 65);

  const layers = Array.from(new Set(graph.nodes.map((n) => n.layer))).sort(
    (a, b) => a - b
  );

  const positions: Record<string, { x: number; y: number }> = {};

  layers.forEach((layer, layerIndex) => {
    const nodesInLayer = graph.nodes.filter((n) => n.layer === layer);
    const x = 130 + layerIndex * 350;

    nodesInLayer.forEach((node, nodeIndex) => {
      const y = 80 + nodeIndex * 70;
      positions[node.id] = { x, y };
    });
  });

  return (
    <div>
      <p className="text-gray-400 mb-4">
        Nodes: <span className="text-green-400">{graph.node_count}</span> | Edges:{" "}
        <span className="text-yellow-400">{graph.edge_count}</span>
      </p>

      <div className="overflow-x-auto rounded-xl border border-gray-700 bg-black p-4">
        <svg width={width} height={height}>
          <defs>
            <marker
              id="arrow"
              markerWidth="10"
              markerHeight="10"
              refX="8"
              refY="3"
              orient="auto"
              markerUnits="strokeWidth"
            >
              <path d="M0,0 L0,6 L9,3 z" fill="gray" />
            </marker>
          </defs>

          {graph.edges.map((edge) => {
            const source = positions[edge.source];
            const target = positions[edge.target];

            if (!source || !target) return null;

            return (
              <line
                key={edge.id}
                x1={source.x + 90}
                y1={source.y}
                x2={target.x - 90}
                y2={target.y}
                stroke="gray"
                strokeWidth="1.5"
                markerEnd="url(#arrow)"
              />
            );
          })}

          {graph.nodes.map((node) => {
            const pos = positions[node.id];

            if (!pos) return null;

            const isPlacement = node.role === "placement";
            const isIntegration = node.role.includes("integration");

            return (
              <g key={node.id}>
                <rect
                  x={pos.x - 90}
                  y={pos.y - 25}
                  width="180"
                  height="50"
                  rx="10"
                  fill={
                    isPlacement
                      ? "#064e3b"
                      : isIntegration
                      ? "#7f1d1d"
                      : "#1e293b"
                  }
                  stroke={
                    isPlacement
                      ? "#22c55e"
                      : isIntegration
                      ? "#ef4444"
                      : "#38bdf8"
                  }
                />
                <text
                  x={pos.x}
                  y={pos.y - 3}
                  textAnchor="middle"
                  fill="white"
                  fontSize="12"
                  fontWeight="bold"
                >
                  {node.label}
                </text>
                <text
                  x={pos.x}
                  y={pos.y + 14}
                  textAnchor="middle"
                  fill="#cbd5e1"
                  fontSize="10"
                >
                  L{node.layer} | {node.role}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
}