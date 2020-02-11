import React, { useState } from 'react';
import {
  Button,
  StyleSheet,
  Text,
  View,
  TextInput,
} from 'react-native';

import LoadingModal from 'jumbosmash/components/LoadingModal/LoadingModal';
import urls from 'jumbosmash/constants/Urls';

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
        onChangeText={(newText) => setEmail(newText.toLowerCase())}/>     
      <Button title='Login'
        onPress={() => {
          setLoading(true);
          requestEmail(email).then(valid =>
          { 
            if (valid) {
              setRejected(false);
              console.log(email);
              props.navigation.navigate('OTP', {email: email});
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

async function requestEmail(email) {
  console.log(urls.backendURL);
  let url = `${urls.backendURL}auth/email/`;
  console.log(url);
  console.log('here');
  console.log('there'); 
  try {
    const response = await fetch(url, {
      method: 'POST', 
      cache: 'no-cache', 
      redirect: 'folloW', 
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `email=${email}`
    });
    let res = await response.json(); // parses JSON response into native JavaScript objects  await fetch 
    console.log(res);
    return true;
  }
  catch (e) {
    console.log(e);
    return false;
  }
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