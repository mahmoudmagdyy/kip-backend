class BookingWebSocket {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectInterval = 3000;
    }

    connect(token) {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/admin/bookings/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = (event) => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
            this.requestBookings();
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.socket.onclose = (event) => {
            console.log('WebSocket disconnected');
            this.handleReconnect();
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    handleMessage(data) {
        switch (data.type) {
            case 'booking_created':
                this.onBookingCreated(data.data);
                break;
            case 'booking_updated':
                this.onBookingUpdated(data.data);
                break;
            case 'booking_deleted':
                this.onBookingDeleted(data.data);
                break;
            case 'bookings_data':
                this.onBookingsData(data.data);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    onBookingCreated(bookingData) {
        console.log('New booking created:', bookingData);
        
        // Show notification
        this.showNotification('New Booking Created', 
            `${bookingData.user_details.first_name} ${bookingData.user_details.last_name} booked ${bookingData.service_name} for ${bookingData.booking_date} at ${bookingData.booking_time}`,
            'success'
        );
        
        // Add to bookings list if it exists
        if (window.addBookingToList) {
            window.addBookingToList(bookingData);
        }
        
        // Update statistics if function exists
        if (window.updateBookingStats) {
            window.updateBookingStats();
        }
    }

    onBookingUpdated(bookingData) {
        console.log('Booking updated:', bookingData);
        
        // Show notification
        this.showNotification('Booking Updated', 
            `Booking for ${bookingData.user_details.first_name} ${bookingData.user_details.last_name} has been updated`,
            'info'
        );
        
        // Update booking in list if function exists
        if (window.updateBookingInList) {
            window.updateBookingInList(bookingData);
        }
    }

    onBookingDeleted(bookingData) {
        console.log('Booking deleted:', bookingData);
        
        // Show notification
        this.showNotification('Booking Deleted', 
            `Booking for ${bookingData.user_details.first_name} ${bookingData.user_details.last_name} has been deleted`,
            'warning'
        );
        
        // Remove from bookings list if function exists
        if (window.removeBookingFromList) {
            window.removeBookingFromList(bookingData.id);
        }
    }

    onBookingsData(bookingsData) {
        console.log('Bookings data received:', bookingsData);
        
        // Update bookings list if function exists
        if (window.updateBookingsList) {
            window.updateBookingsList(bookingsData);
        }
    }

    requestBookings() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                type: 'get_bookings'
            }));
        }
    }

    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectInterval);
        } else {
            console.error('Max reconnection attempts reached');
        }
    }

    showNotification(title, message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <h4>${title}</h4>
                <p>${message}</p>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        // Add styles if not already added
        if (!document.getElementById('notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    border-left: 4px solid #007bff;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    border-radius: 4px;
                    padding: 16px;
                    max-width: 400px;
                    z-index: 10000;
                    animation: slideIn 0.3s ease-out;
                }
                .notification-success { border-left-color: #28a745; }
                .notification-warning { border-left-color: #ffc107; }
                .notification-error { border-left-color: #dc3545; }
                .notification-content h4 {
                    margin: 0 0 8px 0;
                    font-size: 16px;
                    font-weight: 600;
                }
                .notification-content p {
                    margin: 0 0 12px 0;
                    font-size: 14px;
                    color: #666;
                }
                .notification-close {
                    position: absolute;
                    top: 8px;
                    right: 8px;
                    background: none;
                    border: none;
                    font-size: 18px;
                    cursor: pointer;
                    color: #999;
                }
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(styles);
        }
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
        
        // Close button functionality
        notification.querySelector('.notification-close').addEventListener('click', () => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        });
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

// Initialize WebSocket when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Get token from localStorage or sessionStorage
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    
    if (token) {
        window.bookingWebSocket = new BookingWebSocket();
        window.bookingWebSocket.connect(token);
    }
});

// Export for use in other scripts
window.BookingWebSocket = BookingWebSocket;
