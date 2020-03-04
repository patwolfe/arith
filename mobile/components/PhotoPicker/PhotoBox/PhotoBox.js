import React, { useState } from 'react';
import { 
  Image,
  StyleSheet,
  Text,
  TouchableOpacity } from 'react-native';

import * as ImagePicker from 'expo-image-picker';

import { getPermissionAsync } from 'jumbosmash/utils/permissions';

/* Props:
 * dispatch: function from userReducer in parent component
 * that update's parent state with the uri of selected image
 * 
 * id: Integer key for image used if parent state contains a 
 * list or object of image uris
 */
export default function PhotoBox(props) {
  const [pic, setPic] = useState(props.pic ? props.pic : 'none');
  let picDiv = null;
  if (pic === 'none') {
    picDiv = (<Text style={styles.content}>#{props.id}</Text>);
  } else {
    picDiv = (<Image style={styles.content} source={{uri: pic}} />);
  }
  return (
    <TouchableOpacity style={styles.photoBox}
      onPress={() => selectPhoto(props.id, setPic, props.dispatch)}>
      {picDiv}
    </TouchableOpacity>
  );
}

async function selectPhoto(id, setPic, dispatch) {
  let status = await getPermissionAsync('Uploading pictures requires camera role access');
  if (status !== 'granted') {
    return;
  }

  let result = await ImagePicker.launchImageLibraryAsync({
    allowsEditing: true,
    aspect: [1,1],
  });

  if (result.cancelled === true) {
    // leave state unchanged
    return;
  }
  dispatch({type: 'picture', id: id, payload: result.uri});
  setPic(result.uri);
}

const styles = StyleSheet.create({
  photoBox: {
    width: '35%',
    borderWidth: 1,
    borderStyle: 'solid',
    borderColor: 'black',
    aspectRatio: 1
  },
  content: {
    height: '100%',
    width: '100%'
  }
});
