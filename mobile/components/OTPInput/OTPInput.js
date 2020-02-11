import React, { 
  useReducer, useEffect, 
} from 'react';

import { 
  StyleSheet,
  Text,
  TextInput, 
  View 
} from 'react-native';

import urls from 'jumbosmash/constants/Urls';

export default function OTPInput(props) {
  const initialState = {otp: ''};
  const [state, dispatch] = useReducer(reducer, initialState);
  useEffect(() => {
    if (state.otp.length === 6) {
      props.loadingHook(true);
      sendCode(props.email, state.otp);
    }});

  return (
    <View style={styles.boxesContainer}>
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
      selected={state.otp.length === i}
      val={state.otp[i]}
      maxLength={6}
    />);
  });
}

async function sendCode(email, otp) {
  let url = `${urls.backendURL}auth/token/`;
  try {
    const response = await fetch(url, {
      method: 'POST', 
      cache: 'no-cache', 
      redirect: 'folloW', 
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `email=${email}&token=${otp}`
    });
    let res = await response.json();
    console.log(res);
    alert(res.token);
    return true;
  }
  catch (e) {
    console.log(e);
    return true;
  }
}

function reducer(state, action) {
  switch(action.type) {
  case 'input':
    return {...state, otp: action.val};
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