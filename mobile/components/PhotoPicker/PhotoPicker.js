import React from 'react';
import { 
  StyleSheet,
  Text, 
  View } from 'react-native';
import AddPhoto from './AddPhoto/AddPhoto'


export default function PhotoPicker() {
  return (
    <View style={styles.photoPickerContainer}>
      <View style={styles.titleContainer}>
      <Text style={styles.titleText}>Add Photos</Text>
      </View>
      <View style={styles.photoBoxesContainer}>
        {[...Array(6).keys()].map((_, key) => {return <AddPhoto key={key} i={key}/>})}
      </View>
    </View>
    );
}

const styles = StyleSheet.create({
  photoPickerContainer: {
    display: 'flex',
    flex: 1
  },
  titleContainer: {
    alignContent: 'center'
  },
  titleText: {
    flexGrow: 1,
    marginTop: '15%',
  },
  photoBoxesContainer: {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    flexGrow: 6,
    marginBottom: '5%',
    paddingVertical: '7%',
    justifyContent: 'space-around'
  }
});