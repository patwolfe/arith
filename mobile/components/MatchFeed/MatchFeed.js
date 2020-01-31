import React, { useState } from 'react';
import { TouchableOpacity, Button, View, Text, StyleSheet } from 'react-native';
import ProfileView from '../ProfileView/ProfileView';
import {PanGestureHandler} from 'react-native-gesture-handler';
import Swipeable from 'react-native-gesture-handler/Swipeable';
import profiles from '../../test_data/UserProfiles';

export default function MatchFeed() {
  const [state, setState] = useState(
    {profiles: [<ProfileView user_profile={profiles.will}/>, 
      <ProfileView user_profile={profiles.lexi} />, 
      <ProfileView user_profile={profiles.steven} />,
      <ProfileView user_profile={profiles.patrick} />], 
    profile: null,});
  if (!state.profile) {
    setState({profiles: state.profiles.slice(1), profile: state.profiles[0]});
  }

  function changeState(){
    if (state.profiles.length == 0) {
      setState({profiles: [<ProfileView user_profile={profiles.will}/>, 
        <ProfileView user_profile={profiles.lexi} />, 
        <ProfileView user_profile={profiles.patrick} />],
      profile: <ProfileView user_profile={profiles.steven} />});
    } else {
      setState({profiles: state.profiles.slice(1), 
        profile: state.profiles[0]});
    }
  }
  let swipeableRef = null;

  return (
    <View style={styles.container}>
      <Swipeable
        leftThreshold={20}
        rightThreshold={20}
        ref={ref => swipeableRef = ref}
        // Actions that occur when the tab is opened
        onSwipeableLeftOpen={() => {
          // do something with state.profile
          swipeableRef.close();
          changeState();
        }}
        onSwipeableRightOpen={() => {
          // do something with state.profile
          swipeableRef.close();
          changeState();
        }}
        // Render functions for tabs
        renderLeftActions={() => {
          return (
            <View style={styles.leftPanel}><Text>Match!</Text></View>
          );
        }}
        renderRightActions={() => {
          return (
            <View style={styles.rightPanel}><Text>Denied!</Text></View>
          );
        }}
      >
        {state.profile}
      </Swipeable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    borderStyle: 'solid',
    borderWidth: 1,
    margin: '5%',
  },
  button: {
    borderStyle: 'solid',
    borderWidth: 1,
    marginLeft: 50,
    marginRight: 50
  },
  text: {
    textAlign: 'center',
  },
  leftPanel: {
    backgroundColor: '#33cc33',
  },
  rightPanel: {
    backgroundColor: '#ff0000',
  },
});
