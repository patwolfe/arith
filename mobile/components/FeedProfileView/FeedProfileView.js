import React from 'react';
import { TouchableOpacity, View, Text, StyleSheet } from 'react-native';

export default function FeedProfileView(props) {
  return (
    <TouchableOpacity>
      <View style={styles.container}><Text style={styles.text}>{props.text}</Text></View>
    </TouchableOpacity>  
  );
}

const styles = StyleSheet.create({
  text: {
    textAlign: 'center'
  }
});
