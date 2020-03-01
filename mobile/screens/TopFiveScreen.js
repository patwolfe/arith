import React, { useState } from 'react';
import Autocomplete from 'jumbosmash/components/Autocomplete/Autocomplete';
import {
  Button,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet
} from 'react-native';
import Button from 'jumbosmash/components/Button/Button';
import namesList from '../test_data/SeniorNames';

export default function TopFiveScreen() {
  const [names, setNames] = useState(['', '', '', '', '']);

  // puts namesList into [{name: 'Patrick'}, {name: 'Caroline'}] format
  // is this going to be super slow and horrible? I don't know
  const namesFormattedList = namesList;
  let fields = [];

  Array.from(Array(5).keys()).map(x => {
    const z = 5 - x;
    fields.push(
      <View style={{ zIndex: z }}>
        <Autocomplete
          list={namesFormattedList}
          onChangeText={(text) => {
            let n = names;
            n[x] = text;
            setNames(n);
          }}
        />
        <View style={styles.autocomplete}/>
      </View>
      
    );
  });

  return(
    <View >
      <Text style={styles.text}> 1: </Text>
      {fields}
      <Button title={'Submit'} />
    </View>
  );
}

const styles = StyleSheet.create({
  text: {
    fontSize: 20,
  },
  autocomplete: {
    height: 20,
  },
  container: {
    flex: 1,
    flexDirection: 'row',
  }
});