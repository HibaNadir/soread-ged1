import { useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo2m.png";
import { apiRequest } from "../services/api";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Veuillez remplir tous les champs.");
      return;
    }

    setIsLoading(true);

    try {
      const tokens = await apiRequest("/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: email, password }),
      });

      localStorage.setItem("access_token", tokens.access);
      localStorage.setItem("refresh_token", tokens.refresh);
      navigate("/dashboard");
    } catch {
      setError("Identifiants incorrects ou serveur indisponible.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">

      <div className="login-left">

        <img
          src={logo}
          alt="Logo 2M"
          className="login-logo"
        />

        <h1>SOREAD GED</h1>

        <p>
          Plateforme collaborative de gestion électronique
          des documents.
        </p>

      </div>

      <div className="login-right">

        <div className="login-card">

          <h2>Bienvenue</h2>

          <p className="login-subtitle">
            Connectez-vous à votre espace de travail
          </p>

          <form onSubmit={handleSubmit}>

            {error && <div className="login-error">{error}</div>}

            <label>Adresse e-mail</label>

            <input
              type="email"
              placeholder="exemple@entreprise.ma"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <label>Mot de passe</label>

            <input
              type="password"
              placeholder="Votre mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <div className="login-options">

              <label className="remember">
                <input type="checkbox" />
                Se souvenir de moi
              </label>

              <a href="#">
                Mot de passe oublié ?
              </a>

            </div>

            <button type="submit" className="login-button">
              {isLoading ? "Connexion..." : "Se connecter"}
            </button>

          </form>

        </div>

      </div>

    </div>
  );
}