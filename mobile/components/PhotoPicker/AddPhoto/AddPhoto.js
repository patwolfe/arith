import React from 'react';
import { 
  StyleSheet,
  Text,
  TouchableOpacity } from 'react-native';

export default function AddPhoto(props) {
  const [pic, setPic] = useState('none');
  let picDiv = null;
  if (pic === 'none') {
    picDiv = (<Text style={styles.content}>#{props.i}</Text>);
  } else {
    picDiv = (<Image style={styles.content} source={{uri: pic}} />);
  }
  return (
    <TouchableOpacity style={styles.photoBox}
      onPress={() => selectPhoto(setPic)}>
      {picDiv}
    </TouchableOpacity>
  );
}

async function selectPhoto(setPic) {
  let result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    aspect: [1,1],
  });

  if (result.cancelled === true) {
    // leave state unchanged
    return;    
  }
  setPic(result.uri);
}

const styles = StyleSheet.create({
  photoBox: {
    width: '35%',
    marginTop: '3%',
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
