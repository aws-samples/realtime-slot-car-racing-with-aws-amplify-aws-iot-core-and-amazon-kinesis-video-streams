const appsync = require('./graphql-client').appsync;
const gql = require('graphql-tag');
const { CORE_OVERVIEW_ID } = require('./constants')

exports.createCar = async (carData) => {
  const createCarMutation = gql`
    mutation CreateCar(
      $input: CreateCarInput!
      $condition: ModelCarConditionInput
    ) {
    createCar(input: $input, condition: $condition) {
      id
    }}
  `;
  return appsync
    .mutate({
      mutation: createCarMutation,
      fetchPolicy: 'no-cache',
      variables: {
        input: carData,
      },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.getCar = async (id) => {
  const getCarQuery = gql`
    query GetCar($id: ID!) {
      getCar(id: $id) {
        id
        color
        throttle
        fuelLevel
        speed
        tireWear
        createdAt
        updatedAt
      }
    }
  `;
  return appsync
    .query({
      query: getCarQuery,
      fetchPolicy: 'no-cache',
      variables: { id },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.getOverview = async () => {
  const getOverviewQuery = gql`
    query GetOverview($id: ID!) {
      getOverview(id: $id) {
        id
      }
    }
  `;
  return appsync
    .query({
      query: getOverviewQuery,
      fetchPolicy: 'no-cache',
      variables: { id: CORE_OVERVIEW_ID },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.createOverview = async () => {
  const createOverviewMutation = gql`
    mutation CreateOverview(
      $input: CreateOverviewInput!
      $condition: ModelOverviewConditionInput
    ) {
      createOverview(input: $input, condition: $condition) {
        id
    }}
  `;
  return appsync
    .mutate({
      mutation: createOverviewMutation,
      fetchPolicy: 'no-cache',
      variables: {
        input: { id: CORE_OVERVIEW_ID }
      },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.createRace = async (raceData) => {
  const createRaceMutation = gql`
    mutation CreateRace(
      $input: CreateRaceInput!
      $condition: ModelRaceConditionInput
    ) {
      createRace(input: $input, condition: $condition) {
        id
    }}
  `;
  return appsync
    .mutate({
      mutation: createRaceMutation,
      fetchPolicy: 'no-cache',
      variables: {
        input: raceData
      },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.createPlayer = async (playerData) => {
  const createPlayerMutation = gql`
    mutation CreatePlayer(
      $input: CreatePlayerInput!
      $condition: ModelPlayerConditionInput
    ) {
      createPlayer(input: $input, condition: $condition) {
        id
    }}
  `;
  return appsync
    .mutate({
      mutation: createPlayerMutation,
      fetchPolicy: 'no-cache',
      variables: {
        input: playerData
      },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.updateOverview = async (updateOverviewData) => {
  const updateOverviewMutation = gql`
    mutation UpdateOverview(
      $input: UpdateOverviewInput!
      $condition: ModelOverviewConditionInput
    ) {
      updateOverview(input: $input, condition: $condition) {
        id
      }
    }
  `;
  return appsync
    .mutate({
      mutation: updateOverviewMutation,
      fetchPolicy: 'no-cache',
      variables: {
        input: updateOverviewData
      },
    })
    .then((res) => res)
    .catch((err) => { throw new Error(err) });
}

exports.updateRace = async (updateRaceData) => {
  const updateRaceMutation = gql`
    mutation UpdateRace(
      $input: UpdateRaceInput!
      $condition: ModelRaceConditionInput
    ) {
      updateRace(input: $input, condition: $condition) {
        id
      }
    }
  `;
  return appsync
    .mutate({
      mutation: updateRaceMutation,
      fetchPolicy: 'no-cache',
      variables: {
        input: updateRaceData
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
            createdAt
            updatedAt
            racePlayersId
            playerCarId
          }
          nextToken
        }
        nrOfLaps
        currentRaceState
        createdAt
        updatedAt
        overviewAllRacesId
        raceFinalStatsId
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