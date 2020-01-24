/* eslint-disable */
import React from 'react';
import { Platform } from 'react-native';
import { createStackNavigator } from 'react-navigation-stack';
import { createBottomTabNavigator } from 'react-navigation-tabs';
import TabBarIcon from '../components/TabBarIcon';

// Screens
import ChatListScreen from '../screens/ChatListScreen/ChatListScreen';
import ChatScreen from '../screens/ChatScreen/ChatScreen';
import EditProfileScreen from '../screens/EditProfileScreen';
import EntryScreen from '../screens/EntryScreen/EntryScreen';
import HomeScreen from '../screens/HomeScreen';
import LoginScreen from '../screens/LoginScreen/LoginScreen';
import MatchFeedScreen from '../screens/MatchFeedScreen/MatchFeedScreen';
import ProfileScreen from '../screens/ProfileScreen';
import SettingsScreen from '../screens/SettingsScreen'
import VerifyScreen from '../screens/VerifyScreen/VerifyScreen';

const config = Platform.select({
  web: { headerMode: 'screen' },
  default: {},
});

const ProfileStack = createStackNavigator(
  {
    Profile: ProfileScreen,
    Edit: EditProfileScreen,
  },
  config
);


ProfileStack.navigationOptions = {
  tabBarLabel: 'Profile',
  tabBarIcon: ({ focused }) => (
    <TabBarIcon
      focused={focused}
      name={
        Platform.OS === 'ios'
          ? 'ios-contact'
          : 'md-contact'
      }
    />
  ),
};

ProfileStack.path = '';

const HomeStack = createStackNavigator(
  {
    Home: HomeScreen,
  },
  config
);

HomeStack.navigationOptions = {
  tabBarLabel: 'Home',
  tabBarIcon: ({ focused }) => (
    <TabBarIcon
      focused={focused}
      name={
        Platform.OS === 'ios'
          ? `ios-information-circle${focused ? '' : '-outline'}`
          : 'md-information-circle'
      }
    />
  ),
};

HomeStack.path = '';

const MatchStack = createStackNavigator(
  {
    Feed: MatchFeedScreen,
  },
  config
);

MatchStack.navigationOptions = {
  tabBarLabel: 'Feed',
  tabBarIcon: ({focused}) => (
    <TabBarIcon
      focused={focused}
      name={
        Platform.OS === 'ios'
        ? `ios-information-circle${focused ? '' : '-outline'}`
        : 'md-information-circle'
      }
    />
  ),
};

const SettingsStack = createStackNavigator(
  {
    Settings: SettingsScreen,
  },
  config
);

SettingsStack.navigationOptions = {
  tabBarLabel: 'Settings',
  tabBarIcon: ({ focused }) => (
    <TabBarIcon focused={focused} name={Platform.OS === 'ios' ? 'ios-options' : 'md-options'} />
  ),
};

const ChatStack = createStackNavigator(
  {
    ChatList: {
      screen: ChatListScreen,
    },
    Chat: {
      screen: ChatScreen,
    },
  },
  {
    initialRouteName: 'ChatList',
  },
  config,
);

ChatStack.navigationOptions = {
  tabBarLabel: 'Chat',
  tabBarIcon: ({ focused }) => (
    <TabBarIcon
      focused={focused}
      name={
        Platform.OS === 'ios'
          ? `ios-information-circle${focused ? '' : '-outline'}`
          : 'md-information-circle'
      }
    />
  ),
};

ChatStack.path = '';

const EntryStack = createStackNavigator(
  {
    Entry: {
      screen: EntryScreen,
    },
    SignIn: {
      screen: LoginScreen,
    },
    Verify: {
      screen: VerifyScreen,
    },
  },
  {
    initialRouteName: 'Entry',
  },
  config,
);

EntryStack.navigationOptions = {
  tabBarLabel: 'Entry',
  tabBarIcon: ({ focused }) => (
    <TabBarIcon
      focused={focused}
      name={
        Platform.OS === 'ios'
          ? `ios-information-circle${focused ? '' : '-outline'}`
          : 'md-information-circle'
      }
    />
  ),
};

ChatStack.path = '';

const tabNavigator = createBottomTabNavigator({
  ProfileStack,
  HomeStack,
  MatchStack,
  SettingsStack,
  ChatStack,
  EntryStack,
});

tabNavigator.path = '';

export default tabNavigator;