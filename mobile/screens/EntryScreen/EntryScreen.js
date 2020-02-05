import React from 'react';
import {
  Button,
  StyleSheet,
  View,
} from 'react-native';

// It's called EntryScreen because https://english.stackexchange.com/a/195828
export default function EntryScreen(props) {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        {/* Header will go here*/}
      </View>
      <Button title="Login"
        onPress={() => 
          props.navigation.navigate('Login')} />
      <Button title="Register" 
        onPress={() => 
          props.navigation.navigate('Register')} />

    </View>
  );
}

EntryScreen.navigationOptions = {
  header: null,
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#a9c6de',
  },
  header: {
    marginTop: '30%',
    padding: '10%',
    backgroundColor: '#ffc6de',
  },
});