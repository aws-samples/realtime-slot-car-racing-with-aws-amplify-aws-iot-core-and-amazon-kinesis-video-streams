import React from 'react';

import {
  BrowserRouter as Router,
  Route,
  Routes,
} from 'react-router-dom'

import Home from '../pages/home'
import Admin from '../pages/admin'
import Race from '../pages/race'
import RaceLobby from '../pages/race-lobby';
import RaceController from '../pages/race-controller';
import RaceOverview from '../pages/race-overview';
import {Login} from "./login";
import {RequireAuth} from "./require-auth";


export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home/>}/>
        <Route exact path="/login" element={<Login/>}/>
        <Route path="/admin" element={<Admin/>}/>
        <Route path="/race-lobby" element={<RaceLobby/>}/>
        <Route
            path="/race-overview"
            element={
              <RequireAuth>
                <RaceOverview />
              </RequireAuth>
            }
        />
        <Route path="/race/:id" element={<Race/>}/>
        <Route path="/race/:raceId/car/:carId/controller" element={<RaceController/>}/>
      </Routes>
    </Router>
  )
}
