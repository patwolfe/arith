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
  const initState  = {
    profile: {
      name: props.userName,
      pronouns: props.userPronouns,
      bio: 'Just testing',
      pictures: {},
      questions: {},
    },
    stage: 'photos',
    photoSetInfo: null
  };
  const [state, dispatch] = useReducer(reducer, initState); 
  const questionPicker = <QuestionPicker dispatch={dispatch}/>;
  const photoPicker = <PhotoPicker dispatch={dispatch}/>;

  // Fetch s3 urls when component is rendered
  useEffect(() => {
    getEditProfile(dispatch);
  }, []);

  useEffect(() => {
    if (state.stage === 'done') {
      Alert.alert('Submitted!');
      submitProfile(dispatch, state);
    }
  }, [state]);

  return (
    <View style={styles.wizard}>
      {state.stage === 'questions' ? questionPicker : photoPicker}
      <Button 
        title={state.stage === 'questions' ? 'Submit' : 'Next'}
        onPress={() => dispatch({type: 'button'})}/>
    </View>
  );
}

async function getEditProfile(dispatch) {
  const url = `${urls.backendURL}user/profile/edit/`;
  const result = await APICall.GetAuth(url);
  // save urls in state
  dispatch({type: 'updatePhotoSetInfo', photoSetInfo: result.res});
}

async function submitProfile(dispatch, state) {
  await uploadPicture(state.pictures[0], state.photoSetInfo.d[0][1].fields);
  dispatch({type: 'button'});
  return true;
  
}

async function uploadProfile(profile) {
  return true;
}

async function uploadPicture(imagePath, photoInfo) {
  let body = formDataFromPhotoInfo(photoInfo);
  console.log(body);
  return;
  let filename = imagePath.split('/').pop();
  const photo = {
    uri: imagePath,
    type: 'image/jpg',
    name: filename
  };
  body.append('file', photo);
  const url = urls.photoBucketURL;
  await APICall.PostNoAuth(url, {'Content-Type': 'multipart/form-data'}, body);
  return true;
}

function formDataFromPhotoInfo(photoInfo) {
  // let body = new FormData();

  // console.log('----AWS Info----');
  // console.log(`key: ${photoInfo.key}`);
  // console.log(`AWSAccessKeyId: ${photoInfo.AWSAccessKeyId}`);
  // console.log(`policy: ${photoInfo.policy}`);
  // console.log(`signature: ${photoInfo.signature}`);
  // console.log('---------------');

  // body.append('key', photoInfo.key);
  // body.append('AWSAccessKeyId', photoInfo.AWSAccessKeyId);
  // body.append('policy', photoInfo.policy);
  // body.append('signature', photoInfo.signature);
  // return body;
  let body = new FormData();
  return Object.keys(photoInfo).reduce(
    (body, key) => {body.append(key, photoInfo[key]); return body;}, 
    body);
}

function reducer(state, action) {
  switch(action.type) {
  case 'picture':
    return {...state, pictures: {...state.pictures, [action.id]: action.payload}};
  case 'question':      
    return {...state, questions: {...state.questions, [action.id]: action.payload}};
  case 'button': {
    let nextStep = '';
    if (state.stage === 'photos') {
      nextStep = 'questions';
    } else if (state.stage === 'done') {
      nextStep = 'photos';
    } else { 
      nextStep = 'done';
    }
    return {...state, stage: nextStep};
  }
  case 'updatePhotoSetInfo':
    return {...state, photoSetInfo: action.photoSetInfo};
  default:
    throw new Error('Invalid reducer action');
  }
}

const styles = StyleSheet.create({
  wizard: {
    flex: 1
  }
});
