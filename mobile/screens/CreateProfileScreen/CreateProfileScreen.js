import React from 'react';
import {
  StyleSheet,
  View,
} from 'react-native';

import OTPInput from 'jumbosmash/components/OTPInput/OTPInput';

export default function CreateProfileScreen() {
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
