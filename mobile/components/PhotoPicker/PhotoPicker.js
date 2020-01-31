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
        {/* {[...Array(2).keys()].map((_, key) => {return <AddPhoto key={key} i={key}/>;})} */}
        {createAddPhotoRows()}
      </View>
    </View>
    );
}

function createAddPhotoRows() {
  let id  = 0;
  return [...Array(3).keys()].map((_, i) => {
    return (
      <View key={i} style={styles.photoBoxRow}> 
        {[...Array(2).keys()].map((_, j) => {
          return <AddPhoto key={id} i={id++}/>;
        })}
      </View>
    );});
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
  photoBoxRow: {
    justifyContent: 'space-around',
    width: '100%',
    flex: 1,
    flexDirection: 'row'
  },
  photoBoxesContainer: {
    display: 'flex',
    flexDirection: 'column',
    flexGrow: 6,
    marginBottom: '5%',
    paddingVertical: '7%',
    marginTop: '3%'
  }
});