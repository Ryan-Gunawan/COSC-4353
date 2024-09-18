import { useState } from 'react';
import { FaRegBell } from "react-icons/fa";
const NotificationBell = () => {

    return (
        <div className="bell" style={styles.bell}>
            <FaRegBell />
        </div>
    );

};

const styles = {
    bell: {
        scale: '1.5',
        position: 'relative',
        paddingTop: '2px',
        marginLeft: '10px',
    },
}
export default NotificationBell;
