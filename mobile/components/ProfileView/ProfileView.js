import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  View,
  Image,
  Button,
} from 'react-native';

export default function ProfileView(props) {
  let fields = [];
  for (const field in props.userProfile.questions) {
    fields.push(
      <View key={field} style={styles.question_grouping}> 
        <Text style={styles.question}> {field} </Text>
        <Text> {props.userProfile.questions[field]} </Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.scroll}>
      <View style={styles.profileimg}>
        <Image source={props.userProfile.profile_image} style={styles.image}/>
      </View>
      <View style={styles.textcontent}>
        <Text style={styles.title}> {props.userProfile.name} </Text>
        <Text> {props.userProfile.pronouns} </Text>
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
    paddingLeft: 20,
    paddingRight: 20,
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