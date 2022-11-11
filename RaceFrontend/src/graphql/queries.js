/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const raceOperations = /* GraphQL */ `
  query RaceOperations($input: raceOperationInput) {
    raceOperations(input: $input) {
      status
      message
      details
    }
  }
`;
export const getOverview = /* GraphQL */ `
  query GetOverview($id: ID!) {
    getOverview(id: $id) {
      id
      currentRace {
        id
        players {
          nextToken
        }
        lapTimes {
          nextToken
        }
        nrOfLaps
        currentRaceState
        finalStats {
          id
          raceId
          createdAt
          updatedAt
          finalRaceStatsFastestLapTimeId
          finalRaceStatsWinnerId
        }
        createdAt
        updatedAt
        overviewAllRacesId
        raceFinalStatsId
      }
      allRaces {
        items {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        nextToken
      }
      createdAt
      updatedAt
      overviewCurrentRaceId
    }
  }
`;
export const listOverviews = /* GraphQL */ `
  query ListOverviews(
    $filter: ModelOverviewFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listOverviews(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        currentRace {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        allRaces {
          nextToken
        }
        createdAt
        updatedAt
        overviewCurrentRaceId
      }
      nextToken
    }
  }
`;
export const getRace = /* GraphQL */ `
  query GetRace($id: ID!) {
    getRace(id: $id) {
      id
      players {
        items {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        nextToken
      }
      lapTimes {
        items {
          id
          raceId
          playerId
          timeInMilliSec
          type
          createdAt
          updatedAt
        }
        nextToken
      }
      nrOfLaps
      currentRaceState
      finalStats {
        id
        raceId
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        fastestLapTime {
          id
          raceId
          playerId
          timeInMilliSec
          type
          createdAt
          updatedAt
        }
        winner {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        createdAt
        updatedAt
        finalRaceStatsFastestLapTimeId
        finalRaceStatsWinnerId
      }
      createdAt
      updatedAt
      overviewAllRacesId
      raceFinalStatsId
    }
  }
`;
export const listRaces = /* GraphQL */ `
  query ListRaces(
    $filter: ModelRaceFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listRaces(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        players {
          nextToken
        }
        lapTimes {
          nextToken
        }
        nrOfLaps
        currentRaceState
        finalStats {
          id
          raceId
          createdAt
          updatedAt
          finalRaceStatsFastestLapTimeId
          finalRaceStatsWinnerId
        }
        createdAt
        updatedAt
        overviewAllRacesId
        raceFinalStatsId
      }
      nextToken
    }
  }
`;
export const getFinalRaceStats = /* GraphQL */ `
  query GetFinalRaceStats($id: ID!) {
    getFinalRaceStats(id: $id) {
      id
      raceId
      race {
        id
        players {
          nextToken
        }
        lapTimes {
          nextToken
        }
        nrOfLaps
        currentRaceState
        finalStats {
          id
          raceId
          createdAt
          updatedAt
          finalRaceStatsFastestLapTimeId
          finalRaceStatsWinnerId
        }
        createdAt
        updatedAt
        overviewAllRacesId
        raceFinalStatsId
      }
      fastestLapTime {
        id
        raceId
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        playerId
        player {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        timeInMilliSec
        type
        createdAt
        updatedAt
      }
      winner {
        id
        car {
          id
          color
          throttle
          fuelLevel
          tireWear
          speed
          requestLaneSwitch
          brakesOn
          createdAt
          updatedAt
        }
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        allLapTimes {
          nextToken
        }
        claims {
          nextToken
        }
        createdAt
        updatedAt
        racePlayersId
        playerCarId
      }
      createdAt
      updatedAt
      finalRaceStatsFastestLapTimeId
      finalRaceStatsWinnerId
    }
  }
`;
export const listFinalRaceStats = /* GraphQL */ `
  query ListFinalRaceStats(
    $filter: ModelFinalRaceStatsFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listFinalRaceStats(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        raceId
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        fastestLapTime {
          id
          raceId
          playerId
          timeInMilliSec
          type
          createdAt
          updatedAt
        }
        winner {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        createdAt
        updatedAt
        finalRaceStatsFastestLapTimeId
        finalRaceStatsWinnerId
      }
      nextToken
    }
  }
`;
export const raceStatsByRaceId = /* GraphQL */ `
  query RaceStatsByRaceId(
    $raceId: ID!
    $sortDirection: ModelSortDirection
    $filter: ModelFinalRaceStatsFilterInput
    $limit: Int
    $nextToken: String
  ) {
    raceStatsByRaceId(
      raceId: $raceId
      sortDirection: $sortDirection
      filter: $filter
      limit: $limit
      nextToken: $nextToken
    ) {
      items {
        id
        raceId
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        fastestLapTime {
          id
          raceId
          playerId
          timeInMilliSec
          type
          createdAt
          updatedAt
        }
        winner {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        createdAt
        updatedAt
        finalRaceStatsFastestLapTimeId
        finalRaceStatsWinnerId
      }
      nextToken
    }
  }
`;
export const getPlayer = /* GraphQL */ `
  query GetPlayer($id: ID!) {
    getPlayer(id: $id) {
      id
      car {
        id
        color
        throttle
        fuelLevel
        tireWear
        speed
        requestLaneSwitch
        brakesOn
        createdAt
        updatedAt
      }
      race {
        id
        players {
          nextToken
        }
        lapTimes {
          nextToken
        }
        nrOfLaps
        currentRaceState
        finalStats {
          id
          raceId
          createdAt
          updatedAt
          finalRaceStatsFastestLapTimeId
          finalRaceStatsWinnerId
        }
        createdAt
        updatedAt
        overviewAllRacesId
        raceFinalStatsId
      }
      allLapTimes {
        items {
          id
          raceId
          playerId
          timeInMilliSec
          type
          createdAt
          updatedAt
        }
        nextToken
      }
      claims {
        items {
          id
          uuid
          username
          createdAt
          updatedAt
          playerClaimsId
        }
        nextToken
      }
      createdAt
      updatedAt
      racePlayersId
      playerCarId
    }
  }
`;
export const listPlayers = /* GraphQL */ `
  query ListPlayers(
    $filter: ModelPlayerFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listPlayers(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        car {
          id
          color
          throttle
          fuelLevel
          tireWear
          speed
          requestLaneSwitch
          brakesOn
          createdAt
          updatedAt
        }
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        allLapTimes {
          nextToken
        }
        claims {
          nextToken
        }
        createdAt
        updatedAt
        racePlayersId
        playerCarId
      }
      nextToken
    }
  }
`;
export const getPlayerClaim = /* GraphQL */ `
  query GetPlayerClaim($id: ID!) {
    getPlayerClaim(id: $id) {
      id
      uuid
      username
      player {
        id
        car {
          id
          color
          throttle
          fuelLevel
          tireWear
          speed
          requestLaneSwitch
          brakesOn
          createdAt
          updatedAt
        }
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        allLapTimes {
          nextToken
        }
        claims {
          nextToken
        }
        createdAt
        updatedAt
        racePlayersId
        playerCarId
      }
      createdAt
      updatedAt
      playerClaimsId
    }
  }
`;
export const listPlayerClaims = /* GraphQL */ `
  query ListPlayerClaims(
    $filter: ModelPlayerClaimFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listPlayerClaims(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        uuid
        username
        player {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        createdAt
        updatedAt
        playerClaimsId
      }
      nextToken
    }
  }
`;
export const getCar = /* GraphQL */ `
  query GetCar($id: ID!) {
    getCar(id: $id) {
      id
      color
      throttle
      fuelLevel
      tireWear
      speed
      requestLaneSwitch
      brakesOn
      createdAt
      updatedAt
    }
  }
`;
export const listCars = /* GraphQL */ `
  query ListCars(
    $filter: ModelCarFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listCars(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        color
        throttle
        fuelLevel
        tireWear
        speed
        requestLaneSwitch
        brakesOn
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
export const getLapTime = /* GraphQL */ `
  query GetLapTime($id: ID!) {
    getLapTime(id: $id) {
      id
      raceId
      race {
        id
        players {
          nextToken
        }
        lapTimes {
          nextToken
        }
        nrOfLaps
        currentRaceState
        finalStats {
          id
          raceId
          createdAt
          updatedAt
          finalRaceStatsFastestLapTimeId
          finalRaceStatsWinnerId
        }
        createdAt
        updatedAt
        overviewAllRacesId
        raceFinalStatsId
      }
      playerId
      player {
        id
        car {
          id
          color
          throttle
          fuelLevel
          tireWear
          speed
          requestLaneSwitch
          brakesOn
          createdAt
          updatedAt
        }
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        allLapTimes {
          nextToken
        }
        claims {
          nextToken
        }
        createdAt
        updatedAt
        racePlayersId
        playerCarId
      }
      timeInMilliSec
      type
      createdAt
      updatedAt
    }
  }
`;
export const listLapTimes = /* GraphQL */ `
  query ListLapTimes(
    $filter: ModelLapTimeFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listLapTimes(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        raceId
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        playerId
        player {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        timeInMilliSec
        type
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
export const lapTimesByRaceId = /* GraphQL */ `
  query LapTimesByRaceId(
    $raceId: ID!
    $sortDirection: ModelSortDirection
    $filter: ModelLapTimeFilterInput
    $limit: Int
    $nextToken: String
  ) {
    lapTimesByRaceId(
      raceId: $raceId
      sortDirection: $sortDirection
      filter: $filter
      limit: $limit
      nextToken: $nextToken
    ) {
      items {
        id
        raceId
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        playerId
        player {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        timeInMilliSec
        type
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
export const lapTimesByPlayerId = /* GraphQL */ `
  query LapTimesByPlayerId(
    $playerId: ID!
    $sortDirection: ModelSortDirection
    $filter: ModelLapTimeFilterInput
    $limit: Int
    $nextToken: String
  ) {
    lapTimesByPlayerId(
      playerId: $playerId
      sortDirection: $sortDirection
      filter: $filter
      limit: $limit
      nextToken: $nextToken
    ) {
      items {
        id
        raceId
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        playerId
        player {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        timeInMilliSec
        type
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
export const lapTimesByTime = /* GraphQL */ `
  query LapTimesByTime(
    $type: String!
    $timeInMilliSec: ModelIntKeyConditionInput
    $sortDirection: ModelSortDirection
    $filter: ModelLapTimeFilterInput
    $limit: Int
    $nextToken: String
  ) {
    lapTimesByTime(
      type: $type
      timeInMilliSec: $timeInMilliSec
      sortDirection: $sortDirection
      filter: $filter
      limit: $limit
      nextToken: $nextToken
    ) {
      items {
        id
        raceId
        race {
          id
          nrOfLaps
          currentRaceState
          createdAt
          updatedAt
          overviewAllRacesId
          raceFinalStatsId
        }
        playerId
        player {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
        }
        timeInMilliSec
        type
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
