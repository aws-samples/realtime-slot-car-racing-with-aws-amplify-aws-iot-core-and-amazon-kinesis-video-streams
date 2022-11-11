import { Client, Message } from 'paho-mqtt'
import * as CryptoJS from 'crypto-js'

import awsExports from "../aws-exports";

class MqttClient {

  constructor(client, connectionOptions, topics) {
    this._topics = topics
    this._mainTopic = this._topics[0]
    this._connected = false

    this.client = client
    this.client.onConnectionLost = this.onConnectionLost;
    this.client.onMessageArrived = this.onMessageArrived;

    this.connect(connectionOptions)
  }

  connect() {
    this.client.connect({
      onSuccess: () => { this._connected = true; this.onConnect(); console.log("connected"); },
      onFailure: (err) => { console.log(err) }
    });
  }

  //
  onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    this.client.subscribe(this._mainTopic);

    // Test message
    // this.sendPayload("test", this._mainTopic)
  }

  // called when sending payload
  sendPayload(messageString, topic) {
    if (this._connected === false) {
      this.connect()
    }
    try {
      const message = new Message(messageString);
      message.destinationName = topic;
      this.client.send(message);
    } catch (err) {
      console.error(err)
    }
  }

  // called when client lost connection
  onConnectionLost = responseObject => {
    if (responseObject.errorCode !== 0) {
      console.log("onConnectionLost: " + responseObject.errorMessage);
      this._connected = false;
    }
  }

  // called when messages arrived
  onMessageArrived = message => {
    console.log("onMessageArrived: " + message.payloadString);
  }


  // called when subscribing topic(s)
  onSubscribe = () => {
    this.client.connect({
      onSuccess: () => {
        for (var i = 0; i < this._topics.length; i++) {
          this.client.subscribe(this._topics[i], this._options);
        }
      }
    }); // called when the client connects
  }

  // called when subscribing topic(s)
  onUnsubscribe = () => {
    for (var i = 0; i < this._topics.length; i++) {
      this.client.unsubscribe(this._topics[i], this._options);
    }
  }

  // called when disconnecting the client
  onDisconnect = () => {
    this._connected = false;
    this.client.disconnect();
  }

  // Disconnect
  disconnect = () => {
    this._connected = false;
    this.client.disconnect();
  }
}

class PahoMqttClient extends MqttClient {
  constructor(host, port, topics) {
    var connectionOptions = {}

    const _clientId = `client-${Math.floor((Math.random() * 100000) + 1)}`
    const client = new Client(host, Number(port), _clientId);

    super(client, connectionOptions, topics)
  }
}

class IotCoreMqttClient extends MqttClient {
  constructor(host, accessKeyId, secretAccessKey, sessionToken, topics) {
    const _clientId = `client-${Math.floor((Math.random() * 100000) + 1)}`

    const endpoint = SigV4Utils.createEndpoint(
      awsExports.aws_project_region,
      host,
      accessKeyId,
      secretAccessKey,
      sessionToken
    )
    const client = new Client(endpoint, _clientId);

    const connectionOptions = {
      useSSL: true,
      timeout: 3,
      mqttVersion: 4
    }
    super(client, connectionOptions, topics)
  }
}

class SigV4Utils {
  static _sign = (key, msg) => {
    var hash = CryptoJS.HmacSHA256(msg, key);
    return hash.toString(CryptoJS.enc.Hex);
  };

  static _sha256 = (msg) => {
    var hash = CryptoJS.SHA256(msg);
    return hash.toString(CryptoJS.enc.Hex);
  };

  static _getSignatureKey = (key, dateStamp, regionName, serviceName) => {
    var kDate = CryptoJS.HmacSHA256(dateStamp, 'AWS4' + key);
    var kRegion = CryptoJS.HmacSHA256(regionName, kDate);
    var kService = CryptoJS.HmacSHA256(serviceName, kRegion);
    var kSigning = CryptoJS.HmacSHA256('aws4_request', kService);
    return kSigning;
  };

  static createEndpoint = (regionName, awsIotEndpoint, accessKey, secretKey, sessionToken) => {
    // date & time
    const dt = (new Date()).toISOString().replace(/[^0-9]/g, "");
    const ymd = dt.slice(0, 8);
    const fdt = `${ymd}T${dt.slice(8, 14)}Z`

    var dateStamp = ymd
    var amzdate = fdt
    var service = 'iotdevicegateway';
    var region = regionName;
    var algorithm = 'AWS4-HMAC-SHA256';
    var method = 'GET';
    var canonicalUri = '/mqtt';
    var host = awsIotEndpoint;
    var credentialScope = dateStamp + '/' + region + '/' + service + '/aws4_request';
    var canonicalQuerystring = 'X-Amz-Algorithm=AWS4-HMAC-SHA256';
    canonicalQuerystring += '&X-Amz-Credential=' + encodeURIComponent(accessKey + '/' + credentialScope);
    canonicalQuerystring += '&X-Amz-Date=' + amzdate;
    canonicalQuerystring += '&X-Amz-SignedHeaders=host';
    var canonicalHeaders = 'host:' + host + '\n';
    var payloadHash = this._sha256('');
    var canonicalRequest = method + '\n' + canonicalUri + '\n' + canonicalQuerystring + '\n' + canonicalHeaders + '\nhost\n' + payloadHash;
    var stringToSign = algorithm + '\n' + amzdate + '\n' + credentialScope + '\n' + this._sha256(canonicalRequest);
    var signingKey = this._getSignatureKey(secretKey, dateStamp, region, service);
    var signature = this._sign(signingKey, stringToSign);
    canonicalQuerystring += '&X-Amz-Signature=' + signature;
    canonicalQuerystring += '&X-Amz-Security-Token=' + encodeURIComponent(sessionToken);
    return 'wss://' + host + canonicalUri + '?' + canonicalQuerystring;
  }
}

export { PahoMqttClient, IotCoreMqttClient }