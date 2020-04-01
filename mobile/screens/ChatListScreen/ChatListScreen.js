import React, { useEffect, useState } from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
} from 'react-native';
import APICall from 'jumbosmash/utils/APICall';
import urls from 'jumbosmash/constants/Urls';
import ChatList from 'jumbosmash/components/ChatList/ChatList';

const initialState = {
  conversationList: [],
  error: false,
};

// TODO: Add ability to refresh, remove print statements
export default function ChatListScreen(props) {
  const [state, setState] = useState(initialState);

  useEffect(() => {
    getConversations(setState);  
  },[]);

  const errorText = state.error ? <Text>Error loading messages!!</Text> : <View />;

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}>
        <View>
          <View style={styles.headerContainer}>
            <Text style={styles.headerText}>Chat</Text>
          </View>
          {errorText}
          <TouchableOpacity onPress={() => getConversation(1)}>
            <Text>PRESS TO GET MESSAGES FOR CHAT 1</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => props.navigation.navigate('Chat', {match_id: 1, match_name: 'TESTUSER2_FIRST'})}>
            <Text>PRESS TO NAVIGATE TO CHAT SCREEN FOR USER 1</Text>
          </TouchableOpacity>
          <ChatList navigation={props.navigation} conversations={state.conversationList}/>
        </View>

      </ScrollView>

    </View>
  );
}

ChatListScreen.navigationOptions = {
  header: null,
};

async function getConversation(match_id) {
  const url = `${urls.backendURL}chat/convo?match=${match_id}`;
  const headers = {'Content-Type': 'application/json'};
  const response = await APICall.GetAuth(url, headers);
  if (response.error || !response.ok) {
    console.log(`Bad request to ${url}`);
    console.log('Result was: ');
    console.log(response);
  } else {
    console.log('Request succeeded!');
    console.log(response);
  }
}

async function getConversations(setState) {
  const url = `${urls.backendURL}chat/all/`;
  const result = await APICall.GetAuth(url);

  if (result.error || !result.ok) {
    console.log('error in /chat/all request!');
    setState({conversationList: [], error: true});
  } else {
    setState({conversationList: result.res, error: false});
  }
}

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