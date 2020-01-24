import React, { useState } from "react";
import { TouchableOpacity, Button, View, Text, StyleSheet } from "react-native";
import FeedProfileView from "../FeedProfileView/FeedProfileView";
import {PanGestureHandler} from "react-native-gesture-handler";
import Swipeable from 'react-native-gesture-handler/Swipeable';

export default function MatchFeed() {
    const [state, setState] = useState(
                                {profiles: [<FeedProfileView text="Will" />, 
                                            <FeedProfileView text="Patrick" />, 
                                            <FeedProfileView text="Lexi" />, 
                                            <FeedProfileView text="Steven" />],
                                profile: null,});
    if (!state.profile) {
        setState({profiles: state.profiles.slice(1), profile: state.profiles[0]});
    }

    function changeState(){
        if (state.profiles.length == 0) {
            setState({profiles: [<FeedProfileView text="Will" />, 
                                <FeedProfileView text="Patrick" />, 
                                <FeedProfileView text="Lexi" />],
                    profile: <FeedProfileView text="Steven" />});
        } else {
            setState({profiles: state.profiles.slice(1), 
                    profile: state.profiles[0]});
        }
    }
    let swipeableRef = null;

    return (
        <View style={styles.container}>
            <TouchableOpacity style={styles.button}>
                <Button title="Swipe" onPress={changeState} />
            </TouchableOpacity>
            <Swipeable
                leftThreshold={20}
                rightThreshold={20}
                ref={ref => swipeableRef = ref}
                // Actions that occur when the tab is opened
                onSwipeableLeftOpen={() => {
                    // do something with state.profile
                    swipeableRef.close();
                    changeState();
                }}
                onSwipeableRightOpen={() => {
                    // do something with state.profile
                    swipeableRef.close();
                    changeState();
                }}
                // Render functions for tabs
                renderLeftActions={() => {
                    return (
                        <View style={styles.leftPanel}><Text>Match!</Text></View>
                    );
                }}
                renderRightActions={() => {
                    return (
                        <View style={styles.rightPanel}><Text>Denied!</Text></View>
                    );
                }}
                >
                {state.profile}
            </Swipeable>
        </View>
    );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  button: {
    borderStyle: 'solid',
    borderWidth: 1,
    marginLeft: 50,
    marginRight: 50
  },
  text: {
    textAlign: 'center',
  },
  leftPanel: {
    backgroundColor: '#33cc33',
  },
  rightPanel: {
    backgroundColor: '#ff0000',
  },
});
