#!/usr/bin/env node
console.log('Starting healthcheck...');
const http = require("http");

const options = {
    host : process.env.HOSTNAME || '0.0.0.0',
    port : process.env.PORT || 3000,
    timeout : 2000
};

console.log(`Checking ${options.host}:${options.port}...`)

const request = http.request(options, (res) => {
    console.log(`STATUS: ${res.statusCode}`);
    if (res.statusCode == 200) {
        process.exit(0);
    }
    else {
        process.exit(1);
    }
});

request.on('error', function(err) {
    console.log('ERROR');
    process.exit(1);
});

request.end();