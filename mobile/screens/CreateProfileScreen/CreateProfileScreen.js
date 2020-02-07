import React, { useState } from 'react';
import {
  Button,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import PhotoPicker from '../../components/PhotoPicker/PhotoPicker'

export default function CreateProfileScreen(props) {
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <PhotoPicker />
      </View>
    </View>
  );
}

CreateProfileScreen.navigationOptions = {
  header: null
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#a9c6de',
  },
  content: {
    paddingHorizontal: '5%',
    flex: 1
  }
});
