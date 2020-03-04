import React from 'react';
import { StyleSheet, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function BlobBackground(props) {
  function make_blob(blob_props, i) {
    const blob_style = {
      ...blob_props.style,
      zIndex: blob_props.zIndex,
    };

    return (<blob_props.image width={blob_props.width} height={blob_props.height} style={blob_style} key={i} />);
  }
  
  const viewStyle = {
    ...props.style,
    ...styles.viewStyle, // last spread overwrites previous' keys
  };

  return (
    <View style={viewStyle}>
      <LinearGradient colors={[props.gradient.start_color, props.gradient.end_color]} style={styles.linearGradient}>
        {props.blobs ? props.blobs.map(make_blob) : <View />}
        <View style={styles.child_container}>
          {props.children}
        </View>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  viewStyle: {
    zIndex: 0,
    flex: 1,
    width: '100%',
    height: '100%',
  },
  linearGradient: {
    zIndex: 0,
    flex: 1,
  },
  child_container: {
    zIndex: 2,
    flex: 1,
  },
});