class ChatClient {
  constructor(wsUrl) {
    // Dummy attributes
    this.onpm = function(message, user) {};
    this.onchatmessage = function(message, user) {};
    this.onjoinchannel = function(user) {};
    this.onleavechannel = function(user) {};
    this.onerror = function(e) {};

    this.webSocket = new WebSocket(wsUrl);
    this.webSocket.onerror = this.socketClosedHandler.bind(this);
    this.webSocket.onmessage = this.messageHandler.bind(this);

  }

  socketClosedHandler(e) {
    console.error(e);
    this.onerror(e);
  }

  messageHandler(e) {
    let data = JSON.parse(e.data);
    if(typeof data['type'] === 'undefined') {
        console.log("Received message without type parameter, ignoring")
    }
    else {
        switch(data['type']){
            case 'join_channel':
                this.onjoinchannel(data['user']);
                break;
            case 'leave_channel':
                this.onleavechannel(data['user']);
                break;
            case 'pm':
                this.onpm(data['message'], data['user']);
                break;
            case 'message':
                this.onchatmessage(data['message'], data['user']);
                break;
            default:
                console.log("Received message with invalid type " + data['type'] + ",ignoring");
        }
    }
  }

  _sendMessage(data) {
      this.webSocket.send(JSON.stringify(data));
  }

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
          'target': target
      });
  }

}