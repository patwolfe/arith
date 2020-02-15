import React from 'react';
import {
  StyleSheet,
  View,
} from 'react-native';

import CreateProfileWizard from 'jumbosmash/components/CreateProfileWizard/CreateProfileWizard';
import Test from 'jumbosmash/components/Test';
export default function CreateProfileScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <CreateProfileWizard />
        {/* <Test /> */}
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
