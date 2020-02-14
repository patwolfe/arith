import React from 'react';
import {
  TextInput,
  StyleSheet,
} from 'react-native';

/* Props
 * darkMode: bool, decides the color of the bar below the box (default false)
 * initText: initial content of the text box on load
 * canExpand: bool, whether it can be more than one line or not
 * onChangeText: what should happen with the text when it changes
 */
export default function TextInputCustom(props) {
  const initialText = props.initText ? props.initText : '';
  const barColor = props.darkMode ? 'white' : 'black';
  const colorMode = {borderBottomColor: barColor};
  return (
    <TextInput
      defaultValue={initialText}
      maxLength={300}
      multiline={props.canExpand}
      style={[styles.textBox, colorMode]}
      onChangeText={props.onChangeText}
    />
  );  
}

const styles = StyleSheet.create({
  textBox: {
    borderBottomWidth: 2,
    fontSize: 18,
  },
});