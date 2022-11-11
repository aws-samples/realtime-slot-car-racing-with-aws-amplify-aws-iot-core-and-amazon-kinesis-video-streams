export const customGetOverview = /* GraphQL */ `
  query GetOverview($id: ID!) {
    getOverview(id: $id) {
      id
      currentRace {
        id
        players {
          items {
            id
            car {
              color
              id
            }
            claims {
              items {
                id
                uuid
                username
              }
            }
          }
        }
        currentRaceState
        nrOfLaps
      }
    }
  }
`;

export const customGetRace = /* GraphQL */ `
  query GetRace($id: ID!) {
    getRace(id: $id) {
      id
      nrOfLaps
      currentRaceState
      players {
        items {
          id
          createdAt
          updatedAt
          racePlayersId
          playerCarId
          allLapTimes {
            items {
              id
              playerId
              timeInMilliSec
              createdAt
              updatedAt
              raceId
            }
            nextToken
          }
          claims {
            items {
              id
              uuid
              username
            }
          }
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
        }
        nextToken
      }
      lapTimes {
        items {
          id
          playerId
          timeInMilliSec
          createdAt
          updatedAt
          raceId
        }
        nextToken
      }
      nrOfLaps
      currentRaceState
      createdAt
      updatedAt
      overviewAllRacesId
    }
  }
`;

// TODO: Where-ever we subscribe, instead of just getting the id, get other info to and update state
export const customOnUpdateRaceById = /* GraphQL */ `
  subscription OnUpdateRaceById($id: String!) {
    onUpdateRaceById(id: $id) {
      id
    }
  }
`;

export const customOnUpdatePlayerClaim = /* GraphQL */ `
  subscription OnUpdatePlayerClaim {
    onUpdatePlayerClaim {
      id
    }
  }
`;

export const customOnCreatePlayerClaim = /* GraphQL */ `
  subscription OnCreatePlayerClaim {
    onCreatePlayerClaim {
      id
    }
  }
`;

export const customOnUpdateOverview = /* GraphQL */ `
subscription OnUpdateOverview {
  onUpdateOverview {
    id
  }
}
`;

export const customOnCreateLapTime = /* GraphQL */ `
subscription OnCreateLapTime {
  onCreateLapTime {
    id
    raceId
    playerId
    player {
      id
      claims {
        items {
          id
          uuid
          username
        }
      }
      car {
        id
        color
      }
    }
    timeInMilliSec
    type
    createdAt
    updatedAt
  }
}
`;

export const customLapTimesByPlayerId = /* GraphQL */ `
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
        playerId
        timeInMilliSec
        type
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;

export const customLapTimesByRaceId = /* GraphQL */ `
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
        playerId
        player {
          id
          claims {
            items {
              id
              uuid
              username
            }
          }
          car {
            id
            color
          }
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

export const customLapTimesByTime = /* GraphQL */ `
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
        playerId
        player {
          id
          claims {
            items {
              username
            }
          }
        }
        timeInMilliSec
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;