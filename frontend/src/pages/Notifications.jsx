import { useState } from "react";
import MainLayout from "../layouts/MainLayout";

export default function Notifications() {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: "document",
      icon: "📄",
      title: "Nouveau document ajouté",
      message: "Le document « Rapport annuel 2026 » a été ajouté.",
      date: "Il y a 10 minutes",
      unread: true,
    },
    {
      id: 2,
      type: "share",
      icon: "👥",
      title: "Document partagé avec vous",
      message: "Malak a partagé « Présentation projet GED » avec vous.",
      date: "Il y a 1 heure",
      unread: true,
    },
    {
      id: 3,
      type: "comment",
      icon: "💬",
      title: "Nouveau commentaire",
      message: "Ahmed a commenté le document « Contrat de partenariat ».",
      date: "Hier",
      unread: false,
    },
    {
      id: 4,
      type: "space",
      icon: "📁",
      title: "Invitation à un espace",
      message: "Vous avez été invité(e) à rejoindre l'espace « Projet GED ».",
      date: "Il y a 2 jours",
      unread: false,
    },
  ]);

  const markAsRead = (id) => {
    setNotifications(
      notifications.map((notification) =>
        notification.id === id
          ? { ...notification, unread: false }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(
      notifications.map((notification) => ({
        ...notification,
        unread: false,
      }))
    );
  };

  const unreadCount = notifications.filter(
    (notification) => notification.unread
  ).length;

  return (
    <MainLayout>
      <div className="notifications-header">
        <div>
          <h1>Notifications</h1>
          <p>
            Vous avez {unreadCount} notification(s) non lue(s).
          </p>
        </div>

        <button
          className="btn-mark-all"
          onClick={markAllAsRead}
        >
          Tout marquer comme lu
        </button>
      </div>

      <div className="notifications-list">
        {notifications.map((notification) => (
          <div
            className={`notification-card ${
              notification.unread ? "unread" : ""
            }`}
            key={notification.id}
          >
            <div className="notification-icon">
              {notification.icon}
            </div>

            <div className="notification-content">
              <h3>{notification.title}</h3>

              <p>{notification.message}</p>

              <small>{notification.date}</small>
            </div>

            {notification.unread && (
              <button
                className="btn-read"
                onClick={() => markAsRead(notification.id)}
              >
                Marquer comme lu
              </button>
            )}
          </div>
        ))}
      </div>
    </MainLayout>
  );
}