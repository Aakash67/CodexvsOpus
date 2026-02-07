import "./Sidebar.css";

const navItems = [
  { label: "Dashboard", icon: "📊", active: true },
  { label: "Customers", icon: "👥" },
  { label: "Revenue", icon: "💰" },
  { label: "Products", icon: "📦" },
  { label: "Reports", icon: "📈" },
  { label: "Settings", icon: "⚙️" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <span className="sidebar-logo-icon">◆</span>
        <span className="sidebar-logo-text">Acme</span>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <a
            key={item.label}
            href="#"
            className={`sidebar-link${item.active ? " sidebar-link--active" : ""}`}
          >
            <span className="sidebar-link-icon">{item.icon}</span>
            <span>{item.label}</span>
          </a>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="sidebar-avatar">AR</div>
          <div className="sidebar-user-info">
            <span className="sidebar-user-name">Aarthy R.</span>
            <span className="sidebar-user-role">Admin</span>
          </div>
        </div>
      </div>
    </aside>
  );
}

