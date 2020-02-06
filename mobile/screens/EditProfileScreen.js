import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  Image,
} from 'react-native';

import profiles from '../test_data/mockProfiles';


export default function ProfileScreen() {
  let userProfile = profiles['patrick'];
  let fields = [];
  for (const field in userProfile.questions) {
    fields.push(
      <View key={field} style={styles.question_grouping}> 
        <Text style={styles.question}> {field} </Text>
        <TextInput
          style={styles.textbox}
          value={userProfile.questions[field]}
        />
      </View>
    );
  }
    
  return (
      <ScrollView style={styles.scroll}>
        <View style={styles.profileimg}>
          <Image source={userProfile.profile_image} style={styles.image}/>
        </View>
        <View style={styles.textcontent}>
          <Text style={styles.title}> {userProfile.name} </Text>
          <Text> {userProfile.pronouns} </Text>
          { fields }
        </View>
      </ScrollView>
  );
}

ProfileScreen.navigationOptions = {
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