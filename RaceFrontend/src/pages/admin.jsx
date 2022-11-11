import React, { useEffect, useState, useRef } from 'react'
import { API, graphqlOperation, Auth } from 'aws-amplify'
import { Heading, Grid, useTheme, Button, SliderField } from '@aws-amplify/ui-react';

import { useNavigate } from "react-router-dom";

import * as customStatements from '../graphql/custom-statements'

import { CORE_OVERVIEW_ID, RACE_STATES, RACE_OPERATIONS, RACE_CONFIRMATION_MESSAGES, RACE_STATE_ICONS, CARS } from '../utils/constants'

import { MQTT_TOPICS } from '../utils/constants';

import { PahoMqttClient, IotCoreMqttClient } from '../utils/mqttClient'

import awsExports from "../aws-exports";

import * as queries from '../graphql/queries'

const {
  REACT_APP_MQTT_ENDPOINT_HOST_REMOTE,
  REACT_APP_MQTT_ENDPOINT_HOST_LOCAL,
  REACT_APP_MQTT_ENDPOINT_PORT
} = process.env

export default function Admin() {
  const [race, setRace] = useState()
  const [nrOfLaps, setNrOfLaps] = useState(30)
  const [secretPin, setSecretPin] = useState("")
  const [loading, setLoading] = useState(false)
  const [overview, setOverview] = useState()
  const [raceSubscription, setRaceSubscription] = useState()

  const raceSubscriptionRef = useRef(raceSubscription)
  const clientRef = useRef()

  const navigate = useNavigate();

  const loadingText = "Loading ..."

  useEffect(() => {
    checkPin()

    init()

    return () => {
      tearDownConnections()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const tearDownConnections = () => {
    if (raceSubscriptionRef.current) {
      raceSubscriptionRef.current.unsubscribe()
    }

    if (clientRef.current) {
      clientRef.current.disconnect()
    }
  }

  const checkPin = () => {
    const adminPin = prompt("Provide admin PIN")
    if (adminPin !== process.env.REACT_APP_ADMIN_PIN) { alert("Incorrect PIN"); navigate(`/`) }
    setSecretPin(adminPin)
  }

  const init = async () => {
    await initWsClient()
    const raceId = await setup()

    if (raceId) {
      const updateRaceSubscription = await API.graphql({
        query: customStatements.customOnUpdateRaceById,
        variables: { id: raceId }
      }).subscribe({
        next: ({ _, value }) => { console.log("Updated Race: ", value); fetchCurrentRace(value.data.onUpdateRaceById.id) },
        error: error => console.warn(error)
      });
      raceSubscriptionRef.current = updateRaceSubscription
      setRaceSubscription(updateRaceSubscription)

      return updateRaceSubscription
    }
    return null
  }

  const initWsClient = async () => {
    const isLocal = awsExports.aws_appsync_graphqlEndpoint.startsWith('http://')
    if (clientRef.current) { return }

    if (isLocal === false) {
      console.log("Remote Client")
      const { accessKeyId, secretAccessKey, sessionToken } = await Auth.currentCredentials()
      const client = new IotCoreMqttClient(
        REACT_APP_MQTT_ENDPOINT_HOST_REMOTE,
        accessKeyId,
        secretAccessKey,
        sessionToken,
        [MQTT_TOPICS.GAME_STATE_UPDATE]
      )
      clientRef.current = client
    } else {
      console.log("Local Client")
      const client = new PahoMqttClient(
        REACT_APP_MQTT_ENDPOINT_HOST_LOCAL,
        REACT_APP_MQTT_ENDPOINT_PORT,
        [MQTT_TOPICS.GAME_STATE_UPDATE]
      )
      clientRef.current = client
    }
  }

  const setup = async () => {
    const overview = await getOverview()
    setOverview(overview)

    if (overview && overview.currentRace !== null) {
      await fetchCurrentRace(overview.currentRace.id)
      return overview?.currentRace?.id
    }
    return null
  }

  const getOverview = async () => {
    var overview = null;
    try {
      const overviewData = await API.graphql(graphqlOperation(customStatements.customGetOverview, { id: CORE_OVERVIEW_ID }))
      overview = overviewData.data.getOverview || null
    } catch (error) {
      console.error("No overview found, likely that you need to initialise")
      console.log(error)
    }
    return overview
  }

  const fetchCurrentRace = async (raceId) => {
    setLoading(true)
    try {
      const raceData = await API.graphql(graphqlOperation(customStatements.customGetRace, { id: raceId }))
      const currentRace = raceData.data.getRace
      const carClaims = currentRace.currentRaceState === RACE_STATES.FORMATION_LAPS ? getFormationLapClaimsArray(currentRace) : getCarClaimsArray(currentRace)
      const updatedState = {
        raceId: currentRace.id,
        gameState: currentRace.currentRaceState,
        carClaims
      }
      clientRef.current.sendPayload(JSON.stringify(updatedState), MQTT_TOPICS.GAME_STATE_UPDATE)
      setRace(currentRace)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const getCarClaimsArray = (raceData) => {
    var array = []
    for (const player of raceData.players.items) {
      var object = {
        carId: parseInt(player.playerCarId),
        playerId: ""
      }
      if (player.claims.items.length > 0) {
        object.playerId = player.claims.items[0].id
      }
      array.push(object)
    }
    return array
  }

  const getFormationLapClaimsArray = (raceData) => {
    var array = []
    for (const player of raceData.players.items) {
      const carId = parseInt(player.playerCarId)
      array.push({
        carId,
        playerId: CARS[carId-1]?.claimable ? player.id : ""
      })
    }
    return array
  }

  const initialise = async () => {
    setLoading(true)
    try {
      await API.graphql(graphqlOperation(queries.raceOperations, {
        input: {
          operation: RACE_OPERATIONS.INITIALISE,
          secretPin,
          additionalParams: {
            nrOfLaps
          }
        }
      }))
    } catch (error) {
      console.error(error)
    }
    window.location.reload();
    setLoading(false)
  }

  const createNewRace = async () => {
    const operation = RACE_OPERATIONS.CREATE_NEW_RACE
    setLoading(true)
    // eslint-disable-next-line no-restricted-globals
    const confirmed = confirm(RACE_CONFIRMATION_MESSAGES[operation])
    if (confirmed === true) {
      try {
        await API.graphql(graphqlOperation(queries.raceOperations, {
          input: {
            operation: operation,
            secretPin,
            additionalParams: {
              nrOfLaps
            }
          }
        }))
        raceSubscriptionRef.current.unsubscribe()
        await init()
      } catch (error) {
        console.error(error)
      }
    }
    setLoading(false)
  }

  const { tokens } = useTheme();

  const raceIsOngoing = () => {
    const state = race?.currentRaceState
    return race && state !== RACE_STATES.CHECKERED_FLAG && state !== RACE_STATES.LOBBY && state !== RACE_STATES.ABORTED && state !== RACE_STATES.PRACTICE
  }

  const canChangeToThisActiveRaceState = (desiredState) => {
    const state = race?.currentRaceState
    return raceIsOngoing() && state !== RACE_STATES.LOBBY && state !== desiredState
  }

  const raceOperation = async (operation) => {
    setLoading(true)
    if (RACE_CONFIRMATION_MESSAGES[operation] !== undefined) {
      // eslint-disable-next-line no-restricted-globals
      const confirmed = confirm(RACE_CONFIRMATION_MESSAGES[operation])
      if (!confirmed) { setLoading(false); return }
    }
    try {
      await API.graphql(graphqlOperation(queries.raceOperations, {
        input: {
          operation: operation,
          secretPin,
          additionalParams: {
            raceId: race.id
          }
        }
      }))
    } catch (error) {
      console.error(error)
      setLoading(false)
    }
  }
  const actionButtons = () => {
    if (!overview) {
      return (
        <>
          <Heading level={3}>One-time initialisation .... </Heading>
          <Button
            variation='primary'
            isLoading={loading}
            loadingText={loadingText}
            onClick={initialise}
          >
            Initialise
          </Button>
        </>
      )
    }
    else {
      return (
        <>

          <Button
            variation='primary'
            disabled={raceIsOngoing() || race?.currentRaceState !== RACE_STATES.LOBBY}
            onClick={() => raceOperation(RACE_OPERATIONS.SET_PRACTICE)}
            isLoading={loading}
            loadingText={loadingText}
          >
            Set practice mode {RACE_STATE_ICONS[RACE_STATES.PRACTICE]}
          </Button>
          <Button
            variation='primary'
            disabled={raceIsOngoing() || race?.currentRaceState !== RACE_STATES.PRACTICE}
            onClick={() => raceOperation(RACE_OPERATIONS.SET_PENDING)}
            isLoading={loading}
            loadingText={loadingText}
          >
            Driver line-up {RACE_STATE_ICONS[RACE_STATES.PENDING]}
          </Button>
          <Button
            variation='primary'
            disabled={!canChangeToThisActiveRaceState(RACE_STATES.GREEN_FLAG)}
            onClick={() => raceOperation(RACE_OPERATIONS.TRIGGER_GREEN_FLAG)}
            isLoading={loading}
            loadingText={loadingText}
          >
            (Re)start race: {RACE_STATE_ICONS[RACE_STATES.GREEN_FLAG]}
          </Button>
          <Button
            variation='primary'
            disabled={!canChangeToThisActiveRaceState(RACE_STATES.YELLOW_FLAG)}
            onClick={() => raceOperation(RACE_OPERATIONS.TRIGGER_YELLOW_FLAG)}
            isLoading={loading}
            loadingText={loadingText}
          >
            Reduce speed: {RACE_STATE_ICONS[RACE_STATES.YELLOW_FLAG]}
          </Button>
          <Button
            variation='primary'
            disabled={!canChangeToThisActiveRaceState(RACE_STATES.RED_FLAG)}
            onClick={() => raceOperation(RACE_OPERATIONS.TRIGGER_RED_FLAG)}
            isLoading={loading}
            loadingText={loadingText}
          >
            Temporarily stop race {RACE_STATE_ICONS[RACE_STATES.RED_FLAG]}
          </Button>
          <Button
            variation='primary'
            disabled={!canChangeToThisActiveRaceState(RACE_STATES.CHECKERED_FLAG)}
            onClick={() => raceOperation(RACE_OPERATIONS.TRIGGER_CHECKERED_FLAG)}
            isLoading={loading}
            loadingText={loadingText}
          >
            Finish race {RACE_STATE_ICONS[RACE_STATES.CHECKERED_FLAG]}
          </Button>
          <Button
            variation={'primary'}
            isLoading={loading}
            loadingText={loadingText}
            onClick={createNewRace}
            disabled={raceIsOngoing() || (race && race.currentRaceState !== RACE_STATES.ABORTED && race.currentRaceState !== RACE_STATES.CHECKERED_FLAG)}
          >
            Create new race
          </Button>
          <Button
            variation=''
            disabled={!race || race.currentRaceState === RACE_STATES.ABORTED}
            isLoading={loading}
            loadingText={loadingText}
            onClick={() => raceOperation(RACE_OPERATIONS.ABORT_RACE)}
          >
            Abort race {RACE_STATE_ICONS[RACE_STATES.ABORTED]}
          </Button>
          <Button
            variation='primary'
            disabled={raceIsOngoing() || race?.currentRaceState !== RACE_STATES.LOBBY}
            onClick={() => raceOperation(RACE_OPERATIONS.TRIGGER_FORMATION_LAPS)}
            isLoading={loading}
            loadingText={loadingText}
          >
            Run formation lap(s)
          </Button>
          <SliderField
            label="Nr of Laps"
            max={150}
            size="large"
            value={nrOfLaps}
            onChange={setNrOfLaps}
            isDisabled={raceIsOngoing() || race?.currentRaceState === RACE_STATES.LOBBY}
          />
        </>
      )
    }
  }
  return (
    <>
      <Heading level={2} margin={'relative.xxs'}>Admin</Heading>
      {race &&
        <>
          <Heading level={4} margin={'relative.xxs'}>Current race id: {race?.id}</Heading>
          <Heading level={4} margin={'relative.xxs'}>Current race state: {race?.currentRaceState}</Heading>
        </>
      }
      <Grid
        templateColumns="1fr 1fr"
        // templateRows="10rem 10rem"
        templateRows={{ base: 'repeat(4, 5rem)' }}
        gap={tokens.space.small}
        autoColumns={true}
        margin={'relative.medium'}
      >
        {actionButtons()}
      </Grid>

    </>
  )
}