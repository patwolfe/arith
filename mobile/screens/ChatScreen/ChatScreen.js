import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

export default function ChatScreen(props) {
  const matchName = props.navigation.getParam('matchName', 'Undefined');
  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}>
        <View>
          <View style={styles.headerContainer}>
            <Text style={styles.headerText}>{matchName}</Text>
          </View>
          <Text>On the match screen!!</Text>

        </View>

      </ScrollView>

    </View>
  );
}

ChatScreen.navigationOptions = {
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