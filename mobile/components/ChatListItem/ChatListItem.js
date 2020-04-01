import React from 'react';
import { Text, TouchableOpacity } from 'react-native';

export default function ChatListItem(props) {
  const name = props.converstionData.user_name;
  const preview = props.conversationData.content;
  const viewed = props.converstionData.viewed;
  return (
    <TouchableOpacity 
      onPress={() => 
        props.navigation.navigate('Chat', {match_id: props.conversationData.match, match_name: name})}  
      style={styles.listItem} className="chatListItem">
      <Text>{name}</Text>
      <Text>{preview}</Text>
      <Text>{viewed?'Viewed':'Unviewed'}</Text>
    </TouchableOpacity>
  );
}

const styles = {
  listItem: {
    textAlign: 'left',
    padding: '5%',
    width: '100%',
    borderStyle: 'solid',
    borderBottomWidth: '.25%',
  }
};