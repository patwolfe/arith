import React, { useState } from 'react';
import {
  Button,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import PhotoPicker from 'jumbosmash/components/PhotoPicker/PhotoPicker';
import QuestionPicker from '../../components/QuestionPicker/QuestionPicker';

export default function CreateProfileScreen(props) {
  const { pictures, setPictures} = useState([]);
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        {/* <PhotoPicker picsHook={setPictures}/> */}
        <QuestionPicker />
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
