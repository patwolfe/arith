import React, { useState, useReducer } from 'react';
import {
  Button,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import IDUpload from 'jumbosmash/components/IDUpload/IDUpload';

function NameEmail(props) {
  return (
    <View style={styles.content}>
      <View style={styles.fieldWithTitle}>
        <Text>Name:</Text>
        <TextInput style={styles.inputField}
          editable
          autoCapitalize='none'
          onChangeText={(newText) => props.setName(newText)}/>     
      </View>
      <View style={styles.fieldWithTitle}>
        <Text>Email:</Text>
        <TextInput style={styles.inputField}
          editable
          autoCapitalize='none'
          onChangeText={(newText) => props.setEmail(newText)}/>     
      </View>
    </View>
  );
}

export default function RegisterScreen(props) {
  const initialState = {
    email: '',
    name: '',
    idUri: '',
    stage: 'name-email',
    navigation: props.navigation
  };
  const [state, dispatch] = useReducer(reducer, initialState);
  const nameEmail = 
    <NameEmail 
      setEmail={(email) => dispatch({type: 'email', email: email})} 
      setName={(name) => dispatch({type: 'name', name: name})} 
    />;
  const idUpload = <IDUpload setUri={(uri) => dispatch({type: 'id', uri: uri})}/>;
  return (
    <View style={styles.container}>
      {state.stage === 'name-email' ? nameEmail : idUpload}
      <Button title={state.stage === 'id-upload' ? 'Upload' : 'Register'} 
        onPress={() => dispatch({type: 'button'})} /> 
    </View>
  );
}

function reducer(state, action) {
  switch(action.type) {
  case 'id':
    return {...state, idUri: action.idUri};
  case 'name':
    return {...state, name: action.name};
  case 'email':
    return {...state, email: action.email};
  case 'button': {
    let nextStep = '';
    if (state.stage === 'name-email') {
      nextStep = 'id-upload';
    } else if (state.stage === 'id-upload') {
      nextStep = 'done';
    } else {
      nextStep = 'done';
    }
    return {...state, stage: nextStep};
  }
  default:
    throw new Error('Invalid reducer action');
  }

}

RegisterScreen.navigationOptions = {
  header: null
};

const styles = StyleSheet.create({
  parentContainer: {
    flex: 1
  },
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
