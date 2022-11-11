import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import App from './App'
import reportWebVitals from './reportWebVitals'

import '@aws-amplify/ui-react/styles.css'
import { ThemeProvider, defaultDarkModeOverride } from '@aws-amplify/ui-react'

const root = ReactDOM.createRoot(document.getElementById('root'))
const theme = {
  name: 'my-theme',
  overrides: [defaultDarkModeOverride],
};


root.render(
  // <React.StrictMode>
    <ThemeProvider theme={theme} colorMode={'dark'}>
      <App />
    </ThemeProvider>
  // </React.StrictMode>
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
