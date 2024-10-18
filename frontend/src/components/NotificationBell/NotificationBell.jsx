import { useState, useEffect } from 'react';
import { FaRegBell } from "react-icons/fa";
import { io } from 'socket.io-client';
import './NotificationBell.css'
import axios from 'axios';

const socket = io('http://localhost:5000');

const NotificationBell = () => {

    const [hasUnread, setHasUnread] = useState(false);

    const checkUnreadNotifications = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/notifications/unread', { withCredentials: true });
            setHasUnread(response.data.has_unread);
        } catch (error) {
            console.error('Error checking undread notifications:', error);
        }
    };

    useEffect(() => {
        checkUnreadNotifications();

        // Listen on 'unread_notification'
        socket.on('unread_notification', (data) => {
            setHasUnread(data.has_unread);
        });

        // Cleanup on component unmount
        return () => {
            // socket.disconnect();
            socket.off('unread_notification')
        }
    }, []);

    return (
        <div className="bell" style={styles.bell}>
            <FaRegBell />
            {hasUnread && <span className="red-dot"></span>}
        </div>
    );

};

const styles = {
    bell: {
        scale: '1.5',
        position: 'relative',
        paddingTop: '2px',
        marginLeft: '10px',
        display: 'inlineBlock'
    },
}
export default NotificationBell;
