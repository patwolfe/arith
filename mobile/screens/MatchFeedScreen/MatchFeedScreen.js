import React from 'react';
import { ScrollView, View, StyleSheet, Text } from 'react-native';
import MatchFeed from '../../components/MatchFeed/MatchFeed';

export default function MatchFeedScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>Feed</Text>
      </View>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}>
        <MatchFeed />
      </ScrollView>
    </View>
  );
}

MatchFeedScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    margin: 0,
  },
  contentContainer: {
    // paddingTop: 30,
  },
  header: {
    marginBottom: 10,
    marginTop: 20,
  },
  headerText: {
    textAlign: 'center',
    fontSize: 32,
  },
});
