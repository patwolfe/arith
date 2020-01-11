import React from "react";
import { Text, View } from "react-native";

export default function ChatListItem(props) {
    return (
        <View style={styles.listItem} className="chatListItem">
            <Text>{props.matchName}</Text>
        </View>
    )
}

const styles = {
    listItem: {
        textAlign: 'left',
        padding: '5%',
        width: '100%',
        borderStyle: 'solid',
        borderBottomWidth: '.25%',
    }
}