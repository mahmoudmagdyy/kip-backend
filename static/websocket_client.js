/**
 * WebSocket Client for Real-time Booking Dashboard
 * Use this in Flutter Web or any web application
 */

class BookingWebSocketClient {
    constructor(options = {}) {
        this.url = options.url || 'ws://localhost:8000/ws/admin/bookings/';
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
        this.reconnectInterval = options.reconnectInterval || 3000;
        this.autoConnect = options.autoConnect !== false;
        
        // Event callbacks
        this.onConnect = options.onConnect || (() => {});
        this.onDisconnect = options.onDisconnect || (() => {});
        this.onError = options.onError || (() => {});
        this.onBookingCreated = options.onBookingCreated || (() => {});
        this.onBookingUpdated = options.onBookingUpdated || (() => {});
        this.onBookingDeleted = options.onBookingDeleted || (() => {});
        this.onBookingsData = options.onBookingsData || (() => {});
        
        if (this.autoConnect) {
            this.connect();
        }
    }

    connect() {
        try {
            console.log('🔌 Connecting to WebSocket:', this.url);
            this.socket = new WebSocket(this.url);
            
            this.socket.onopen = (event) => {
                console.log('✅ WebSocket connected');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.onConnect(event);
                
                // Request current bookings
                this.requestBookings();
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('📨 Received message:', data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('❌ Error parsing message:', error);
                }
            };

            this.socket.onclose = (event) => {
                console.log('❌ WebSocket disconnected');
                this.isConnected = false;
                this.onDisconnect(event);
                this.handleReconnect();
            };

            this.socket.onerror = (error) => {
                console.error('💥 WebSocket error:', error);
                this.onError(error);
            };

        } catch (error) {
            console.error('❌ Failed to connect:', error);
            this.onError(error);
        }
    }

    disconnect() {
        if (this.socket) {
            console.log('🔌 Disconnecting WebSocket');
            this.socket.close();
            this.socket = null;
            this.isConnected = false;
        }
    }

    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`🔄 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectInterval);
        } else {
            console.log('❌ Max reconnection attempts reached');
        }
    }

    handleMessage(data) {
        switch (data.type) {
            case 'booking_created':
                console.log('🆕 New booking created:', data.data);
                this.onBookingCreated(data.data);
                break;
            case 'booking_updated':
                console.log('✏️ Booking updated:', data.data);
                this.onBookingUpdated(data.data);
                break;
            case 'booking_deleted':
                console.log('🗑️ Booking deleted:', data.data);
                this.onBookingDeleted(data.data);
                break;
            case 'bookings_data':
                console.log('📋 Received bookings data:', data.data);
                this.onBookingsData(data.data);
                break;
            default:
                console.log('❓ Unknown message type:', data.type);
        }
    }

    requestBookings() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log('📤 Requesting current bookings...');
            this.socket.send(JSON.stringify({
                type: 'get_bookings'
            }));
        } else {
            console.warn('⚠️ Cannot request bookings - WebSocket not connected');
        }
    }

    // Utility method to send custom messages
    sendMessage(type, data = {}) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                type: type,
                ...data
            }));
        } else {
            console.warn('⚠️ Cannot send message - WebSocket not connected');
        }
    }

    // Get connection status
    getStatus() {
        return {
            connected: this.isConnected,
            readyState: this.socket ? this.socket.readyState : null,
            reconnectAttempts: this.reconnectAttempts
        };
    }
}

// Flutter Web Integration Helper
class FlutterWebSocketHelper {
    constructor() {
        this.client = null;
        this.bookings = [];
    }

    initialize(options = {}) {
        this.client = new BookingWebSocketClient({
            ...options,
            onConnect: () => {
                console.log('🎉 Connected to booking WebSocket');
                if (options.onConnect) options.onConnect();
            },
            onDisconnect: () => {
                console.log('💔 Disconnected from booking WebSocket');
                if (options.onDisconnect) options.onDisconnect();
            },
            onError: (error) => {
                console.error('❌ WebSocket error:', error);
                if (options.onError) options.onError(error);
            },
            onBookingCreated: (booking) => {
                this.bookings.unshift(booking);
                console.log('🆕 New booking added to list');
                if (options.onBookingCreated) options.onBookingCreated(booking, this.bookings);
            },
            onBookingUpdated: (booking) => {
                const index = this.bookings.findIndex(b => b.id === booking.id);
                if (index !== -1) {
                    this.bookings[index] = booking;
                } else {
                    this.bookings.unshift(booking);
                }
                console.log('✏️ Booking updated in list');
                if (options.onBookingUpdated) options.onBookingUpdated(booking, this.bookings);
            },
            onBookingDeleted: (booking) => {
                this.bookings = this.bookings.filter(b => b.id !== booking.id);
                console.log('🗑️ Booking removed from list');
                if (options.onBookingDeleted) options.onBookingDeleted(booking, this.bookings);
            },
            onBookingsData: (bookings) => {
                this.bookings = bookings;
                console.log('📋 Bookings list updated');
                if (options.onBookingsData) options.onBookingsData(bookings);
            }
        });
    }

    connect() {
        if (this.client) {
            this.client.connect();
        }
    }

    disconnect() {
        if (this.client) {
            this.client.disconnect();
        }
    }

    getBookings() {
        return this.bookings;
    }

    requestBookings() {
        if (this.client) {
            this.client.requestBookings();
        }
    }

    getStatus() {
        return this.client ? this.client.getStatus() : { connected: false };
    }
}

// Export for use in Flutter Web
if (typeof window !== 'undefined') {
    window.BookingWebSocketClient = BookingWebSocketClient;
    window.FlutterWebSocketHelper = FlutterWebSocketHelper;
}

// Node.js export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BookingWebSocketClient, FlutterWebSocketHelper };
}
