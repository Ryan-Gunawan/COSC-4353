
import React, { createContext, useEffect, useState } from 'react';
import { io } from 'socket.io-client';

// Create a context for the socket
export const SocketContext = createContext();

// Replace with your actual server URL
const SOCKET_SERVER_URL = "http://localhost:5000";

const SocketProvider = ({ children }) => {
  const [socket] = useState(() => io(SOCKET_SERVER_URL, { withCredentials: true }));

  useEffect(() => {
    // Function to join the room
    const joinRoom = () => {
      socket.emit('join');
    };

    // Handle socket connection
    socket.on('connect', () => {
      console.log('Connected to socket server');
      joinRoom(); // Join the room on connection
    });

    // Handle reconnection
    socket.on('reconnect', (attempt) => {
      console.log(`Reconnected to socket server on attempt ${attempt}`);
      joinRoom(); // Rejoin the room after reconnection
    });

    // Handle disconnection
    socket.on('disconnect', () => {
      console.log('Disconnected from socket server');
    });

    // Cleanup on unmount
    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('reconnect');
    };
  }, [socket]);

  return (
    <SocketContext.Provider value={{ socket }}>
      {children}
    </SocketContext.Provider>
  );
};

export default SocketProvider;

