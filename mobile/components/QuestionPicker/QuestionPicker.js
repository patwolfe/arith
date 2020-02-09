import React from 'react';
import { 
  ScrollView,
  StyleSheet, 
} from 'react-native';
import Question from './Question/Question';
import mockQuestions from 'jumbosmash/test_data/mockQuestions';

export default function QuestionPicker(props) {
  return (
    <ScrollView style={styles.questionContainer}>
      {mockQuestions.questions.map((question, i) => { 
        return (<Question question={question} key={i} id={i} dispatch={props.dispatch}/>);})}
    </ScrollView>
  );
}

const styles =  StyleSheet.create({
  questionContainer: {
    marginTop: '10%'
  }    
});