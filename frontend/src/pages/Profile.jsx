import { useEffect, useState } from "react";
import MainLayout from "../layouts/MainLayout";
import { getProfile, updateProfile } from "../services/userService";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({ email: "", first_name: "", last_name: "", service: "" });
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    getProfile()
      .then((user) => {
        setProfile(user);
        setForm({
          email: user.email || "",
          first_name: user.first_name || "",
          last_name: user.last_name || "",
          service: user.service || "",
        });
      })
      .catch((loadError) => setError(loadError.message))
      .finally(() => setIsLoading(false));
  }, []);

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSave = async (event) => {
    event.preventDefault();
    setIsSaving(true);
    setError("");
    setMessage("");

    try {
      const updatedProfile = await updateProfile(form);
      setProfile(updatedProfile);
      setForm({
        email: updatedProfile.email || "",
        first_name: updatedProfile.first_name || "",
        last_name: updatedProfile.last_name || "",
        service: updatedProfile.service || "",
      });
      setIsEditing(false);
      setMessage("Profil modifié avec succès.");
    } catch (saveError) {
      setError(saveError.message);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <MainLayout><div className="profile-loading">Chargement du profil...</div></MainLayout>;
  }

  if (!profile) {
    return <MainLayout><div className="page-error">{error || "Profil introuvable."}</div></MainLayout>;
  }

  const fullName = `${profile.first_name || ""} ${profile.last_name || ""}`.trim() || profile.username;
  const initials = fullName.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase();

  return (
    <MainLayout>
      <div className="profile-header">
        <h1>Mon profil</h1>
        <p>Gérez vos informations personnelles et vos préférences.</p>
      </div>

      {error && <div className="page-error">{error}</div>}
      {message && <div className="page-success">{message}</div>}

      <div className="profile-container">

        <div className="profile-card">

          <div className="profile-avatar">
            {initials}
          </div>

          <h2>{fullName}</h2>

          <p className="profile-role">
            {profile.role || "Utilisateur"}
          </p>

          <button className="btn-edit" onClick={() => { setIsEditing(true); setMessage(""); }}>
            {isEditing ? "Modification en cours" : "Modifier le profil"}
          </button>

        </div>

        <div className="profile-info">

          <h2>Informations personnelles</h2>

          {isEditing ? (
            <form className="profile-edit-form" onSubmit={handleSave}>
              <label>Prénom<input name="first_name" value={form.first_name} onChange={handleChange} /></label>
              <label>Nom<input name="last_name" value={form.last_name} onChange={handleChange} /></label>
              <label>Email<input type="email" name="email" value={form.email} onChange={handleChange} /></label>
              <label>Service<input name="service" value={form.service} onChange={handleChange} /></label>
              <div className="profile-edit-actions">
                <button className="btn-add" type="submit" disabled={isSaving}>{isSaving ? "Enregistrement..." : "Enregistrer"}</button>
                <button className="folder-cancel" type="button" onClick={() => setIsEditing(false)}>Annuler</button>
              </div>
            </form>
          ) : (
            <>
              <div className="info-row"><span>Nom complet</span><strong>{fullName}</strong></div>
              <div className="info-row"><span>Email</span><strong>{profile.email || "Non renseigné"}</strong></div>
            </>
          )}

          <div className="info-row">
            <span>Rôle</span>
            <strong>{profile.role || "Utilisateur"}</strong>
          </div>

          <div className="info-row">
            <span>Date d'inscription</span>
            <strong>{new Date(profile.date_joined).toLocaleDateString("fr-FR")}</strong>
          </div>

        </div>

      </div>
    </MainLayout>
  );
}