import "./Header.css";

export default function Header() {
  return (
    <header className="header">
      <div className="header-left">
        <h1 className="header-title">Dashboard</h1>
        <span className="header-subtitle">Welcome back, Aarthy 👋</span>
      </div>

      <div className="header-right">
        <div className="header-search">
          <span className="header-search-icon">🔍</span>
          <input
            className="header-search-input"
            type="text"
            placeholder="Search…"
          />
        </div>

        <button className="header-icon-btn" title="Notifications">
          🔔
        </button>
      </div>
    </header>
  );
}

