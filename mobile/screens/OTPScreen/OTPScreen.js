import React, { useState } from 'react';
import {
  StyleSheet,
  View,
} from 'react-native';

import LoadingModal from 'jumbosmash/components/LoadingModal/LoadingModal';
import OTPInput from 'jumbosmash/components/OTPInput/OTPInput';

export default function OTPScreen(props) {
  const [loading, setLoading] = useState(false);
  const email = props.navigation.getParam('email', 'Undefined');
  return (
    <View style={styles.container}>
      {loading ? 
        <LoadingModal /> :
        <OTPInput email={email} loadingHook={setLoading}/>
      }
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