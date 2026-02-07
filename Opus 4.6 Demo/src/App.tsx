import "./App.css";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import MetricCard from "./components/MetricCard";

const metrics = [
  {
    icon: "💰",
    label: "Total Revenue",
    value: "$48,352",
    change: "+12.5%",
    changeType: "up" as const,
  },
  {
    icon: "👥",
    label: "Active Users",
    value: "2,420",
    change: "+8.1%",
    changeType: "up" as const,
  },
  {
    icon: "📦",
    label: "New Orders",
    value: "1,210",
    change: "-3.2%",
    changeType: "down" as const,
  },
  {
    icon: "⭐",
    label: "Satisfaction",
    value: "98.5%",
    change: "+0.4%",
    changeType: "up" as const,
  },
];

export default function App() {
  return (
    <div className="app-layout">
      <Sidebar />

      <div className="app-main">
        <Header />

        <main className="app-content">
          <section className="metrics-section">
            <h2 className="section-title">Key Metrics</h2>
            <div className="metrics-grid">
              {metrics.map((m) => (
                <MetricCard key={m.label} {...m} />
              ))}
            </div>
          </section>

          <section className="placeholder-section">
            <div className="placeholder-card">
              <h3>Recent Activity</h3>
              <p>Charts and activity feed will go here.</p>
            </div>
            <div className="placeholder-card">
              <h3>Quick Actions</h3>
              <p>Shortcuts and tools will go here.</p>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
