import React from 'react';
import { 
  StyleSheet,
  Text, 
  View } from 'react-native';
import AddPhoto from './AddPhoto/AddPhoto'


export default function PhotoPicker(props) {
  return (
    <View style={styles.photoPickerContainer}>
      <Text style={styles.titleText}>Add Photos</Text>
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
  titleText: {
    flexGrow: 1,
    marginTop: '30%'
  },
  photoBoxesContainer: {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    flexGrow: 4,
    paddingVertical: '7%',
    justifyContent: 'space-between',
  }
});