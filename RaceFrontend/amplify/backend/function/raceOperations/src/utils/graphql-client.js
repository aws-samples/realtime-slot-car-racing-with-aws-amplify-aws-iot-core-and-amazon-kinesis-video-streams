const AWS = require('aws-sdk')
const AWSAppSyncClient = require('aws-appsync').default;
require('cross-fetch/polyfill');

var credentials = AWS.config.credentials
if (process.env.API_RACER_GRAPHQLAPIENDPOINTOUTPUT.startsWith('http://')){
    credentials = {
        "accessKeyId": "ASIAVJKIAM-AuthRole",
        "secretAccessKey": "fake"
    }
}

exports.appsync = new AWSAppSyncClient({
	url: process.env.API_RACER_GRAPHQLAPIENDPOINTOUTPUT,
	region: process.env.REGION,
	auth: {
		type: 'AWS_IAM',
		credentials,
	},
	disableOffline: true,
});
