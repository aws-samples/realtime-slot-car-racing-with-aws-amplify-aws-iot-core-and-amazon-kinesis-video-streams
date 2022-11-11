import React from 'react'
import {Link, useNavigate} from 'react-router-dom'
import {Button, Flex, Heading, Text, useAuthenticator} from '@aws-amplify/ui-react'

export default function Home() {
  const { route, signOut } = useAuthenticator((context) => [
    context.route,
    context.signOut,
  ]);
  const navigate = useNavigate();

  const logOut = () => {
    signOut();
    navigate('/');
  }

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
            Select any of the options below. Click on "Join current race" to join the race lobby.
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
          <Link to={'/admin'}>
            <Button
                variation='primary'
                width='80%'
                alignSelf={'center'}
            >
              Admin dashboard
            </Button>
          </Link>
          <Link to={'/race-overview'}>
            <Button
                variation='primary'
                width='80%'
                alignSelf={'center'}
            >
              Race Overview
            </Button>
          </Link>
          {route === 'authenticated' && (
              <Button variation='primary'
                      width='80%'
                      alignSelf={'center'}
                      onClick={() => logOut()}>
                Logout
              </Button>
          )}
        </Flex>
      </Flex>
  )
}
