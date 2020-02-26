import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
} from 'react-native';

/* Props
 * darkMode: bool, decides the color of the bar below the box (default false)
 * title: text to show on the button
 * onClick: function to pass to Button's onClick()
 */
export default function Button(props) {

  // determines text vs. background color (for dark or light screen)
  const barColor = props.darkMode ? ['white', 'black'] : ['black', 'white'];
  return (
    <TouchableOpacity 
      style={[styles.button, {backgroundColor: barColor[0]}]}
      onPress={props.onClick}>
      <Text style={[styles.text, {color: barColor[1]}]}> 
        {props.title} 
      </Text>
    </TouchableOpacity>
  );  
}

const styles = StyleSheet.create({
  button: {
    borderRadius: 20,
    fontSize: 50,
    backgroundColor: 'black',
    padding: 10,
    width: '60%',
    alignItems: 'center',
  },
  text: {
    color: 'white',
    fontWeight: '700',
  }
});