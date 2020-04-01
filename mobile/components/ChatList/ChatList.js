import React from 'react';
import ChatListItem from 'jumbosmash/components/ChatListItem/ChatListItem';
import { StyleSheet, View } from 'react-native';

export default function ChatList(props) {
  return (
    <View style={styles.list}>
      {props.conversations.map((conv, i) =>
        <ChatListItem
          navigation={props.navigation}
          conversationData={conv} key={i} />)}
    </View>
  );
}

const styles = StyleSheet.create({
  list: {
    marginLeft: '0%',
    marginRight: '0%',
    paddingHorizontal: '0%',
    width: '100%',
  }
});