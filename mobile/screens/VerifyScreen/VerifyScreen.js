import React from 'react';
import {
  StyleSheet,
  View,
  Text,
} from 'react-native';

export default function VerifyScreen() {
  return (
    <View style={styles.container}>
      <Text>Verification Screen !!!</Text>
    </View>
  );
}

VerifyScreen.navigationOptions = {
  header: null,
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingVertical: '30%',
    backgroundColor: '#a9c6de',
  },
});