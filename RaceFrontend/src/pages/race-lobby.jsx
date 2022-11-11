import React, { useEffect, useState } from 'react'
import { API, graphqlOperation } from 'aws-amplify'
import { Heading, Grid, View, useTheme, Button, Flex, TextField } from '@aws-amplify/ui-react';

import { useNavigate } from "react-router-dom";

import * as customStatements from '../graphql/custom-statements'
import * as mutations from '../graphql/mutations'
import * as graphqlSubscriptionStatements from '../graphql/subscriptions'

import { CORE_OVERVIEW_ID, CARS, RACE_STATES } from '../utils/constants'
import { getOrCreateUserId } from "../utils/localStorageFunctions"
import { getPlayerByUUIDClaim, getClaim } from '../utils/helpers'

import Modal from '../web-components/modal';


export default function RaceLobby() {
  const [race, setRace] = useState()
  const [playerClaimedByUser, setPlayerClaimed] = useState()
  const [modalVisible, setModalVisible] = useState(false)
  const [username, setUsername] = useState("")
  const [claimingPlayerId, setClaimingPlayerId] = useState()

  const uuid = getOrCreateUserId()
  const navigate = useNavigate();

  var subscriptions = []

  useEffect(() => {
    setUp(uuid)
    return () => {
      for (const subscription of subscriptions) {
        subscription.unsubscribe()
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  const setUp = async (uuid) => {
    const raceId = await fetchCurrentRace(uuid)
    console.log(raceId)
    if (raceId !== null) {
      subscriptions = await createSubscriptions(uuid, fetchCurrentRace, raceId)
    }
    console.log(subscriptions)
  }

  const controllerRedirect = (raceId, carId) => {
    navigate(`/race/${raceId}/car/${carId}/controller/`)
  }

  const fetchCurrentRace = async (uuid) => {
    try {
      const overviewData = await API.graphql(graphqlOperation(customStatements.customGetOverview, { id: CORE_OVERVIEW_ID }))
      const currentRace = overviewData.data.getOverview.currentRace
      const claimedPlayer = getPlayerByUUIDClaim(currentRace.players.items, uuid)
      if (claimedPlayer !== undefined) {
        setPlayerClaimed(claimedPlayer)
        setUsername(claimedPlayer.claims.items[0].username)
      }

      if (currentRace.currentRaceState !== RACE_STATES.LOBBY && claimedPlayer) {
        controllerRedirect(currentRace.id, claimedPlayer.car.id)
      }
      setRace(currentRace)
      return currentRace.id
    } catch (err) {
      console.error(err)
      return null
    }
  }

  const createSubscriptions = async (uuid, updateFunction, raceId) => {
    const updateClaimSubscription = await API.graphql(graphqlOperation(customStatements.customOnUpdatePlayerClaim)).subscribe({
      next: ({ _, value }) => { console.log("Updated Claim: ", value); updateFunction(uuid) },
      error: error => console.warn(error)
    });

    const createClaimSubscription = await API.graphql(graphqlOperation(customStatements.customOnCreatePlayerClaim)).subscribe({
      next: ({ _, value }) => { console.log("New Claim: ", value); updateFunction(uuid) },
      error: error => console.warn(error)
    });

    const updateRaceSubscription = await API.graphql({
      query: graphqlSubscriptionStatements.onUpdateRaceById,
      variables: { id: raceId }

    }).subscribe({
      next: ({ _, value }) => { console.log("Updated Race: ", value); updateFunction(uuid) },
      error: error => console.warn(error)
    });
    return [
      updateClaimSubscription,
      createClaimSubscription,
      updateRaceSubscription
    ]
  }


  const { tokens } = useTheme();

  const CarBoxContent = (claimedInfo, available) => {
    if (!available) {
      return <Heading>Not available</Heading>
    }

    const toClaimText = playerClaimedByUser ? "" : <i>Click to claim</i>
    const text = claimedInfo ? `☑️ Claimed by: ${claimedInfo.username} ${claimedInfo.uuid === uuid ? "(you)" : ""}` : toClaimText
    return (
      <Heading level={5}>{text}</Heading>
    )
  }

  const setPlayerName = async () => {
    const claimingNew = playerClaimedByUser?.id === undefined
    const playerItemId = claimingNew ? claimingPlayerId : playerClaimedByUser.id
    const mutation = claimingNew ? mutations.createPlayerClaim : mutations.updatePlayerClaim

    var inputObject = {
      id: playerItemId,
      uuid,
      username,
      playerClaimsId: playerItemId
    }
    await API.graphql(graphqlOperation(mutation, { input: inputObject }))
    setModalVisible(false)
  }

  const handleBoxClick = async (playerItem, claimable) => {
    if (playerClaimedByUser !== undefined) {
      if (playerClaimedByUser.id === playerItem.id) {
        setModalVisible(true)
      }
    } else if (claimable === true) {
      setClaimingPlayerId(playerItem.id)
      setModalVisible(true)
    }
  }

  if (race?.currentRaceState && race.currentRaceState !== RACE_STATES.LOBBY) {
    return (
      <>
        <Heading level={2} margin={'relative.xxs'}>Race currently in progress ...</Heading>
      </>
    )
  }

  return (
    <>
      <Heading level={2} margin={'relative.xxs'}>Join race</Heading>
      <Grid
        templateColumns="1fr 1fr"
        templateRows={{ base: 'repeat(4, 3.5rem)' }}
        gap={tokens.space.small}
        autoColumns={true}
        margin={'relative.medium'}
      >
        {race &&
          CARS.map(item => {
            const playerItem = race.players.items.find(player => player.car.id === String(item.value))
            const claimedInfo = getClaim(playerItem)
            const available = item.claimable
            const claimed = claimedInfo !== null
            const claimable = available && !claimed
            const intensity = claimable ? 60 : 20
            return (
              <View
                key={playerItem.id}
                backgroundColor={tokens.colors[item.color][intensity]}
                borderRadius="6px"
                border="2px solid var(--amplify-colors-white)"
                id={playerItem.id}
                onClick={() => handleBoxClick(playerItem, claimable)}
              >
                <Heading level={5} style={{ color: 'white' }} >Car: {item.value} - {item.color}</Heading>
                {CarBoxContent(claimedInfo, available)}
              </View>
            )
          })
        }
      </Grid>
      <Modal title="Set username" handleClose={() => setModalVisible(false)} visible={modalVisible}>
        <Flex>
          <TextField
            label="Search"
            labelHidden={true}
            value={username}
            placeholder={"Type a username (max 10 characters)"}
            onChange={(event) => setUsername(event.target.value)}
            isRequired={true}
            maxLength={10}
            minLength={3}
            width={'100%'}
          />
          <Button onClick={() => setPlayerName()}>Save</Button>
        </Flex>
      </Modal>
    </>
  )
}