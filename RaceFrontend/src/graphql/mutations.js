/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createOverview = /* GraphQL */ `
  mutation CreateOverview(
    $input: CreateOverviewInput!
    $condition: ModelOverviewConditionInput
  ) {
    createOverview(input: $input, condition: $condition) {
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
export const updateOverview = /* GraphQL */ `
  mutation UpdateOverview(
    $input: UpdateOverviewInput!
    $condition: ModelOverviewConditionInput
  ) {
    updateOverview(input: $input, condition: $condition) {
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
export const deleteOverview = /* GraphQL */ `
  mutation DeleteOverview(
    $input: DeleteOverviewInput!
    $condition: ModelOverviewConditionInput
  ) {
    deleteOverview(input: $input, condition: $condition) {
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
export const createRace = /* GraphQL */ `
  mutation CreateRace(
    $input: CreateRaceInput!
    $condition: ModelRaceConditionInput
  ) {
    createRace(input: $input, condition: $condition) {
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
export const updateRace = /* GraphQL */ `
  mutation UpdateRace(
    $input: UpdateRaceInput!
    $condition: ModelRaceConditionInput
  ) {
    updateRace(input: $input, condition: $condition) {
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
export const deleteRace = /* GraphQL */ `
  mutation DeleteRace(
    $input: DeleteRaceInput!
    $condition: ModelRaceConditionInput
  ) {
    deleteRace(input: $input, condition: $condition) {
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
export const createFinalRaceStats = /* GraphQL */ `
  mutation CreateFinalRaceStats(
    $input: CreateFinalRaceStatsInput!
    $condition: ModelFinalRaceStatsConditionInput
  ) {
    createFinalRaceStats(input: $input, condition: $condition) {
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
export const updateFinalRaceStats = /* GraphQL */ `
  mutation UpdateFinalRaceStats(
    $input: UpdateFinalRaceStatsInput!
    $condition: ModelFinalRaceStatsConditionInput
  ) {
    updateFinalRaceStats(input: $input, condition: $condition) {
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
export const deleteFinalRaceStats = /* GraphQL */ `
  mutation DeleteFinalRaceStats(
    $input: DeleteFinalRaceStatsInput!
    $condition: ModelFinalRaceStatsConditionInput
  ) {
    deleteFinalRaceStats(input: $input, condition: $condition) {
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
export const createPlayer = /* GraphQL */ `
  mutation CreatePlayer(
    $input: CreatePlayerInput!
    $condition: ModelPlayerConditionInput
  ) {
    createPlayer(input: $input, condition: $condition) {
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
export const updatePlayer = /* GraphQL */ `
  mutation UpdatePlayer(
    $input: UpdatePlayerInput!
    $condition: ModelPlayerConditionInput
  ) {
    updatePlayer(input: $input, condition: $condition) {
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
export const deletePlayer = /* GraphQL */ `
  mutation DeletePlayer(
    $input: DeletePlayerInput!
    $condition: ModelPlayerConditionInput
  ) {
    deletePlayer(input: $input, condition: $condition) {
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
export const createPlayerClaim = /* GraphQL */ `
  mutation CreatePlayerClaim(
    $input: CreatePlayerClaimInput!
    $condition: ModelPlayerClaimConditionInput
  ) {
    createPlayerClaim(input: $input, condition: $condition) {
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
export const updatePlayerClaim = /* GraphQL */ `
  mutation UpdatePlayerClaim(
    $input: UpdatePlayerClaimInput!
    $condition: ModelPlayerClaimConditionInput
  ) {
    updatePlayerClaim(input: $input, condition: $condition) {
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
export const deletePlayerClaim = /* GraphQL */ `
  mutation DeletePlayerClaim(
    $input: DeletePlayerClaimInput!
    $condition: ModelPlayerClaimConditionInput
  ) {
    deletePlayerClaim(input: $input, condition: $condition) {
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
export const createCar = /* GraphQL */ `
  mutation CreateCar(
    $input: CreateCarInput!
    $condition: ModelCarConditionInput
  ) {
    createCar(input: $input, condition: $condition) {
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
export const updateCar = /* GraphQL */ `
  mutation UpdateCar(
    $input: UpdateCarInput!
    $condition: ModelCarConditionInput
  ) {
    updateCar(input: $input, condition: $condition) {
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
export const deleteCar = /* GraphQL */ `
  mutation DeleteCar(
    $input: DeleteCarInput!
    $condition: ModelCarConditionInput
  ) {
    deleteCar(input: $input, condition: $condition) {
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
export const createLapTime = /* GraphQL */ `
  mutation CreateLapTime(
    $input: CreateLapTimeInput!
    $condition: ModelLapTimeConditionInput
  ) {
    createLapTime(input: $input, condition: $condition) {
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
export const updateLapTime = /* GraphQL */ `
  mutation UpdateLapTime(
    $input: UpdateLapTimeInput!
    $condition: ModelLapTimeConditionInput
  ) {
    updateLapTime(input: $input, condition: $condition) {
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
export const deleteLapTime = /* GraphQL */ `
  mutation DeleteLapTime(
    $input: DeleteLapTimeInput!
    $condition: ModelLapTimeConditionInput
  ) {
    deleteLapTime(input: $input, condition: $condition) {
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
