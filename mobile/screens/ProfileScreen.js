import React from 'react';
import {
    ScrollView,
    StyleSheet,
    Text,
    View,
    Image,
    Button,
  } from 'react-native';
import user_profile from '../test_data/UserProfile';

export default function ProfileScreen(props) {
  let fields = []
  for (const field in user_profile.questions) {
    fields.push(
      <Text key={field} style={styles.question_grouping}> 
        <Text style={styles.question}> {field} </Text>
        <Text> {user_profile.questions[field]} </Text>
      </Text>
    );
  }
    
  return (
    <ScrollView style={styles.scroll}>
        <View style={styles.profileimg}>
            {/* <Image source={require('../assets/images/icon.png')}/> */}
            <Image source={{uri: `data:image/jpeg;base64,${user_profile.prof_image}`}} 
                    style={{width: 200, height: 200}}/>
        </View>
        <View style={styles.textcontent}>
            <Text style={styles.title}> {user_profile.name} </Text>
            <Text> {user_profile.pronouns} </Text>
            { fields }
        </View>
        <Button
          title="Edit Profile"
          color="#aaa"
          onPress={() => props.navigation.navigate('Edit')}
        />
    </ScrollView>
  );
}

ProfileScreen.navigationOptions = (props) => ({
  headerTitle: 'Your Profile',
  headerRight: (
      <Button
      title="Edit Profile"
      color="#aaa"
      onPress={() => props.navigation.navigate('Edit')}
      />)
});

const styles = StyleSheet.create({
    profileimg: {
        justifyContent: 'center',
        alignItems: 'center',
        padding: 15,
    },
    textcontent: {
        paddingLeft: 25,
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