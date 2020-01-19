import React from "react";
import { Text, TouchableOpacity } from "react-native";

export default function ChatListItem(props) {
  return (
    <TouchableOpacity 
      onPress={() => 
         props.navigation.navigate('Chat', {matchName: props.matchName})}  
      style={styles.listItem} className="chatListItem"
      >
      <Text>{props.matchName}</Text>
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
}