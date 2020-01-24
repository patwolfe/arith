import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import ChatList from '../../components/ChatList/ChatList';

export default function ChatListScreen(props) {
  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}>
        <View>
          <View style={styles.headerContainer}>
            <Text style={styles.headerText}>Chats</Text>
          </View>
          <ChatList navigation={props.navigation}/>
        
        </View>

      </ScrollView>

    </View>
  );
}

ChatListScreen.navigationOptions = {
  header: null,
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#a9c6de',
  },
  contentContainer: {
    paddingTop: 30,
  },
  headerContainer: {
    borderStyle: 'solid',
    borderBottomWidth: .25,
    paddingBottom: '5%',
  },
  headerText: {
    textAlign: 'center',
    alignContent: 'center',
    fontWeight: 'bold',
    fontSize: 16,
  }
});