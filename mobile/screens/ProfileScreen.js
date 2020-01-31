import React from 'react';
import {
  Button,
} from 'react-native';
import ProfileView from '../components/ProfileView/ProfileView';
import profiles from '../test_data/UserProfiles';

export default function ProfileScreen() {
    
  return (
    <ProfileView user_profile={profiles.patrick}/>
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