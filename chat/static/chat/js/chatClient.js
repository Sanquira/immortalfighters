class ChatClient {
    constructor(wsUrl) {
        // Dummy attributes
        // More info on these types of messages can be found in chat/components/messages.py
        this.onPrivateMessage = function ({target_user, user, time, message}) {};
        this.onChatMessage = function ({user, time, message}) {};
        this.onJoinChannel = function ({user, time, users, history}) {};
        this.onUserJoinChannel = function ({user, time}) {};
        this.onUserLeaveChannel = function ({user, time}) {};

        // All error handling will be in this function, list of possible errors can be found in chat/components/messages.py
        // It contains one additional possible error and that is websocket_error that is created on the client when the
        // websocket stream is closed
        this.onErrorMessage = function (error) {};

        this.webSocket = new WebSocket(wsUrl);
        this.webSocket.onerror = this.socketErrorHandler.bind(this);
        this.webSocket.onclose = this.socketCloseHandler.bind(this);
        this.webSocket.onmessage = this.messageHandler.bind(this);
        this.joined = false;

    }

    // Simulates websocket_error message as it would arrive from server in case of socket closure
    socketErrorHandler(e) {
        console.error(e);
        var error = {
            "type": "error",
            "error_type": "websocket_closed",
            "message": e.data,
            "time": new Date().getTime() / 1000,
        };
        this.onErrorMessage(error)
    }

    socketCloseHandler() {
        var error = {
            "type": "error",
            "error_type": "websocket_closed",
            "message": "Websocket closed",
            "time": new Date().getTime() / 1000,
        };
        this.onErrorMessage(error)
    }

    messageHandler(e) {
        let data = JSON.parse(e.data);
        if (typeof data['type'] === 'undefined') {
            console.debug("Received message without type parameter, ignoring")
        } else {
            console.debug("Received message with type " + data['type'] + ", processing");
            this._process_message(data);
        }
    }

    _process_message(message) {
        var message_type = message["type"];
        delete message.type;
        switch (message_type) {
            case 'user_join_channel':
                this.onUserJoinChannel(message);
                break;
            case 'user_leave_channel':
                this.onUserLeaveChannel(message);
                break;
            case 'private_message':
                this.onPrivateMessage(message);
                break;
            case 'chat_message':
                this.onChatMessage(message);
                break;
            case 'join_channel':
                this.onJoinChannel(message);
                this.joined = true;
                break;
            case 'error':
                this.onErrorMessage(message);
                break;
            default:
                console.debug("Received message with invalid type " + message['type'] + ", ignoring");
        }
    }

    _sendMessage(data) {
        this.webSocket.send(JSON.stringify(data));
    }

    // Public methods
    sendChatMessage(message) {
        this._sendMessage({
            'type': "chat_message",
            'message': message
        });
    }

    sendPrivateMessage(message, target) {
        this._sendMessage({
            'type': "private_message",
            'message': message,
            'target_user': target
        });
    }

    simulateHistory(history) {
        for (const message of history) {
            this._process_message(message)
        }
    }

    hasJoined() {
        return this.joined;
    }
}