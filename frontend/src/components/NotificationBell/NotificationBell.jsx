import { useState, useEffect } from 'react';
import { FaRegBell } from "react-icons/fa";
import { io } from 'socket.io-client';
import './NotificationBell.css'

const NotificationBell = () => {

    const [hasUnread, setHasUnread] = useState(false);

    // useEffect(() => {
    //     // Connect to backend
    //     const socket = io('http://localhost:5000');
    //     // Listen on 'unread_notification'
    //     socket.on('unread_notification', (data) => {
    //         setHasUnread(data.has_unread);
    //     });
    //
    //     // Cleanup on component unmount
    //     return () => {
    //         socket.disconnect();
    //     }
    // }, []);

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
