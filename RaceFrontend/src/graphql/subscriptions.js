/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const onUpdateRaceById = /* GraphQL */ `
  subscription OnUpdateRaceById($id: String!) {
    onUpdateRaceById(id: $id) {
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
export const onCreateOverview = /* GraphQL */ `
  subscription OnCreateOverview {
    onCreateOverview {
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
export const onUpdateOverview = /* GraphQL */ `
  subscription OnUpdateOverview {
    onUpdateOverview {
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
export const onDeleteOverview = /* GraphQL */ `
  subscription OnDeleteOverview {
    onDeleteOverview {
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
export const onCreateRace = /* GraphQL */ `
  subscription OnCreateRace {
    onCreateRace {
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
export const onUpdateRace = /* GraphQL */ `
  subscription OnUpdateRace {
    onUpdateRace {
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
export const onDeleteRace = /* GraphQL */ `
  subscription OnDeleteRace {
    onDeleteRace {
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
export const onCreateFinalRaceStats = /* GraphQL */ `
  subscription OnCreateFinalRaceStats {
    onCreateFinalRaceStats {
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
export const onUpdateFinalRaceStats = /* GraphQL */ `
  subscription OnUpdateFinalRaceStats {
    onUpdateFinalRaceStats {
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
export const onDeleteFinalRaceStats = /* GraphQL */ `
  subscription OnDeleteFinalRaceStats {
    onDeleteFinalRaceStats {
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
export const onCreatePlayer = /* GraphQL */ `
  subscription OnCreatePlayer {
    onCreatePlayer {
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
export const onUpdatePlayer = /* GraphQL */ `
  subscription OnUpdatePlayer {
    onUpdatePlayer {
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
export const onDeletePlayer = /* GraphQL */ `
  subscription OnDeletePlayer {
    onDeletePlayer {
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
export const onCreatePlayerClaim = /* GraphQL */ `
  subscription OnCreatePlayerClaim {
    onCreatePlayerClaim {
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
export const onUpdatePlayerClaim = /* GraphQL */ `
  subscription OnUpdatePlayerClaim {
    onUpdatePlayerClaim {
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
export const onDeletePlayerClaim = /* GraphQL */ `
  subscription OnDeletePlayerClaim {
    onDeletePlayerClaim {
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
export const onCreateCar = /* GraphQL */ `
  subscription OnCreateCar {
    onCreateCar {
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
export const onUpdateCar = /* GraphQL */ `
  subscription OnUpdateCar {
    onUpdateCar {
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
export const onDeleteCar = /* GraphQL */ `
  subscription OnDeleteCar {
    onDeleteCar {
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
export const onCreateLapTime = /* GraphQL */ `
  subscription OnCreateLapTime {
    onCreateLapTime {
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
export const onUpdateLapTime = /* GraphQL */ `
  subscription OnUpdateLapTime {
    onUpdateLapTime {
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
export const onDeleteLapTime = /* GraphQL */ `
  subscription OnDeleteLapTime {
    onDeleteLapTime {
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
