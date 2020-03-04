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

/* Props:
  name, pronouns, bio: Strings, all come from previous 
  stage of profile creation
*/
export default function CreateProfileWizard(props) {
  const initState  = {
    name: props.userName,
    pronouns: props.userPronouns,
    bio: 'Just testing',
    pictures: {},
    questions: {},
    stage: 'photos',
    photoSetInfo: null
  };
  const [state, dispatch] = useReducer(reducer, initState); 
  const questionPicker = <QuestionPicker dispatch={dispatch}/>;
  const photoPicker = <PhotoPicker dispatch={dispatch}/>;

  // Fetch s3 urls when component is rendered
  // TODO: figure out if this should just be 
  // done in the submitProfile function
  useEffect(() => {
    getEditProfile(dispatch);
  }, []);

  useEffect(() => {
    if (state.stage === 'done') {
      Alert.alert('Submitted!');
    }
  });

  return (
    <View style={styles.wizard}>
      {state.stage === 'questions' ? questionPicker : photoPicker}
      <Button 
        title={state.stage === 'questions' ? 'Submit' : 'Next'}
        onPress={state.stage === 'questions' ? 
          () => submitProfile(dispatch, state) : 
          () => dispatch({type: 'button'})}/>
    </View>
  );
}

async function getEditProfile(dispatch) {
  const url = `${urls.backendURL}user/profile/edit/`;
  const result = await APICall.GetAuth(url);
  if (result.error || !result.ok) {
    console.log(result);
    return false;
  }

  // save urls in state
  dispatch({type: 'updatePhotoSetInfo', photoSetInfo: result.res});
}

async function submitProfile(dispatch, state) {
  let uris = Object.values(state.pictures).reduce(
    (acc, elem) => elem !== '' ? [...acc, elem] : acc, []);
  const uploads = uris.map((uri, i) => uploadPicture(uri, state.photoSetInfo.d[i][1].fields));
  const results = await Promise.all(uploads);
  if (results.some((elem) => elem === false)) {
    return false;
  }

  await uploadProfile(state, uris.map((uri, i) => state.photoSetInfo.d[i][0]));
  dispatch({type: 'button'});
  return true;
}

async function uploadProfile(state, ids) {
  const url = `${urls.backendURL}user/profile/edit/`;
  const body = [...Array(6).keys()].reduce(
    (acc, elem) => ({...acc, [`photo${elem}`]: ids[elem] ? ids[elem] : null}), {bio: state.bio});
 
  const result = await APICall.PostAuth(url,  {Accept: 'application/json', 'Content-Type': 'application/json'}, JSON.stringify(body));
  if (result.error || !result.ok) {
    console.log(result);
    return false;
  }
  return true;
}

async function uploadPicture(imagePath, photoInfo) {
  const body = formDataFromPhotoInfo(photoInfo);
  const filename = imagePath.split('/').pop();
  const photo = {
    uri: imagePath,
    type: 'image/jpg',
    name: `${filename}.jpg` 
  };
  body.append('file', photo);
  
  const url = urls.photoBucketURL;
  await APICall.PostNoAuth(url, {Accept: 'application/json','Content-Type': 'multipart/form-data'}, body);
  return true;
}

function formDataFromPhotoInfo(photoInfo) {
  return Object.keys(photoInfo).reduce(
    (body, key) => {body.append(key, photoInfo[key]); return body;}, 
    new FormData);
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
