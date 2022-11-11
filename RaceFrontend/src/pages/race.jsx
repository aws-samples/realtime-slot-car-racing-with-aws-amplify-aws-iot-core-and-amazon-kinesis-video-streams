import React from 'react'
import { Link, useParams } from 'react-router-dom'
import { Button, Flex, Heading, Text } from '@aws-amplify/ui-react'

export default function Race(props) {
  const params = useParams()
  console.log(params)
  return (
    <Flex
      direction={{ base: 'column', large: 'row' }}
      // maxWidth="32rem"
      padding='1rem'
      width='100%'
    >
      <Flex justifyContent='space-between' direction='column'>
        <Heading level={3}>Welcome to re:Invent racer</Heading>
        <Text>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Volutpat
          sed cras ornare arcu dui. Duis aute irure dolor in reprehenderit in
          voluptate velit esse.
        </Text>
        <Link to={'/race-lobby'}>
          <Button
            variation='primary'
            width='80%'
            alignSelf={'center'}
          >
            Join current race
          </Button>
        </Link>
        <Button
          variation='primary'
          onClick={() => alert('Added item to cart!')}
          width='80%'
          alignSelf={'center'}
        >
          Admin dashboard
        </Button>
        <Button
          variation='primary'
          onClick={() => alert('Added item to cart!')}
          width='80%'
          alignSelf={'center'}
        >
          See overall stats
        </Button>
      </Flex>
    </Flex>
  )
}