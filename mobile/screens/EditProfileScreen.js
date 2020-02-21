import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  View,
  Image,
} from 'react-native';

import profiles from '../test_data/mockProfiles';
import TextInput from '../components/TextInput/TextInput';
import Button from '../components/Button/Button';


export default function EditProfileScreen() {
  let userProfile = profiles['patrick'];
  let fields = [];
  for (const field in userProfile.questions) {
    fields.push(
      <View key={field} style={styles.questionGrouping}> 
        <Text style={styles.question}> {field} </Text>
        <TextInput
          style={styles.textBox}
          initText={userProfile.questions[field]}
          canExpand={true}
          displayCount={true}
        />
      </View>
    );
  }
    
  return (
    <ScrollView style={styles.scroll}>
      <View style={styles.profileImg}>
        <Image source={userProfile.profile_image} style={styles.image}/>
      </View>
      <View style={styles.textContent}>
        <Text style={styles.title}> {userProfile.name} </Text>
        <Text> {userProfile.pronouns} </Text>
        { fields }
      </View>
    </ScrollView>
  );
}

EditProfileScreen.navigationOptions = {
  headerTitle: 'Your Profile',
};

const styles = StyleSheet.create({
  scroll: {
    flex: 1,
    margin: 30,
  },
  profileImg: {
    justifyContent: 'center',
    alignItems: 'center',
    aspectRatio: 1,
  },
  image: {
    height: '90%',
    width: '90%',
    resizeMode: 'contain',
  },
  textContent: {
    paddingLeft: 25,
  },
  textBox: {
    borderColor: 'black',
    borderBottomWidth: 1,
    width: 200,
  },
  title: {
    fontSize: 30,
  },
  question: {
    fontWeight: 'bold',
  },
  questionGrouping: {
    paddingTop: 10,
  }
});