import { useState, useEffect } from "react";
import NotificationCard from "../NotificationCard/NotificationCard";

const NotificationGrid = () => {

    // List of notifications
    const [notifications, setNotifications] = useState([]);

    // Fetch notifications when the component mounts
    useEffect(() => {
        fetch("http://localhost:5000/api/notifications", {
            method: 'GET',
            credentials: 'include', // include cookies to handle session
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load notifications');
                }
                return response.json();
            })
            .then(data => {
                //console.log("Fetched notifications:", data); // debug
                setNotifications(data);
            })
            .catch(error => console.error('Error:', error));
    }, []); // empty dependency array means this runs once on component mount


    // Handler functions
    const handleDelete = async (id) => {
        try {
            const response = await fetch("http://localhost:5000/api/notifications", {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ notification_id: id }), // Send notification_id in request body
            });

            console.log('Response:', response);

            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error deleting notification: ${errorData.msg}`);
            }

            // Update local state to reflect the deletion
            setNotifications(notifications.filter(notification => notification.id !== id));
        } catch (error) {
            console.error('Error deleting notification:', error);
        }
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
