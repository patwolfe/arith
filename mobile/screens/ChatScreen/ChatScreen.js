import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  StatusBar,
  Keyboard,
  Platform,
} from 'react-native';
import ChatView from '../../components/ChatView/ChatView';

export default function ChatScreen(props) {
  const initialState = {
    keyboardavoidingviewkey: 0,
    textInput: '',
    messages: [{content: 'Hi how\'re you doing?', author: 'me'}, 
      {content: 'Good good, you?', author: 'them'}, //{content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, {content: 'Good good, you?', author: 'them'}, 
    ],
  };
  const matchName = props.navigation.getParam('matchName', 'Undefined');
  const [state, setState] = React.useState(initialState);
  React.useEffect(() => {
    function updateKey() {
      console.log('key updated to ' + (state.keyboardavoidingviewkey + 1).toString());

      setState({...state, keyboardavoidingviewkey: state.keyboardavoidingviewkey + 1});
    }
    const listener = Keyboard.addListener(Platform.OS === 'android' ? 'keyboardDidHide': 'keyboardWillHide', updateKey);

    return function cleanup(){
      console.log('cleanup');
      listener.remove();
    };
  });
  console.log('rendering');
  return (
    <View style={styles.container}>
      {/* <View>
        <StatusBar backgroundColor="white" barStyle="light-content" />
      </View> */}
      <View style={styles.headerContainer}>
        <View style={styles.headerContents}>
          <View>
            <TouchableOpacity
              style={styles.backButton}
              onPress={() => 
                props.navigation.navigate('ChatList')}>
              <Text style={styles.backButtonText}>&lt;</Text>
            </TouchableOpacity>
          </View>
          <Text style={styles.headerText}>{matchName}</Text>
        </View>
      </View>
      <KeyboardAvoidingView style={styles.chat} behavior='padding' 
        enabled keyboardVerticalOffset={100}
        key={state.keyboardavoidingviewkey}>
        <View style={styles.chat}>
          <View style={styles.textBar}>
            <TextInput
              style={styles.textInput}
              onChangeText={text => setState({...state, textInput: text})}
              value={state.textInput} />
            <TouchableOpacity 
              style={styles.sendButton}
              disabled={state.textInput == ''}
              onPress={() => 
                setState({
                  ...state,
                  textInput: '', 
                  messages: state.messages.concat({content: state.textInput, author: 'me'})})}>
              <Text style={styles.sendButtonText}>^</Text>
            </TouchableOpacity>
          </View>
          <ChatView messages={state.messages} />
        </View>
      </KeyboardAvoidingView>
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
  headerContainer: {
    borderStyle: 'solid',
    borderBottomWidth: .25,
    marginTop: '5%',
    marginBottom: '2%',
    minHeight: '7%',
  },
  headerContents: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerText: {
    textAlign: 'center',
    alignContent: 'center',
    fontWeight: 'bold',
    fontSize: 24,
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
  backButton: {
    margin: 15,
    alignSelf: 'flex-start'
  },
  backButtonText: {
    color: 'steelblue',
    fontSize: 24,
  },
  chat: {
    flex: 1,
    flexDirection: 'column-reverse',
    width: '100%',
  },
  sendButton: {
    margin: '1%',
    width: '5%',
  },
  sendButtonText: {
    fontSize: 24,
    color: 'steelblue',
  },
  textBar: {
    flex: 0,
    flexDirection: 'row',
    justifyContent: 'center',
    borderStyle: 'solid',
    borderTopColor: 'gray',
    borderTopWidth: .25,
  },
});