const appsync = require('./graphql-client').appsync;
const gql = require('graphql-tag');
const { LAPTIME_TYPE_STRING } = require('./constants')

exports.createLapTime = async (lapTimeData) => {
  const createLapTimeMutation = gql`
    mutation CreateLapTime(
      $input: CreateLapTimeInput!
      $condition: ModelLapTimeConditionInput
    ) {
      createLapTime(input: $input, condition: $condition) {
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
      }}
  `;
  lapTimeData.type = LAPTIME_TYPE_STRING
  return appsync
    .mutate({
      mutation: createLapTimeMutation,
      fetchPolicy: 'no-cache',
      variables: {
        input: lapTimeData,
      },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.getRace = async (id) => {
  const getRaceQuery = gql`
    query GetRace($id: ID!) {
      getRace(id: $id) {
        id
        players {
          items {
            id
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
  return appsync
    .query({
      query: getRaceQuery,
      fetchPolicy: 'no-cache',
      variables: { id },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.getLapTimesByRace = async (id) => {
  const lapTimesQuery = gql`
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
            timeInMilliSec
            createdAt
            updatedAt
          }
          nextToken
        }
      }`;
  return appsync
    .query({
      query: lapTimesQuery,
      fetchPolicy: 'no-cache',
      variables: {
        id: id,
        limit: 10000
      },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}