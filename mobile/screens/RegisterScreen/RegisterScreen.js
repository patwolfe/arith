import React, { useState } from 'react';
import {
  Button,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';


export default function RegisterScreen(props) {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <View style={styles.fieldWithTitle}>
          <Text>Name:</Text>
          <TextInput style={styles.inputField}
            editable
            autoCapitalize='none'
            onChangeText={(newText) => setName(newText)}/>     
        </View>
        <View style={styles.fieldWithTitle}>
          <Text>Email:</Text>
          <TextInput style={styles.inputField}
            editable
            autoCapitalize='none'
            onChangeText={(newText) => setEmail(newText)}/>     
        </View>
        <Button title='Register' 
          onPress={() => 
            props.navigation.navigate('CreateProfile')} />
      </View>
    </View>
  );
}

RegisterScreen.navigationOptions = {
  header: null
};

const styles = StyleSheet.create({
  container: {
    paddingTop: '30%',
    flex: 1,
    backgroundColor: '#a9c6de',
  },
  content: {
    justifyContent: 'space-around',
    paddingHorizontal: '5%'
  },
  inputField: {
    backgroundColor: '#ffffff',
    marginHorizontal: '15%',
    paddingVertical: '2%'
  },
  fieldWithTitle: {
    paddingVertical: '5%'
  }
});
