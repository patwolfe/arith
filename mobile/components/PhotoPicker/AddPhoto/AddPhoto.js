import React from 'react';
import { 
  StyleSheet,
  Text,
  TouchableOpacity } from 'react-native';

export default function AddPhoto(props) {
  return (
    <TouchableOpacity style={styles.photoBox}>
      <Text>#{props.i}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  photoBox: {
    width: '30%',
    height: '40%',
    marginTop: '3%',
    borderWidth: 1,
    borderStyle: 'solid',
    borderColor: 'black'
  }
});
