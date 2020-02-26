import React, { useEffect } from 'react';
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

import blobs from 'jumbosmash/constants/Blobs';

export default function ChatScreen(props) {
  const initialState = {
    keyboardavoidingviewkey: false,
    textInput: '',
    // TODO: Get actual messages from backend
    messages: [{content: 'Hi how\'re you doing?', author: 'me'}, 
      {content: 'Good good, you?', author: 'them'},
    ],
  };
  
  const [state, setState] = React.useState(initialState);
  
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
        gradient={{start_color: '#E13D71', end_color: '#5E43C4'}}
        blobs={blobs.cold_blobs}>
        <SafeAreaView style={styles.safeView}>
          <ChatScreenHeader navigation={props.navigation} />
          <KeyboardAvoidingView behavior='padding'
            enabled keyboardVerticalOffset={50}
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
                  disabled={state.textInput == ''}
                  onPress={() => setState(() => ({
                    ...state,
                    textInput: '', 
                    messages: state.messages.concat({content: state.textInput, author: 'me'})}))}>
                  <Text style={styles.sendButtonText}>^</Text>
                </TouchableOpacity>
              </View>
              <View style={styles.chatContainer}>
                <ChatView messages={state.messages} />
              </View>
            </View>
          </KeyboardAvoidingView>
        </SafeAreaView>
      </BlobBackground>
    </View>
  );
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
    borderColor: 'gray', 
    borderWidth: 1,
    alignSelf: 'center',
    marginBottom: '1%',
    marginTop: '1%',
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
    color: 'steelblue',
  },
  textBar: {
    flexDirection: 'row',
    justifyContent: 'center',
    borderStyle: 'solid',
    borderTopColor: 'gray',
    borderTopWidth: .25,
  },
});