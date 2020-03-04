import React from 'react';
import { 
  StyleSheet,
  Text, 
  TextInput, 
  View } from 'react-native';

/* Props:
 * dispatch: function from userReducer in parent component
 * that update's parent state with the filled in question
 * 
 * question: String with question this q/a component is asking
 * 
 * id: Integer key for question used if parent state contains a 
 * list or object of q/a pairs
 */
export default function Question(props) {
  return (
    <View style={styles.container}>
      <Text>{props.question}</Text>
      <TextInput style={styles.inputField}
        editable
        autoCapitalize='none'
        onChangeText={(answer) => 
        {
          props.dispatch(
            {
              type: 'question', 
              id: props.id, 
              payload: {question: props.question, answer: answer}});}}/>
    </View>
  );
}

const styles =  StyleSheet.create({
  container: {
    paddingTop: '10%',
    flex: 1
  },
  inputField: {
    backgroundColor: '#ffffff',
    marginHorizontal: '15%',
    paddingVertical: '2%',
    borderStyle: 'solid',
    borderColor: 'black',
    borderWidth: 1
  },
});
