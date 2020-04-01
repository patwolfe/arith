import React from 'react';
import {
  Text,
  View,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';

export default function ChatScreenHeader(props) {
  const matchName = props.navigation.getParam('match_name', 'Undefined');
  
  return (
    <View style={styles.headerContainer}>
      <View style={styles.headerContents}>
        <View>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => 
              props.navigation.navigate('ChatList')}>
            <Text style={styles.backButtonText}>&lt;</Text>
          </TouchableOpacity>
        </View>
        <Text style={styles.headerText}>{matchName}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  backButton: {
    margin: 15,
    alignSelf: 'flex-start'
  },
  backButtonText: {
    color: 'steelblue',
    fontSize: 24,
  },
  headerContainer: {
    borderStyle: 'solid',
    borderBottomWidth: .25,
    minHeight: '7%',
  },
  headerContents: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerText: {
    textAlign: 'center',
    alignContent: 'center',
    fontWeight: 'bold',
    fontSize: 24,
  },
});