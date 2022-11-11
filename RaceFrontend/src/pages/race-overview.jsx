import React, { useEffect, useRef, useState } from 'react'
import {API, Auth, graphqlOperation} from 'aws-amplify'
import {Heading, Grid, Card, useTheme, Text, View, useAuthenticator, Button} from '@aws-amplify/ui-react';

import ChartRace from 'react-chart-race';

import WebRTCViewer from "../web-components/webrtc-viewer"
import * as customStatements from '../graphql/custom-statements'

import { CORE_OVERVIEW_ID, RACE_STATES, RACE_STATE_ICONS, RACER_ICON, LAPTIME_TYPE_STRING, LEADERBOARD_INDEX_ICONS } from '../utils/constants'
import {useNavigate} from "react-router-dom";

const KVSCHANNEL_REGION = "us-west-2"
const KVSCHANNEL_ARN = "arn:aws:kinesisvideo:us-west-2:606456525467:channel/live-track-webRTC/1664486452613"
const NR_OF_LATEST_LAPS_DISPLAYED = 5
const LEADERBOARD_NR_OF_PEOPLE = 3

export default function RaceOverview() {
  const [subscriptions, setSubscriptions] = useState([])
  const [claimSubscriptions, setClaimSubscriptions] = useState([])
  const [config, setConfig] = useState()

  const [race, setRace] = useState()
  const [players, setPlayers] = useState([])
  const [playerLaps, setPlayerLaps] = useState({})
  const [fastestLap, setFastestLap] = useState()
  const [latestLaps, setLatestLaps] = useState([])
  const [allTimeTop3, setAllTimeTop3] = useState([])

  const [loading, setLoading] = useState(false)

  const latestLapsRef = useRef(latestLaps)
  const allLaps = useRef([])
  const fastestLapRef = useRef(fastestLap)

  const subscriptionsRef = useRef(subscriptions)
  const claimSubscriptionRef = useRef(claimSubscriptions)

  const raceRef = useRef(race)

  const { route, signOut } = useAuthenticator((context) => [
    context.route,
    context.signOut,
  ]);
  const navigate = useNavigate();

  useEffect(() => {
    init()

    return () => {
      unsubscribeSubscriptions()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  const unsubscribeSubscriptions = () => {
    const subs = subscriptionsRef.current
    for (const sub of subs) {
      console.log("UNSUBSCRIBING: ", sub)
      sub.unsubscribe()
    }
  }


  const init = async () => {
    setLoading(true)
    await fetchCreds();
    await setRaceDataFromOverview()

    setLoading(false)
  }

  const fetchCreds = async () => {
    const { accessKeyId, secretAccessKey, sessionToken } = await Auth.currentUserCredentials()
    const config = {
      credentials: {
        accessKeyId: accessKeyId,
        secretAccessKey: secretAccessKey,
        sessionToken: sessionToken
      },
      channelARN: KVSCHANNEL_ARN,
      region: KVSCHANNEL_REGION,
      debug: true
    };
    setConfig(config)
  }

  const getRaceIdFromOverview = async () => {
    const overview = await getOverview()
    var raceId = null
    if (overview && overview.currentRace !== null) {
      raceId = overview?.currentRace?.id
      createSubscriptions(raceId)
    }
    return raceId
  }

  const fetchInitialLapTimes = async () => {
    const lapTimes = await API.graphql(graphqlOperation(customStatements.customLapTimesByRaceId, {
      raceId: raceRef.current.id,
      limit: 1000
    }))

    const allTimeFastest = await API.graphql(graphqlOperation(customStatements.customLapTimesByTime, {
      type: LAPTIME_TYPE_STRING,
      limit: LEADERBOARD_NR_OF_PEOPLE,
      sortDirection: "ASC"
    }))

    const lapTimeItems = lapTimes.data.lapTimesByRaceId.items
    const latestLaps = lapTimeItems.sort(function (a, b) {
      return new Date(b.createdAt) - new Date(a.createdAt);
    }).slice(0, NR_OF_LATEST_LAPS_DISPLAYED);

    if (lapTimeItems.length > 0) {
      const fastestLap = lapTimeItems.reduce(function (prev, current) {
        return (prev.timeInMilliSec < current.timeInMilliSec) ? prev : current
      })
      fastestLapRef.current = fastestLap
      setFastestLap(fastestLap)
    }
    latestLapsRef.current = latestLaps
    allLaps.current = lapTimeItems

    setLatestLaps(latestLaps)
    setAllTimeTop3(allTimeFastest.data.lapTimesByTime.items)

    lapsCompletedPerPlayer(lapTimeItems)
  }

  const setRaceDataFromOverview = async () => {
    const raceId = await getRaceIdFromOverview()
    await fetchCurrentRaceAndLapTimes(raceId)
  }

  const createClaimSubscriptions = async (raceId) => {
    unsubscribeClaimsSubscriptions()

    const updateClaimSubscription = await API.graphql(graphqlOperation(customStatements.customOnUpdatePlayerClaim)).subscribe({
      next: ({ _, value }) => { console.log("Updated Claim: ", value); fetchCurrentRaceAndLapTimes(raceId) },
      error: error => console.warn(error)
    });

    const createClaimSubscription = await API.graphql(graphqlOperation(customStatements.customOnCreatePlayerClaim)).subscribe({
      next: ({ _, value }) => { console.log("New Claim: ", value); fetchCurrentRaceAndLapTimes(raceId) },
      error: error => console.warn(error)
    });

    const subs = [
      updateClaimSubscription,
      createClaimSubscription,
    ]

    setClaimSubscriptions(subs)
    claimSubscriptionRef.current = subs

  }

  const unsubscribeClaimsSubscriptions = async () => {
    const subs = claimSubscriptionRef.current
    for (const sub of subs) {
      console.log("UNSUBSCRIBING: ", sub)
      sub.unsubscribe()
    }
  }

  const createSubscriptions = async (raceId) => {
    // Clean up any pre-existing subscriptions
    unsubscribeSubscriptions()

    const updateRaceSubscription = await API.graphql({
      query: customStatements.customOnUpdateRaceById,
      variables: { id: raceId }
    }).subscribe({
      next: ({ _, value }) => {
        fetchCurrentRaceAndLapTimes(raceId)
      },
      error: error => console.warn(error)
    });

    const updateOverviewSubscription = await API.graphql({
      query: customStatements.customOnUpdateOverview
    }).subscribe({
      next: ({ _, value }) => {
        console.log("Updated Overview: ", value);
        setRaceDataFromOverview()
      },
      error: error => console.warn(error)
    });

    const updateOnIncomingLaptime = (lapTime) => {
      var currentLaps = latestLapsRef.current
      currentLaps.unshift(lapTime)
      if (currentLaps.length > NR_OF_LATEST_LAPS_DISPLAYED) {
        currentLaps.pop()
      }

      const newAllLaps = [...allLaps.current, lapTime]
      lapsCompletedPerPlayer(newAllLaps)
      allLaps.current = newAllLaps

      latestLapsRef.current = currentLaps

      if (fastestLapRef.current && lapTime.timeInMilliSec < fastestLapRef.current.timeInMilliSec) {
        fastestLapRef.current = lapTime
        setFastestLap(lapTime)
      }

      setLatestLaps([...currentLaps])
    }

    const lapTimeSubscription = await API.graphql({
      query: customStatements.customOnCreateLapTime
    }).subscribe({
      next: ({ _, value }) => {
        console.log("New LapTime: ", value);
        updateOnIncomingLaptime(value.data.onCreateLapTime)
        //fetchLapTimes()
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

  const lapsCompletedPerPlayer = (lapTimes) => {
    const currRaceId = raceRef.current.id
    const currRacePlayers = raceRef.current.players.items

    const playerLapsObject = {}
    for (const player of currRacePlayers) {
      const lapsOfPlayer = lapTimes.filter(item => item.playerId === player.id && currRaceId === item.raceId)
      playerLapsObject[player.id] = lapsOfPlayer.length
    }
    setPlayerLaps(playerLapsObject)
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

  const fetchCurrentRaceAndLapTimes = async (raceId) => {
    try {
      const raceData = await API.graphql(graphqlOperation(customStatements.customGetRace, { id: raceId }))
      const currentRace = raceData.data.getRace

      if (currentRace.currentRaceState === RACE_STATES.LOBBY && claimSubscriptionRef.current.length === 0) {
        await createClaimSubscriptions(currentRace.id)
      }

      if (currentRace.currentRaceState !== RACE_STATES.LOBBY && claimSubscriptionRef.current.length > 0) {
        unsubscribeClaimsSubscriptions()
      }

      const activePlayers = currentRace.players.items.filter(item => item.claims.items[0]?.username !== undefined)

      setRace(currentRace)
      setPlayers(activePlayers)

      raceRef.current = currentRace

      await fetchInitialLapTimes()
    } catch (err) {
      console.error(err)
    }
  }

  const { tokens } = useTheme();

  const getChartData = (players, playerLaps) => {
    var objects = []
    for (const player of players) {
      objects.push({
        id: player.id,
        title: `${player.claims.items[0]?.username}`,
        value: playerLaps[player.id] || 0,
        color: `${player.car.color}`
      })
    }
    return objects
  }
  const chartData = getChartData(players, playerLaps)

  const getMaxLaps = () => {
    var max = 0
    for (const playerLap of Object.values(playerLaps)) {
      if (playerLap > max) {
        max = playerLap
      }
    }
    return max
  }

  if (race === null || loading ) {
    return (
      <>
      <Heading level={3}>Awaiting race information ... </Heading>
      </>
      )
    } else if ( route !== 'authenticated' ) {
      return (
          <>
            <Heading level={3}>You must be authenticated to view this page. </Heading>
            <Button onClick={() => navigate('/login')}>Login</Button>
          </>
      )
    }else {
      return (
        <Grid
        columnGap="0.5rem"
        rowGap="0.5rem"
        templateColumns="1fr 1fr 1fr 1fr 1fr 1fr"
        templateRows="1fr 60rem 11rem"
        gap={tokens.space.small}
        autoColumns={true}
        // margin={'relative.medium'}
        >
        <Card
        columnStart="1"
        columnEnd="4"
        backgroundColor={tokens.colors.blue[10]}
        border="3px solid var(--amplify-colors-white)"
        display={"inline-block"}
        alignItems={"center"}
        >
        <Heading level={2} fontSize='7rem' margin={'relative.xxs'}>Lap: {getMaxLaps()} / {race?.nrOfLaps}</Heading>
        </Card>
        <Card
        columnStart="4"
        columnEnd="-1"
        backgroundColor={tokens.colors.blue[10]}
        border="3px solid var(--amplify-colors-white)"
        display={"inline-block"}
        alignItems={"center"}
        >
        {
          race &&
          <>
          <Heading level={2} fontSize='6rem' margin={'relative.xxs'}>Race status: {RACE_STATE_ICONS[race?.currentRaceState]}</Heading>
          <Heading level={4} margin={'relative.xxs'}>Current race id: {race?.id}</Heading>
          </>
        }
        </Card>
        <Card
        columnStart="1"
        columnEnd="2"
        color={tokens.colors.white}
        border="3px solid var(--amplify-colors-white)"
        backgroundColor={tokens.colors.blue[10]}
        display={"inline"}
        alignItems={"center"}
        >
        <Heading level={3} margin={'relative.xxs'}>Leaderboard (# of laps): </Heading>
        {
          chartData.length > 0 &&
          <ChartRace
          key={race.id}
          data={chartData}
          backgroundColor='#FFFFF'
          width={'450'}
          padding={20}
          itemHeight={120}
          gap={20}
          titleStyle={{ marginTop: '0rem', textAlign: 'left', fontSize: '1.5rem', color: '#FFF', width: '15rem' }}
          valueStyle={{ fontSize: '3.5rem', color: '#FFF' }}
          />
        }
        </Card>
        <View
        columnStart="2"
        columnEnd="6"
        border="3px solid var(--amplify-colors-white)"
        backgroundColor={tokens.colors.blue[10]}
        display={"inline"}
        alignItems={"center"}
        >
        <Heading level={2} fontSize={"4em"}>📹 Live stream:</Heading>
        {/* <ReactPlayer url={TEST_STREAM_URL} playing muted controls={true} width='100%' height='90%' /> */}
        {config && <WebRTCViewer configProps={config}/>}
        </View>
        <Card
        columnStart="6"
        columnEnd="-1"
        color={tokens.colors.white}
        border="3px solid var(--amplify-colors-white)"
        backgroundColor={tokens.colors.blue[10]}
        display={"inline"}
        alignItems={"center"}
        >
        <Heading level={3} margin={'relative.xxs'}>Latest laps: </Heading>
        {
          latestLaps.map(item => {
            return (
              <Card
              border="3px solid var(--amplify-colors-white)"
              backgroundColor={tokens.colors[item.player.car.color][60]}
              margin={'1rem'}
              >
              <Text fontSize={"2.5em"}>
              {`${item.player.claims.items[0]?.username || "unnamed"}`}
              </Text>
              <Text fontSize={"2.5em"}>
              {`${item.timeInMilliSec}ms`}
              </Text>
              </Card>
              )
            })
          }
          </Card>
          <Card
          columnStart="1"
          columnEnd="4"
          border="3px solid var(--amplify-colors-white)"
          backgroundColor={tokens.colors.blue[10]}
          display={"inline"}
          alignItems={"center"}
          >
          <Heading level={2} fontSize='3rem'>🏆 All-time laptimes top 3: 🏆</Heading>
          <Text fontSize={"2.5em"}>
          {
            allTimeTop3.map((item, index) => {
              return `${LEADERBOARD_INDEX_ICONS[index]} ${item.player.claims.items[0]?.username || "unnamed"} (${item.timeInMilliSec}ms)  `
            })
          }
          </Text>
          </Card>
          <Card
              columnStart="4"
              columnEnd="-1"
              border="3px solid var(--amplify-colors-white)"
              backgroundColor={tokens.colors.blue[10]}
              display={"inline"}
              alignItems={"center"}
          >
            <Heading level={2} fontSize='3rem'>✨ Current race - fastest lap: ✨</Heading>
            {fastestLap &&
                <Text fontSize={"3em"}>
                  {`${RACER_ICON} ${fastestLap.player.claims.items[0]?.username || "unnamed"} - ${fastestLap.timeInMilliSec}ms`}
                </Text>
            }
          </Card>
        </Grid>
          )
        }

      }