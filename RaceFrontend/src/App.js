import React from 'react'

import './App.css';
import AppRouter from './web-components/router'
import { Authenticator } from '@aws-amplify/ui-react';

import { Amplify } from 'aws-amplify';

import awsExports from "./aws-exports";

if (awsExports.aws_appsync_graphqlEndpoint.startsWith('http://')){
  // awsExports.aws_appsync_authenticationType = 'API_KEY'
  awsExports.aws_appsync_graphqlEndpoint = 'http://localhost:3000/graphql'
}

Amplify.configure(awsExports);

function App() {
  return (
    <div className="App">
       <Authenticator.Provider>
           <AppRouter/>
       </Authenticator.Provider>
    </div>
  );
}

export default App;
