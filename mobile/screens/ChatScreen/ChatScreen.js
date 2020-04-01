import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Keyboard,
  Platform,
  SafeAreaView,
} from 'react-native';
import ChatView from 'jumbosmash/components/ChatView/ChatView';
import ChatScreenHeader from 'jumbosmash/components/ChatScreenHeader/ChatScreenHeader';
import BlobBackground from 'jumbosmash/components/BlobBackground/BlobBackground';
import colors from 'jumbosmash/constants/Colors';
import blobs from 'jumbosmash/constants/Blobs';
import urls from 'jumbosmash/constants/Urls';
import APICall from 'jumbosmash/utils/APICall';

// TODO: figure out a way to get our own id
const initialState = {
  my_id: 2,
  keyboardavoidingviewkey: false,
  textInput: '',
  messages: [],
};

// Props = {
//   match_id,
//   match_name
// }

export default function ChatScreen(props) {
  const match_id = props.navigation.getParam('match_id', 'Undefined');
  const [state, setState] = useState(initialState);

  // TODO dont know if [match_id] is required, test with and without pls
  useEffect(() => {
    getConversation(match_id, setState);
  }, [match_id]);
  
  useEffect(() => {
    function updateKey() {
      // if we do not give the keyboardavoiding view a new key the padding will
      // stick around when the keyboard hides
      setState((old_state) => ({...old_state, keyboardavoidingviewkey: !old_state.keyboardavoidingviewkey}));
    }
    const listener = Keyboard.addListener(Platform.OS === 'android' ? 'keyboardDidHide': 'keyboardWillHide', updateKey);

    return function cleanup(){
      listener.remove();
    };
  });

  return (
    <View style={styles.container}>
      <BlobBackground style={styles.container}
        gradient={{start_color: colors.chatGradientStart, end_color: colors.chatGradientEnd}}
        blobs={blobs.cold_blobs}>
        <SafeAreaView style={styles.safeView}>
          <ChatScreenHeader navigation={props.navigation} />

          <KeyboardAvoidingView behavior='padding'
            keyboardVerticalOffset={50}
            style={styles.container}
            key={state.keyboardavoidingviewkey}>
            <View style={styles.chat}>
              <View style={styles.textBar}>
                <TextInput
                  style={styles.textInput}
                  onChangeText={text => setState((old_state) =>  ({...old_state, textInput: text}))}
                  value={state.textInput} />
                <TouchableOpacity 
                  style={styles.sendButton}
                  disabled={state.textInput === ''}
                  onPress={() => {
                    sendMessage(state.textInput, match_id);
                    // TODO: see if there is a better way to do this.  Could pull all messages again but idk if that's right...
                    setState(old_state => ({...old_state, 
                      textInput: '', 
                      messages: old_state.messages.concat({
                        content: old_state.textInput, 
                        delivered: null, 
                        id: null,
                        match: match_id, 
                        read: null, 
                        sender: old_state.my_id,
                        sent: ''})}));
                  }}>
                  <Text style={styles.sendButtonText}>^</Text>
                </TouchableOpacity>
              </View>
              <View style={styles.chatContainer}>
                <ChatView messages={state.messages} my_id={state.my_id}/> 
              </View>
            </View>
          </KeyboardAvoidingView>
        </SafeAreaView>
      </BlobBackground>
    </View>
  );
}

async function getConversation(match_id, setState) {
  const url = `${urls.backendURL}chat/convo?match=${match_id}`;
  const headers = {'Content-Type': 'application/json'};
  const response = await APICall.GetAuth(url, headers);
  if (response.error || !response.ok) {
    console.log(`Bad request to ${url}`);
    console.log('Result was: ');
    console.log(response);
  } else {
    setState((old_state) => ({...old_state, messages: response.res}));
  }
}

async function sendMessage(message, match_id) {
  const uri = `${urls.backendURL}chat/send`;
  const headers = {'Content-Type': 'application/json'};
  const body = {match: match_id, content: message};
  const response = await APICall.PostAuth(uri, headers, JSON.stringify(body));

  if (response.error || !response.ok) {
    console.log('Bad send message request:');
    console.log(body);
    console.log('Response: ');
    console.log(response);
  }
}

ChatScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeView: {
    backgroundColor: 'transparent',
    flex: 1,
  },
  textInput: {
    height: 40, 
    width: '90%',
    borderColor: 'lightgray', 
    borderWidth: 1,
    alignSelf: 'center',
    marginBottom: '1%',
    marginTop: '1%',
    borderRadius: 10,
  },
  chat: {
    flex: 1,
    flexDirection: 'column-reverse',
    width: '100%',
  },
  chatContainer: {
    flex: 1,
  },
  sendButton: {
    margin: '1%',
    minWidth: '5%',
  },
  sendButtonText: {
    fontSize: 32,
    color: 'lightgray',
  },
  textBar: {
    flexDirection: 'row',
    justifyContent: 'center',
    borderStyle: 'solid',
    borderTopColor: 'black',
    borderTopWidth: .25,
    backgroundColor: '#525252',
  },
});