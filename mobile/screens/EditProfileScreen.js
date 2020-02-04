import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  Image,
} from 'react-native';
import user_profile from 'jumbosmash/test_data/UserProfile';

export default function ProfileScreen() {
  /**
   * Go ahead and delete ExpoConfigView and replace it with your content;
   * we just wanted to give you a quick view of your config.
   */
  let fields = [];
  for (const field in user_profile.questions) {
    fields.push(
      <View key={field} style={styles.question_grouping}> 
        <Text style={styles.question}> {field} </Text>
        <TextInput
          style={styles.textbox}
          value={user_profile.questions[field]}
        />
      </View>
    );
  }
    
  return (
    <View>
      <ScrollView>
        <View style={styles.profileimg}>
          {/* <Image source={require('../assets/images/icon.png')}/> */}
          <Image source={{uri: `data:image/jpeg;base64,${user_profile.prof_image}`}} 
            style={styles.image}/>
        </View>
        <View style={styles.textcontent}>
          <Text style={styles.title}> {user_profile.name} </Text>
          <Text> {user_profile.pronouns} </Text>
          { fields }
        </View>
      </ScrollView>
    </View>
  );
}

ProfileScreen.navigationOptions = {
  headerTitle: 'Your Profile',
};

const styles = StyleSheet.create({
  profileimg: {
    justifyContent: 'center',
    alignItems: 'center',
    padding: 15,
  },
  image: {
    height: 200,
    width: 200
  },
  textcontent: {
    paddingLeft: 25,
  },
  textbox: {
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
  question_grouping: {
    paddingTop: 10,
  }
});