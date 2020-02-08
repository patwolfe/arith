import React, { useState } from 'react';
import {
  Button,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import PhotoPicker from 'jumbosmash/components/PhotoPicker/PhotoPicker'
import OTPInput from '../../components/OTPInput/OTPInput';

export default function CreateProfileScreen(props) {
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <OTPInput />
      </View>
    </View>
  );
}

CreateProfileScreen.navigationOptions = {
  header: null
};

const styles = StyleSheet.create({
  container: {
    flex: 1
  },
  content: {
    paddingHorizontal: '5%',
    flex: 1
  }
});
