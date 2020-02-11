import { AsyncStorage } from 'react-native';

export default {
  async PostNoAuth(url, headers, body) {
    try {
      const response = await fetch(url, {
        method: 'POST', 
        headers: headers,
        body: body,
      });
      let res = await response.json();
      console.log(res);
      return {error: false, ok: response.ok, res: res};
    }
    catch (e) {
      console.log(e);
      return {error: true};
    }
  },

  async storeToken(token) {
    try {
      await AsyncStorage.setItem('token', token);
      return true;
    }
    catch (e) {
      console.log(e);
      return false;
    }
  }
};