import React, { useState, useEffect, useRef } from 'react'

import _ from 'lodash';

import { useParams, useNavigate } from 'react-router-dom'
import { Button, Heading, Grid, View, useTheme, SliderField, Text } from '@aws-amplify/ui-react'
import { Helmet } from 'react-helmet';

import { API, graphqlOperation, Auth } from 'aws-amplify'

import { CONTROLLER_VISIBLE_STATES, DRIVING_RACE_STATES, MQTT_TOPICS, RACE_STATE_ICONS } from '../utils/constants';

import { PahoMqttClient, IotCoreMqttClient } from '../utils/mqttClient'

import { getOrCreateUserId } from "../utils/localStorageFunctions"
import { getPlayerByUUIDClaim } from '../utils/helpers'

import awsExports from "../aws-exports";

import * as customStatements from '../graphql/custom-statements'

const {
  REACT_APP_MQTT_ENDPOINT_HOST_REMOTE,
  REACT_APP_MQTT_ENDPOINT_HOST_LOCAL,
  REACT_APP_MQTT_ENDPOINT_PORT
} = process.env

export default function RaceController() {
  const { carId, raceId } = useParams()

  const { tokens } = useTheme();
  const [throttle, setThrottle] = useState(0)
  const [laneSwitch, setRequestLaneSwitch] = useState(false)
  const [brakesOn, setRequestBrakes] = useState(false)
  const [client, setClient] = useState()
  const [race, setRace] = useState()
  const [player, setPlayer] = useState()
  const [subscriptions, setSubscriptions] = useState([])
  const [allLaps, setAllLaps] = useState([])
  const [latestLap, setLatestLap] = useState()
  const [fastestLap, setFastestLap] = useState()
  const [drivingState, setDrivingState] = useState(false)

  // The slider component doesn't update the label when setting the Throttle to 0
  // We update this key value to 'force' a re-render when a race is stopped.
  const [throttleKeyForForceUpdate, setThrottleKeyForForceUpdate] = useState(Math.random())

  const previousUpdateObject = useRef({})

  const clientRef = useRef(client) // Required for the eventListener to get the updated client
  const throttleRef = useRef(throttle)
  const laneSwitchRef = useRef(laneSwitch)
  const requestBrakesRef = useRef(brakesOn)
  const playerRef = useRef(player)
  const raceRef = useRef(race)
  const subscriptionsRef = useRef(subscriptions)

  const navigate = useNavigate();

  useEffect(() => {
    initWsClient()
    fetchCurrentRaceAndLapTimes()
    createSubscriptions()

    window.addEventListener('touchend', releaseButtons)

    return () => {
      unsubscribeSubscriptions()
      window.removeEventListener('touchend', releaseButtons)
      clientRef.current.disconnect()
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  const initWsClient = async () => {
    const isLocal = awsExports.aws_appsync_graphqlEndpoint.startsWith('http://')
    let client;
    if (isLocal === false) {
      console.log("Remote Client")
      const { accessKeyId, secretAccessKey, sessionToken } = await Auth.currentCredentials()
      client = new IotCoreMqttClient(
        REACT_APP_MQTT_ENDPOINT_HOST_REMOTE,
        accessKeyId,
        secretAccessKey,
        sessionToken,
        [MQTT_TOPICS.CAR_CONTROL_UPDATE]
      )
    } else {
      console.log("Local Client")
      client = new PahoMqttClient(
        REACT_APP_MQTT_ENDPOINT_HOST_LOCAL,
        REACT_APP_MQTT_ENDPOINT_PORT,
        [MQTT_TOPICS.CAR_CONTROL_UPDATE]
      )
    }
    clientRef.current = client
    setClient(client)
  }

  const unsubscribeSubscriptions = async () => {
    const subs = subscriptionsRef.current
    for (const sub of subs) {
      console.log("UNSUBSCRIBING: ", sub)
      sub.unsubscribe()
    }
  }

  const handleUnstartedRace = () => {
    const race = raceRef.current
    if (!CONTROLLER_VISIBLE_STATES.includes(race.currentRaceState)){
      setTimeout(() => { navigate("/"); }, 2000);
    }
  }

  const createSubscriptions = async () => {
    // Clean up any pre-existing subscriptions
    unsubscribeSubscriptions()

    const updateRaceSubscription = await API.graphql({
      query: customStatements.customOnUpdateRaceById,
      variables: { id: raceId }
    }).subscribe({
      next: ({ _, value }) => {
        fetchCurrentRaceAndLapTimes()
      },
      error: error => console.warn(error)
    });

    const updateOverviewSubscription = client.graphql({
      query: customStatements.customOnUpdateOverview
    }).subscribe({
      next: ({ _, value }) => {
        console.log("Updated Overview: ", value);

      },
      error: error => console.warn(error)
    });

    const lapTimeSubscription = client.graphql({
      query: customStatements.customOnCreateLapTime
    }).subscribe({
      next: ({ _, value }) => {
        console.log("New LapTime: ", value);
        fetchLapTimes()
      },
      error: error => console.warn(error)
    });

    const subs = [
      updateRaceSubscription,
      updateOverviewSubscription,
      lapTimeSubscription
    ]

    setSubscriptions(subs)
    subscriptionsRef.current = subs
  }

  const fetchCurrentRaceAndLapTimes = async () => {
    try {
      const race = await API.graphql(graphqlOperation(customStatements.customGetRace, { id: raceId }))
      const playerUUID = getOrCreateUserId()
      const player = getPlayerByUUIDClaim(race.data.getRace.players.items, playerUUID)

      playerRef.current = player

      setPlayer(player)
      setRace(race.data.getRace)

      const drivingState = DRIVING_RACE_STATES.includes(race.data.getRace.currentRaceState)

      if (!drivingState) {
        updateThrottle(0)
        setThrottleKeyForForceUpdate(Math.random())
      }

      setDrivingState(drivingState)

      raceRef.current = race.data.getRace
      handleUnstartedRace()
      await fetchLapTimes()
    } catch (err) {
      console.error(err)
    }
  }

  const fetchLapTimes = async () => {
    const lapTimes = await client.graphql({
      query: customStatements.customLapTimesByPlayerId,
      variables: {
        playerId: playerRef.current.id,
        limit: 1000
      }
    })

    const lapTimeItems = lapTimes.data.lapTimesByPlayerId.items

    if (lapTimeItems.length > 0) {
      const fastestLap = lapTimeItems.reduce(function (prev, current) {
        return (prev.timeInMilliSec < current.timeInMilliSec) ? prev : current
      })
      const latestLap = lapTimeItems.reduce(function (prev, current) {
        return (prev.createdAt > current.createdAt) ? prev : current
      })
      setAllLaps(lapTimeItems)
      setFastestLap(fastestLap)
      setLatestLap(latestLap)
    }
  }

  const releaseButtons = () => {
    var updateObject = getUpdateBaseObject()

    updateObject.laneChangeReq = false
    updateObject.brakesOnReq = false

    laneSwitchRef.current = false
    requestBrakesRef.current = false

    sendCarUpdateObjectIfUpdated(updateObject)
    setRequestBrakes(false)
    setRequestLaneSwitch(false)
  }

  const getUpdateBaseObject = () => {
    // Base object initialiser
    return {
      raceId,
      carId,
      playerId: playerRef.current.id,
      throttle: throttleRef.current,
      laneChangeReq: laneSwitchRef.current,
      brakesOnReq: requestBrakesRef.current
    }
  }

  const sendCarUpdateObjectIfUpdated = (updateObject) => {
    const client = clientRef.current
    if (!_.isEqual(updateObject, previousUpdateObject.current)) {
      client.sendPayload(JSON.stringify(updateObject), MQTT_TOPICS.CAR_CONTROL_UPDATE)
      previousUpdateObject.current = updateObject
    }
  }

  const updateThrottle = (value) => {
    const updateObject = getUpdateBaseObject()
    updateObject.throttle = value

    throttleRef.current = value

    sendCarUpdateObjectIfUpdated(updateObject)
    setThrottle(value)
  }

  const requestLaneSwitch = () => {
    const updateObject = getUpdateBaseObject()
    updateObject.laneChangeReq = true

    laneSwitchRef.current = true

    sendCarUpdateObjectIfUpdated(updateObject)
    setRequestLaneSwitch(true)
  }


  const requestBrakes = () => {
    const updateObject = getUpdateBaseObject()
    updateObject.brakesOnReq = true

    requestBrakesRef.current = true
    sendCarUpdateObjectIfUpdated(updateObject)

    setRequestBrakes(true)
  }

  const matchingCarId = player?.playerCarId === carId

  const controllerVisible = matchingCarId && CONTROLLER_VISIBLE_STATES.includes(race.currentRaceState)

  return (
    <>
      <Helmet >
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
      </Helmet>
      <Heading level={3} margin={'relative.xxs'}>Race controller</Heading>
      <View as="div" height={'-webkit-fill-available'} justifyContent={'center'}>
        {
          (!controllerVisible) && <Heading level={4}>You've got the wrong car page or the race hasn't started yet. Redirecting back ... </Heading>
        }
        {
          controllerVisible && <Grid
            templateColumns="1fr 1fr"
            templateRows="6rem 6rem"
            gap={tokens.space.small}
            style={{ transform: 'translateY(15%)' }}
          >
            <View columnSpan={2} backgroundColor={tokens.colors.orange[60]} style={{ display: 'flex', alignItems: 'left' }}>
              <View textAlign="left" style={{ width: '-webkit-fill-available' }}>
                <p style={{ margin: '1px', color: 'white' }}>Nickname: {player.claims.items[0].username}</p>
                <p style={{ margin: '1px', color: tokens.colors[player.car.color][80] }}>{player.car.color} car</p>
              </View>
              <View columnSpan={2} textAlign="center" style={{ width: '-webkit-fill-available' }}>
                <Heading style={{marginBottom: '10px'}} level={4}>Laps: {allLaps.length}/{race.nrOfLaps}</Heading>
                <Text style={{ color: 'white' }}>Latest lap: {latestLap && `${latestLap?.timeInMilliSec}ms`}</Text>
                <Text style={{ color: 'white' }}>Fastest lap: {fastestLap && `${fastestLap?.timeInMilliSec}ms`}</Text>
              </View>
              <View columnSpan={2} textAlign="center" style={{ width: '-webkit-fill-available' }}>
                <Heading level={5}>Race info: </Heading>
                <p style={{ color: 'white' }}>State: {RACE_STATE_ICONS[race.currentRaceState]}</p>
              </View>
            </View>
            <View
              rowSpan={1}
              backgroundColor={tokens.colors.orange[60]}
              justifyContent={'center'}
              borderRadius={tokens.radii.large}
              style={{ display: 'flex', alignItems: 'center' }}
            >
              <Button
                variation="primary"
                size='large'
                backgroundColor={tokens.colors[laneSwitch ? 'green' : 'blue'][80]}
                onTouchStart={() => requestLaneSwitch()}
                margin={tokens.space.small}
              >
                Switch lane
              </Button>
              <Button
                variation="primary"
                size='large'
                backgroundColor={tokens.colors[brakesOn ? 'green' : 'blue'][80]}
                onTouchStart={() => requestBrakes()}
                margin={tokens.space.small}
              >
                Brake
              </Button>
            </View>
            <View rowSpan={1} backgroundColor={tokens.colors.orange[60]} borderRadius={tokens.radii.large}>
              <View style={{ margin: '1em' }}>
                <SliderField
                  key={throttleKeyForForceUpdate}
                  label="Throttle"
                  max={100}
                  step={10}
                  value={throttle}
                  onChange={updateThrottle}
                  size={'large'}
                  disabled={!drivingState}
                />
              </View>
            </View>
          </Grid>
        }
      </View>
    </>
  )
}