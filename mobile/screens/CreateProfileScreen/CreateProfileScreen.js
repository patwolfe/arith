import React, { useState } from 'react';
import {
  StyleSheet,
  View,
} from 'react-native';

import CreateProfileWizard from 'jumbosmash/components/CreateProfileWizard/CreateProfileWizard';

export default function CreateProfileScreen(props) {
  return (
    <View style={styles.content}>
      <CreateProfileWizard 
        userName='Pat Wolfe'
        userPronouns='he/his'
      />
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
