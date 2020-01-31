import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  View,
  Image,
  Button,
} from 'react-native';
// import user_profile from '../../test_data/UserProfiles';

export default function ProfileView(props) {
  let fields = [];
  for (const field in props.user_profile.questions) {
    fields.push(
      <Text key={field} style={styles.question_grouping}> 
        <Text style={styles.question}> {field} </Text>
        <Text> {props.user_profile.questions[field]} </Text>
      </Text>
    );
  }

  console.log(props.user_profile);

  return (
    <ScrollView style={styles.scroll}>
      <View style={styles.profileimg}>
        <Image source={props.user_profile.profile_image} style={styles.image}/>
      </View>
      <View style={styles.textcontent}>
        <Text style={styles.title}> {props.user_profile.name} </Text>
        <Text> {props.user_profile.pronouns} </Text>
        { fields }
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scroll: {
    flex: 1,
    margin: 30,
  },
  profileimg: {
    justifyContent: 'center',
    alignItems: 'center',
    aspectRatio: 1,
  },
  image: {
    height: '90%',
    width: '90%',
    resizeMode: 'contain',
  },
  textcontent: {
    paddingLeft: 20,
    paddingRight: 20,
  },
  title: {
    fontSize: 30,
  },
  question: {
    fontWeight: 'bold',
  },
  question_grouping: {
    paddingTop: 10,
  }
});