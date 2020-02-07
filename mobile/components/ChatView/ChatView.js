import React from 'react';

import {
  View,
  StyleSheet,
  Text,
  ScrollView,
} from 'react-native';

export default function ChatView(props) {
  let scrollViewRef = null;
  return (
    <ScrollView
      ref={ref => scrollViewRef = ref}
      onContentSizeChange={(_, __)=>{        
        scrollViewRef.scrollToEnd({animated: true});}}>
      {props.messages.map(
        (message, i) => {
          const [rowstyle, messagestyle, textstyle] = 
            message.author == 'me' 
              ? [styles.chatMessageSent, 
                styles.chatMessageSentContainer, 
                styles.chatMessageSentText] 
              : [styles.chatMessageReceived, 
                styles.chatMessageReceivedContainer, 
                styles.chatMessageReceivedText];
          return (
            <View key={i}>
              <View style={rowstyle}>
                <View style={messagestyle}>
                  <Text style={textstyle}>{message.content}</Text>
                </View>
              </View>
            </View>
          );
        })}
    </ScrollView>
  );
}

const styles = StyleSheet.create(
  {
    textInput: {
      height: 40, 
      width: '90%',
      borderColor: 'gray', 
      borderWidth: 1,
      alignSelf: 'center',
    },
    chatMessageSent: {
      flex: 1,
      flexDirection: 'row-reverse',
      justifyContent: 'flex-start',
      margin: 3,
    },
    chatMessageSentContainer: {
      backgroundColor: '#147efb',
      maxWidth: '60%',
      padding: '2%',
    },
    chatMessageReceived: {
      flex: 1,
      flexDirection: 'row',
      justifyContent: 'flex-start',
      margin: 3,
    },
    chatMessageReceivedContainer: {
      maxWidth: '60%',
      backgroundColor: '#d3d3d3',
      padding: '2%',
    },
    chatMessageReceivedText: {
      fontSize: 18,
      justifyContent: 'flex-start',
      flex: 1,
      color: 'black',
    },
    chatMessageSentText: {
      fontSize: 18,
      justifyContent: 'flex-start',
      flex: 1,
      color: 'white',
    },
  });

