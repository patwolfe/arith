import React, { useState, useEffect } from 'react';
import Autocomplete from 'jumbosmash/components/Autocomplete/Autocomplete';
import {
  View,
  StyleSheet
} from 'react-native';
import urls from 'jumbosmash/constants/Urls';

import APICall from 'jumbosmash/utils/APICall';
import Button from 'jumbosmash/components/Button/Button';
import LoadingModal from 'jumbosmash/components/LoadingModal/LoadingModal';

export default function TopFiveScreen() {
  const [names, setNames] = useState(['', '', '', '', '']);
  const [namesList, setNamesList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [rejected, setRejected] = useState(false);

  useEffect(() => {
    const getNames = async () => {
      let url = `${urls.backendURL}user/list/`;
      let result = await APICall.GetAuth(url);

      // TODO: Handle rejection
      if (result.error || !result.ok) {
        setLoading(false);
        setRejected(true);
        return false;
      }

      setNamesList(result.res.map(x => {....x, displayName: (x.preferredName ? x.preferredName : x.firstName) + ' ' + x.lastName)}
        x.displayName = (x.preferredName ? x.preferredName : x.firstName) + ' ' + x.lastName; 
        return x;
      }));
      setLoading(false);
      return true;
    };
    
    // Don't send OTP when component is first rendered
    getNames();
  }, []);

  let fields = [];

  Array.from(Array(5).keys()).map(x => {
    const z = 5 - x;
    fields.push(
      <View key={String(x)} style={{ zIndex: z }}>
        <Autocomplete
          // id={x}
          list={namesList}
          onChangeText={(text) => {
            setNames((names) => {
              let n = names;
              n[x] = text;
              return n;
            });
          }}
        />
        <View style={styles.autocomplete}/>
      </View>
      
    );
  });


  // TODO: add rejected logic
  return(
    <View >
      {loading && <LoadingModal />}
      {!loading && fields}
      <Button title={'Submit'} 
        onClick={() => onSubmit(namesList, names)}
      />
    </View>
  );
}

async function onSubmit(allNames, topFive) {
  let errorNames = [];
  let ids = [];
  topFive = topFive.filter(x => x != '');
  for(const name of topFive) {
    const match = allNames.filter((n) =>  n.displayName === name );
    if(match.length > 0) {
      ids.push(match[0].id);
    } else {
      errorNames.push(name);
    }
  }
  if (errorNames.length != 0) {
    alert('The following names are not valid: ' 
    + errorNames.join(', ')
    + '. Please ensure that the names you entered match the formatting in our list.');
  } else {
    // send request
    topFive = topFive.filter((value, index) => topFive.indexOf(value) === index)
    alert('Submitting the following names: '
    + topFive.join(', '));
    const url = `${urls.backendURL}swipe/top5/`;
    ids = ids.filter((value, index) => ids.indexOf(value) === index)
    const body = [];
    for (const id of ids) {
      body.push({"user": id});
    }
    let result = await APICall.PostAuth(url, {'Content-Type': 'application/json'}, JSON.stringify(body));
  }
} 

const styles = StyleSheet.create({
  text: {
    fontSize: 20,
  },
  autocomplete: {
    height: 20,
  },
});
