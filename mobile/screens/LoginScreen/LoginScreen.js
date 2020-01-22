import React, { useState } from 'react';
import {
  Button,
  StyleSheet,
  Text,
  View,
  TextInput,
} from 'react-native';

import LoadingModal from '../../components/LoadingModal/LoadingModal';

export default function LoginScreen(props) {
  const [email, setEmail] = useState('');
  const [rejected, setRejected] = useState(false);
  const [loading, setLoading] = useState(false);
  let rejectedDiv;
  if (rejected) {
    rejectedDiv = (<Text style={styles.rejectedText}>Your email was rejected. Please make sure it is your valid Tufts email address</Text>);
  }
  return (
    <View style={styles.container}>
      <LoadingModal loading={loading}/>
      <Text style={styles.header}>Welcome Back!</Text> 
      {rejectedDiv}
      <TextInput style={styles.inputField}
        editable
        autoCapitalize='none'
        onChangeText={(newText) => setEmail(newText)}/>     
      <Button title='Login'
        onPress={() => {
          setLoading(true);
          checkEmail(email).then(valid =>
          { 
            if (valid) {
              setRejected(false);
              props.navigation.navigate('Verify');
            }
            else {
              setRejected(true);
            }
            setLoading(false);
          });
        }
        }
      />
    </View>
  );
}

async function checkEmail(email) {
  // Async sleep to mock API call
  await new Promise((resolve) => setTimeout(resolve, 3000));
  email = email.toLowerCase();
  if (email === 'patrick.wolfe@tufts.edu' ||
      email === 'alexis.walker@tufts.edu' ||
      email === 'william.rusk@tufts.edu') {
    return true;
  }
  return false;
}

LoginScreen.navigationOptions = {
  header: null,
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#a9c6de',
  },
  header: {
    marginTop: '30%',
    padding: '10%',
    paddingBottom: '3%',
  },
  inputField: {
    backgroundColor: '#ffffff',
    marginHorizontal: '15%',
    paddingVertical: '2%'
  },
  rejectedText: {
    color: 'red',
  }
});