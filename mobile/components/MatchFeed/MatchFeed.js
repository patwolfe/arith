import React, { useState } from 'react';
import ProfileView from '../ProfileView/ProfileView';
import { View, Text, StyleSheet } from 'react-native';
import Swipeable from 'react-native-gesture-handler/Swipeable';
import profiles from '../../test_data/mockProfiles';

export default function MatchFeed() {
  const names = ['will', 'patrick', 'lexi', 'steven'];
  const [state, setState] = useState(
    {profiles: names.slice(0),
    profile: null,});
  if (!state.profile) {
    setState({profiles: state.profiles.slice(1), profile: state.profiles[0]});
  }

  function changeState(){
    if (state.profiles.length == 0) {
      setState({profiles: names.slice(0)});
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
        <ProfileView userProfile={profiles[state.profile]} />
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
  leftPanel: {
    backgroundColor: '#33cc33',
  },
  rightPanel: {
    backgroundColor: '#ff0000',
  },
});
