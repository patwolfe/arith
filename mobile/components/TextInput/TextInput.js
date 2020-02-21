import React, { useState } from 'react';
import {
  TextInput as TextInputRN,
  Text,
  View,
  StyleSheet,
} from 'react-native';

/* Props
 * darkMode: bool, decides the color of the bar below the box (default false)
 * initText: initial content of the text box on load
 * canExpand: bool, whether it can be more than one line or not
 * onChangeText: what should happen with the text when it changes
 * maxLength: int, max # characters, 300 by default
 * displayCount: bool, whether counter should show or not
 */
export default function TextInput(props) {

  const maxLength = props.maxLength ? props.maxLength : 300;
  const initialText = props.initText ? props.initText : '';
  const barColor = props.darkMode ? 'white' : 'black';
  const colorMode = {borderBottomColor: barColor};

  const [textLength, setTextLength] = useState(initialText.length);
  const counter = props.displayCount ? <Text>{textLength}/{maxLength}</Text> : <Text />;

  return (
    <View> 
      <TextInputRN
        defaultValue={initialText}
        maxLength={maxLength}
        multiline={props.canExpand}
        style={[styles.textBox, colorMode]}
        onChangeText={(newText) => {
          setTextLength(newText.length);
          props.onChangeText;
        }}
      />
      {counter}
    </View>
  );  
}

const styles = StyleSheet.create({
  textBox: {
    borderBottomWidth: 2,
    fontSize: 18,
  },
});