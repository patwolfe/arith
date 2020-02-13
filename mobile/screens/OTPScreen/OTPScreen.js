import React from 'react';
import {
  StyleSheet,
  View,
} from 'react-native';

import OTPInput from 'jumbosmash/components/OTPInput/OTPInput';

export default function OTPScreen(props) {
  const email = props.navigation.getParam('email', 'Undefined');
  return (
    <View style={styles.container}>
      <OTPInput email={email}/>
    </View>
  );
}

OTPScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingVertical: '30%',
    backgroundColor: '#a9c6de',
  },
});