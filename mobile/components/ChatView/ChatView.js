import React, { useEffect } from 'react';

import {
  View,
  StyleSheet,
  Text,
  FlatList,
  Platform,
  Keyboard,
} from 'react-native';

export default function ChatView(props) {
  let flatListRef = null;
  let lastMessage = null;

  function scrollToEnd() {
    flatListRef.scrollToEnd({animated: true});
  }

  useEffect(() => {
    // When the keyboard opens scroll to the bottom
    const listener = Keyboard.addListener(Platform.OS === 'android' 
      ? 'keyboardDidShow'
      : 'keyboardWillShow', scrollToEnd);

    // Remove listener when component unmounts
    return function cleanup(){
      listener.remove();
    };
  });

  return (
    <FlatList
      style={styles.container}
      ListFooterComponent={() => (<View style={styles.listFooter}></View>)}
      data={props.messages}
      ref={ref => flatListRef = ref}
      onContentSizeChange={() => scrollToEnd()}
      initialNumToRender={50}
      keyExtractor={(_, i) => i.toString()}
      renderItem={({item}) => {
        const message = item;
        const [rowstyle, messagestyle, textstyle] = 
          message.author == 'me' 
            ? [styles.chatMessageSent, 
              styles.chatMessageSentContainer, 
              styles.chatMessageSentText] 
            : [styles.chatMessageReceived, 
              styles.chatMessageReceivedContainer, 
              styles.chatMessageReceivedText];
        const spacing_wrapper = (lastMessage && (lastMessage.author == message.author) 
          ? styles.chatSpacingWrapperSame 
          : styles.chatSpacingWrapperDiff);
        lastMessage = message;
        return (
          <View>
            <View style={spacing_wrapper}></View>
            <View style={rowstyle}>
              <View style={messagestyle}>
                <Text style={textstyle}>{message.content}</Text>
              </View>
            </View>
          </View> 
        );
      }}/>
  );
}

const styles = StyleSheet.create({
  container: {
    flexShrink: 1,
    flexGrow: 1,
  },
  listFooter: {
    height: 50,
  },
  chatMessageSent: {
    flexDirection: 'row-reverse',
    justifyContent: 'flex-start',
    margin: 2,
  },
  chatMessageSentContainer: {
    backgroundColor: '#147efb',
    maxWidth: '60%',
    padding: '2%',
  },
  chatMessageReceived: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    margin: 2,
  },
  chatMessageReceivedContainer: {
    maxWidth: '60%',
    backgroundColor: '#d3d3d3',
    padding: '2%',
  },
  chatMessageReceivedText: {
    fontSize: 18,
    justifyContent: 'flex-start',
    color: 'black',
  },
  chatMessageSentText: {
    fontSize: 18,
    justifyContent: 'flex-start',
    color: 'white',
  },
  chatSpacingWrapperSame: {
    maxHeight: '0%',
  },
  chatSpacingWrapperDiff: {
    minHeight: '2%',
  },
});
