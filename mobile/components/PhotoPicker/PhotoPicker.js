import React, {useEffect} from 'react';
import { 
  StyleSheet,
  Text, 
  View } from 'react-native';

import { getPermissionAsync } from 'jumbosmash/utils/permissions';
import PhotoBox from './PhotoBox/PhotoBox';

export default function PhotoPicker(props) {
  useEffect(() => {
    getPermissionAsync('Uploading pictures requires camera role access');
  });
  return (
    <View style={styles.photoPickerContainer}>
      <View style={styles.titleContainer}>
        <Text style={styles.titleText}>Add Photos</Text>
      </View>
      <View style={styles.photoBoxesContainer}>
        {createPhotoBoxRows(props.dispatch)}
      </View>
    </View>);
}

function createPhotoBoxRows(dispatch) {
  return [...Array(3).keys()].map((i) => {
    return (
      <View key={i} style={styles.photoBoxRow}> 
        {[...Array(2).keys()].map((j) => {
          let id = (2 * i) + j;
          return <PhotoBox key={id} id={id} dispatch={dispatch}/>;
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