import React, { 
  useReducer, useState, useEffect, 
} from 'react';

import { 
  StyleSheet,
  Text,
  TextInput, 
  View 
} from 'react-native';

import LoadingModal from 'jumbosmash/components/LoadingModal/LoadingModal';
import urls from 'jumbosmash/constants/Urls';
import APICall from 'jumbosmash/utils/APICall';

export default function OTPInput(props) {
  const initialState = {input: '', otp: ''};
  const [rejected, setRejected] = useState(false);
  const [state, dispatch] = useReducer(reducer, initialState);
  const [loading, setLoading] = useState(false);

  let email = props.email;
  useEffect(() => {
    const sendOTP = async () => {
      setLoading(true);
      let url = `${urls.backendURL}auth/token/`;
      let result = await APICall.PostNoAuth(url, 
        {'Content-Type': 'application/x-www-form-urlencoded'},
        `email=${email}&token=${state.otp}`
      );

      if (result.error || !result.ok) {
        setLoading(false);
        setRejected(true);
        console.log('rejected');
        return false;
      }

      let storageResult = await APICall.storeToken(result.res.token);
      setLoading(false);
      return storageResult;
    };
    
    if (state.otp.length === 6) {
      sendOTP();
    }
  }, [state.otp, email]);

  return (
    <View style={styles.boxesContainer}>
      {loading && <LoadingModal />}
      {rejected && <Text>Code rejected.</Text>}
      <Text>Enter the code sent to {props.email}</Text>
      <View style={styles.wrap}>
        {createDigitBoxes(state)}
      </View>
      <TextInput 
        style={styles.hidden} 
        autoFocus={true}
        keyboardType='numeric'
        keyboardShouldPersistTaps={'always'}
        onChangeText={text => dispatch({type: 'input', val: text})}
      />
    </View>
  );
}

function DigitBox(props) {
  return (
    <View style={[styles.digitBox, props.selected ? styles.blueBorder : {}]}>
      <Text>
        {props.val}
      </Text>
    </View>
  );
}

function createDigitBoxes(state) {
  return [...Array(6).keys()].map((i) => {
    return (<DigitBox 
      key={i} 
      i={i}
      selected={state.input.length === i}
      val={state.input[i]}
      maxLength={6}
    />);
  });
}

function reducer(state, action) {
  switch(action.type) {
  case 'input':
    if (action.val.length === 6) {
      // Only update otp when a full code is input
      return {...state, input: action.val, otp: action.val};
    }
    return {...state, input: action.val};
  case 'clear':
    return {...state, input: ''};
  case 'rejected':
    return {...state, rejected: action.val};
  }
}


const styles = StyleSheet.create({
  boxesContainer: {
    flex: 1,
    marginTop: '35%'
  },
  digitBox: {
    borderWidth: 1,
    width: '15%',
    aspectRatio: 1,
    alignItems: 'center',
    justifyContent: 'center'
  },
  blueBorder: {
    borderColor: 'blue'
  },
  hidden:{
    display: 'none'
  },
  wrap: {   
    width: '100%',
    flex: 1,
    flexDirection: 'row',
    position: 'relative',
    justifyContent: 'space-around'
  }

});