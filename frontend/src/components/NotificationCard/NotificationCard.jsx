import './NotificationCard.css'
const NotificationCard = ({ title, date, message, onDelete, onMarkRead }) => {

    return (
        <div className="notification-card">
            <div className="notification-content">
                <h4>{title}</h4>
                <p>{date}</p>
                <p>{message}</p>
            </div>
            <div className="notification-actions">
                <button onClick={onDelete} className="delete-btn">Delete</button>
                {/* <button onClick={onMarkRead} className="mark-read-btn">Mark as Read</button>*/}
            </div>
        </div>
    )
}
export default NotificationCard
