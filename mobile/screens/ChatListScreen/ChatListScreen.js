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
            <Text style={styles.headerText}>Chat</Text>
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
  },
  contentContainer: {
    paddingTop: 50,
  },
  headerContainer: {
    borderStyle: 'solid',
    borderBottomWidth: .25,
    paddingBottom: '5%',
  },
  headerText: {
    textAlign: 'left',
    alignContent: 'center',
    fontWeight: 'bold',
    fontSize: 24,
    paddingLeft: 30,
  }
});