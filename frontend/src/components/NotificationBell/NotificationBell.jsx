import { useState, useEffect, useContext } from 'react';
import { FaRegBell } from "react-icons/fa";
import './NotificationBell.css'
import axios from 'axios';


const NotificationBell = () => {

    const [hasUnread, setHasUnread] = useState(false);

    // const checkUnreadNotifications = async () => {
    //     try {
    //         const response = await axios.get('http://localhost:5000/api/notifications/unread', { withCredentials: true });
    //         setHasUnread(response.data.has_unread);
    //     } catch (error) {
    //         console.error('Error checking unread notifications:', error);
    //     }
    // };
    //
    // useEffect(() => {
    //     // socket.on('connect')
    //     checkUnreadNotifications();
    //
    //     // Listen on 'unread_notification'
    //     socket.on('unread_notification', (data) => {
    //         setHasUnread(data.has_unread);
    //     });
    //
    //     // Cleanup on component unmount
    //     return () => {
    //         socket.off('unread_notification')
    //     }
    // },);

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
