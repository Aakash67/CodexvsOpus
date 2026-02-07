const metricData = [
  { label: "Monthly Revenue", value: "$84,230", delta: "+12.8% vs last month", trend: "up" },
  { label: "Active Users", value: "14,392", delta: "+4.1% this week", trend: "up" },
  { label: "Churn Rate", value: "2.4%", delta: "-0.6% improvement", trend: "up" },
  { label: "Open Tickets", value: "37", delta: "+5 today", trend: "down" }
];

const navItems = ["Overview", "Customers", "Billing", "Reports", "Settings"];

function createElement(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (typeof content === "string") node.textContent = content;
  return node;
}

function Sidebar(items) {
  const aside = createElement("aside", "sidebar");
  const brand = createElement("div", "brand", "Northstar SaaS");
  const list = createElement("ul", "nav-list");

  items.forEach((item, index) => {
    const li = document.createElement("li");
    const link = createElement("a", `nav-item${index === 0 ? " is-active" : ""}`, item);
    link.href = "#";
    li.appendChild(link);
    list.appendChild(li);
  });

  aside.append(brand, list);
  return aside;
}

function Header() {
  const header = createElement("header", "header");
  const copy = createElement("div");
  const title = createElement("h1", null, "Dashboard");
  const subtitle = createElement("p", null, "Here is a quick snapshot of your product performance.");
  const button = createElement("button", "cta", "Create Report");

  copy.append(title, subtitle);
  header.append(copy, button);
  return header;
}

function MetricCard(metric) {
  const card = createElement("article", "metric-card");
  const label = createElement("p", "metric-label", metric.label);
  const value = createElement("p", "metric-value", metric.value);
  const deltaClass = metric.trend === "up" ? "metric-delta is-up" : "metric-delta is-down";
  const delta = createElement("span", deltaClass, metric.delta);

  card.append(label, value, delta);
  return card;
}

function MainContent(metrics) {
  const shell = createElement("main", "main-shell");
  const metricsGrid = createElement("section", "metrics-grid");
  const panel = createElement("section", "panel");
  const panelTitle = createElement("h2", null, "Notes");
  const panelBody = createElement(
    "p",
    null,
    "This layout is intentionally lightweight and componentized so you can quickly swap content, add charts, or plug in real API data."
  );

  metrics.forEach((metric) => metricsGrid.appendChild(MetricCard(metric)));
  panel.append(panelTitle, panelBody);
  shell.append(Header(), metricsGrid, panel);

  return shell;
}

function App() {
  const app = createElement("div", "dashboard");
  app.append(Sidebar(navItems), MainContent(metricData));
  return app;
}

document.getElementById("app")?.appendChild(App());
