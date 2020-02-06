import React from 'react';
import {
  Button,
} from 'react-native';

import ProfileView from '../components/ProfileView/ProfileView';
import profiles from '../test_data/mockProfiles';


export default function ProfileScreen() {
    
  return (
    <ProfileView userProfile={profiles.patrick}/>
  );
}

ProfileScreen.navigationOptions = (props) => ({
  headerTitle: 'Your Profile',
  headerRight: (
    <Button
      title="Edit Profile"
      color="#aaa"
      onPress={() => props.navigation.navigate('Edit')}
    />)
});