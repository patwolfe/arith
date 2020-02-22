import React, { useState } from 'react';
import { 
  Image,
  StyleSheet,
  Text,
  TouchableOpacity,
  View } from 'react-native';

import * as ImagePicker from 'expo-image-picker';

import { getCameraPermissionAsync } from 'jumbosmash/utils/permissions';

export default function IDUpload(props) {
  const [pic, setPic] = useState(props.pic ? props.pic : 'none');
  let picDiv = null;
  if (pic === 'none') {
    picDiv = (<Text style={styles.content}>Touch to launch camera!</Text>);
  } else {
    picDiv = (<Image style={styles.content} source={{uri: pic}} />);
  }
  return (
    <View>  
      <TouchableOpacity style={styles.idBox}
        onPress={() => selectPhoto(setPic, props.setUri)}>
        {picDiv}
      </TouchableOpacity>
    </View>
  );
}

async function selectPhoto(setPic, setUri) {
  let status = await getCameraPermissionAsync('Uploading your ID requires camera access');
  if (status !== 'granted') {
    return;
  }

  let result = await ImagePicker.launchCameraAsync({
    allowsEditing: true,
    aspect: [2,1]
  });

  if (result.cancelled === true) {
    // leave state unchanged
    return;
  }
  setPic(result.uri);
  setUri(result.uri);
}

const styles = StyleSheet.create({
  idBox: {
    width: '70%',
    borderWidth: 1,
    borderStyle: 'solid',
    borderColor: 'black',
    aspectRatio: 2,
    alignSelf: 'center'
  },
  content: {
    height: '100%',
    width: '100%'
  }
});
