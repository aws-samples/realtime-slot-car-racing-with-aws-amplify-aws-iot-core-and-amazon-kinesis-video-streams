const { createProxyMiddleware } = require('http-proxy-middleware');
module.exports = (app) => {
  const gqlProxy = createProxyMiddleware('http://localhost:3000/graphql', {
    target: 'http://localhost:20002',
    changeOrigin: true,
    logLevel: 'debug' // optional
  })

  const wsProxy = createProxyMiddleware('http://localhost:3000/graphql/realtime', {
    target: 'ws://localhost:20002',
    pathRewrite: {
      '^/graphql/realtime': '/graphql'
    },
    changeOrigin: true,
    ws: true,
    logLevel: 'debug' // optional
  })

  app.use(gqlProxy)
  app.use(wsProxy)
};