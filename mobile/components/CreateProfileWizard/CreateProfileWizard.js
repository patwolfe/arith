import React, { useReducer } from 'react';
import {
  Button,
  StyleSheet,
  View,
  Alert,
} from 'react-native';

import PhotoPicker from 'jumbosmash/components/PhotoPicker/PhotoPicker';
import QuestionPicker from 'jumbosmash/components/QuestionPicker/QuestionPicker';

export default function CreateProfileWizard(props) {
  const initState  = {
    name: props.userName,
    pronouns: props.userPronouns,
    pictures: {},
    questions: {},
    stage: 'questions'
  };
  const [state, dispatch] = useReducer(reducer, initState); 
  let questionPicker = <QuestionPicker dispatch={dispatch}/>;
  let photoPicker = <PhotoPicker dispatch={dispatch}/>;
  return (
    <View style={styles.wizard}>
      {state.stage === 'questions' ? questionPicker : photoPicker}
      <Button 
        title={state.stage === 'questions' ? 'Next' : 'Submit'}
        onPress={() => 
        {
          if (state.stage === 'questions')
            dispatch({type: 'button', payload: 'photos'});
          else {
            Alert.alert('Submitted!');
            console.log(state);
          }
        }
        }/>
    </View>
  );
}


function reducer(state, action) {
  switch(action.type) {
  case 'picture':
    return {...state, pictures: {...state.pictures, [action.id]: action.payload}};
  case 'question':      
    return {...state, questions: {...state.questions, [action.id]: action.payload}};
  case 'button':
    return {...state, stage: action.payload};
  default:
    throw new Error();
  }
}

const styles = StyleSheet.create({
  wizard: {
    flex: 1
  }
});
