import "./MetricCard.css";

interface MetricCardProps {
  icon: string;
  label: string;
  value: string;
  change: string;      // e.g. "+12.5%"
  changeType: "up" | "down" | "neutral";
}

export default function MetricCard({
  icon,
  label,
  value,
  change,
  changeType,
}: MetricCardProps) {
  return (
    <div className="metric-card">
      <div className="metric-card-header">
        <span className="metric-card-icon">{icon}</span>
        <span
          className={`metric-card-change metric-card-change--${changeType}`}
        >
          {changeType === "up" && "↑ "}
          {changeType === "down" && "↓ "}
          {change}
        </span>
      </div>

      <div className="metric-card-value">{value}</div>
      <div className="metric-card-label">{label}</div>
    </div>
  );
}

