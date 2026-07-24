import { Link } from "react-router-dom";
import logo from "../assets/logo2m.png";

export default function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="logo">

        <img src={logo} alt="2M"/>

        <h2>SOREAD GED</h2>

      </div>

      <nav>

        <Link to="/dashboard">🏠 Dashboard</Link>

        <Link to="/documents">📄 Documents</Link>

        <Link to="/folders">📁 Dossiers</Link>

        <Link to="/spaces">👥 Espaces</Link>

        <Link to="/search">🔎 Recherche</Link>

        <Link to="/notifications">🔔 Notifications</Link>

        <Link to="/profile">👤 Profil</Link>

      </nav>

    </aside>
  );
}