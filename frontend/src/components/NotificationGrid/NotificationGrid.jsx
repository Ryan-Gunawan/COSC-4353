import { useState } from "react";
import NotificationCard from "../NotificationCard/NotificationCard";

const NotificationGrid = () => {

    // List of test notifications
    const [notifications, setNotifications] = useState([
        {
            id: 1,
            title: 'New Event Available',
            date: '2024-09-17',
            message: 'There is a new event that matches your skills.',
        },
        {
            id: 2,
            title: 'Reminder: Volunteer Training',
            date: '2024-09-16',
            message: 'Don\'t forget about the volunteer training tomorrow.',
        },
        {
            id: 3,
            title: 'Your Feedback is Needed',
            date: '2024-09-15',
            message: 'Please provide feedback on your recent event participation.',
        },
    ]);

    // Handler functions
    const handleDelete = (id) => {
        setNotifications(notifications.filter(notification => notification.id !== id));
    };

    const handleMarkRead = (id) => {
        alert(`Notification ${id} marked as read!`);
    };

    return (

        <div className="notification-grid">
            {notifications.length === 0 ? (
                <p>No notifications available.</p>
            ) : (
                notifications.map(notification => (
                    <NotificationCard
                        key={notification.id}
                        title={notification.title}
                        date={notification.date}
                        message={notification.message}
                        onDelete={() => handleDelete(notification.id)}
                        onMarkAsRead={() => handleMarkRead(notification.id)}
                    />
                ))
            )}
        </div>
    )
}
export default NotificationGrid
