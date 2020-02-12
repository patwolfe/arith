import React, { useReducer, useEffect } from 'react';
import {
  Button,
  StyleSheet,
  View,
  Alert,
} from 'react-native';

import APICall from 'jumbosmash/utils/APICall';
import PhotoPicker from 'jumbosmash/components/PhotoPicker/PhotoPicker';
import QuestionPicker from 'jumbosmash/components/QuestionPicker/QuestionPicker';
import urls from 'jumbosmash/constants/Urls';

export default function CreateProfileWizard(props) {
  const initProfile  = {
    name: props.userName,
    pronouns: props.userPronouns,
    pictures: {},
    questions: {},
    stage: 'questions'
  };
  const [state, dispatch] = useReducer(reducer, initProfile); 
  let questionPicker = <QuestionPicker dispatch={dispatch}/>;
  let photoPicker = <PhotoPicker dispatch={dispatch}/>;

  // Fetch s3 urls when component is rendered
  useEffect(() => {
    getEditProfile();
  }, []);

  useEffect(() => {
    if (state.stage === 'done') {
      //sendProfile();
    }
  }, [state]);

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

async function getEditProfile() {
  const url = `${urls.backendURL}user/profile/edit/`;
  let res = await APICall.GetAuth(url);
  console.log(res);
}


function reducer(state, action) {
  switch(action.type) {
  case 'picture':
    return {...state, pictures: {...state.pictures, [action.id]: action.payload}};
  case 'question':      
    return {...state, questions: {...state.questions, [action.id]: action.payload}};
  case 'button': {
    let nextStep = '';
    if (state.currStep === 'photos') {
      nextStep = 'questions';
    } else { 
      nextStep = 'done';
    }
    return {...state, stage: nextStep};
  }
  default:
    throw new Error();
  }
}

const styles = StyleSheet.create({
  wizard: {
    flex: 1
  }
});
