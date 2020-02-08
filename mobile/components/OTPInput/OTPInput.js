import React, { 
  forwardRef, 
  useEffect, 
  useRef,
  useReducer, 
  createRef
  } from 'react';
import { StyleSheet, TextInput , View } from 'react-native';

export default function OTPInput(props) {
  const initialState = {
    otp: new Array(6).fill(null),
    curr: 0
  }
  const [state, dispatch] = useReducer(reducer, initialState);

  const elRef = useRef([]);
  useEffect(() => elRef.current[state.curr] && elRef.current[state.curr].focus());
  return (
    <View style={styles.boxesContainer}>
      <View style={styles.wrap}>
        {createDigitBoxes(elRef, dispatch)}
      </View>
    </View>
  );
}

const DigitBox = forwardRef((props, ref) => (
  <TextInput
    ref={ref}
    style={styles.digitBox} 
    onChangeText={(v) => props.dispatch({type: 'input', val: v, i: props.i})}
    onKeyPress={e => {
      if (e.nativeEvent.key === "Backspace") {
        console.log('Pressed back');
        props.dispatch({type: 'back', i: props.i})
      }}
    }
    maxLength={1}
    keyboardType='numeric'/>
));

function createDigitBoxes(elRef, dispatch) {
  return [...Array(6).keys()].map((i) => {
    console.log('Rendering box ' + i + '...');
    return (<DigitBox 
              key={i} 
              i={i}
              ref={el => elRef.current[i] = el}
              dispatch={dispatch}
            />);
  });
}

function reducer(state, action) {
  switch(action.type) {
  case 'input':
    if (state.curr < 5) {
      console.log(state.otp);
      console.log(action.val);
      return {
        ...state, 
        otp: [...state.otp.slice(0, action.i), action.val, ...state.otp.slice(action.i + 1)],
        curr: state.curr + 1
      };
    }
    else {
      let otp = [...state.otp.slice(0, action.i), action.val];
      console.log(otp);
      console.log(otp.join(''));
      return {...state, otp: otp};
    }
  case 'back':
      return {
        ...state, 
        otp: [...state.otp.slice(0, action.i), null, ...state.otp.slice(action.i)],
        curr: state.curr > 0 ? state.curr - 1 : state.curr
      };
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
    alignItems: "center",
    justifyContent: "center"
  },
  wrap: {   
    width: '100%',
    flex: 1,
    flexDirection: 'row',
    position: "relative",
    justifyContent: "space-around"
  }

});